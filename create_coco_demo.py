#!/usr/bin/env python3

from logzero import logger
import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
from skimage import measure
from pycocotools import mask
from pycococreatortools import pycococreatortools

IMAGE_DIR = 'example_data/images'
ANNOTATION_DIR = 'example_data/annotations'

INFO = {
    "description": "Example Dataset",
    "url": "https://github.com/waspinator/pycococreator",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "waspinator",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'blueberry',
        'supercategory': 'fruit',
    }
]

def main():

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    segmentation_id = 1
    
    for root, directories, files in os.walk(IMAGE_DIR):
        file_types = ['*.jpeg', '*.jpg']
        file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
        files = [os.path.join(root, f) for f in files]
        files = [f for f in files if re.match(file_types, f)]

        # go through each image
        for i, filename in enumerate(files):
            basename_no_extension = os.path.splitext(os.path.basename(filename))[0]
            image = Image.open(filename)
            image_info = pycococreatortools.create_image_info(image_id, os.path.basename(filename), image.size[0], image.size[1])
            coco_output["images"].append(image_info)

            # go through each associated annotation
            for root, directories, files in os.walk(ANNOTATION_DIR):
                file_types = ['*.png']
                file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
                file_name_prefix = basename_no_extension + '.*'
                files = [os.path.join(root, f) for f in files]
                files = [f for f in files if re.match(file_types, f)]
                files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

                for filename in files:
                    basename_no_extension = os.path.splitext(os.path.basename(filename))[0]
                    binary_mask = np.logical_not(np.array(Image.open(filename))).astype(np.uint8)
                    category_info = {'id': 1, 'is_crowd': 'crowd' in basename_no_extension}
                    annotation_info = pycococreatortools.create_annotation_info(segmentation_id, image_id,
                        category_info, binary_mask, image.size)
                    coco_output["annotations"].append(annotation_info)

                    segmentation_id = segmentation_id + 1

            image_id = image_id + 1

    with open('{}/coco_example.json'.format(ANNOTATION_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
