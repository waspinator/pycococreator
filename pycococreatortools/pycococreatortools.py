#!/usr/bin/env python3

import os
import re
import datetime
import numpy as np
from itertools import groupby
from skimage import measure
from PIL import Image
from pycocotools import mask

convert = lambda text: int(text) if text.isdigit() else text.lower()
natrual_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]

def resize_array(array, new_size):
    image = Image.fromarray(array)
    image = image.resize(new_size)
    return np.asarray(image)

def close_contour(contour):
    if not np.array_equal(contour[0], contour[-1]):
        contour = np.vstack((contour, contour[0]))
    return contour

def binary_mask_to_rle(binary_mask):
    rle = {'counts': [], 'size': list(binary_mask.shape)}
    counts = rle.get('counts')
    for i, (value, elements) in enumerate(groupby(binary_mask.ravel(order='F'))):
        if i == 0 and value == 1:
                counts.append(0)
        counts.append(len(list(elements)))

    return rle

def binary_mask_to_polygon(binary_mask):
    polygons = []
    contours = measure.find_contours(binary_mask, 0.5)
    for contour in contours:
        contour = close_contour(contour)
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        polygons.append(segmentation)

    return polygons

def create_image_info(image_id, file_name, image_size, 
                      date_captured=datetime.datetime.utcnow().isoformat(' '),
                      license_id=1, coco_url="", flickr_url=""):

    image_info = {
            "id": image_id,
            "file_name": file_name,
            "width": image_size[0],
            "height": image_size[1],
            "date_captured": date_captured,
            "license": license_id,
            "coco_url": coco_url,
            "flickr_url": flickr_url
    }

    return image_info

def create_annotation_info(annotation_id, image_id, category_info, binary_mask, image_size):
    binary_mask = resize_array(binary_mask, image_size)
    binary_mask_encoded = mask.encode(np.asfortranarray(binary_mask.astype(np.uint8)))
    bounding_box = mask.toBbox(binary_mask_encoded)
    area = mask.area(binary_mask_encoded)

    if category_info["is_crowd"]:
        annotation_info = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_info["id"],
            "iscrowd": 1,
            "area": area.tolist(),
            "bbox": bounding_box.tolist(),
            "segmentation": binary_mask_to_rle(binary_mask),
            "width": binary_mask.shape[1],
            "height": binary_mask.shape[0],
        } 
    else:
        annotation_info = {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": category_info["id"],
            "iscrowd": 0,
            "area": area.tolist(),
            "bbox": bounding_box.tolist(),
            "segmentation": binary_mask_to_polygon(binary_mask),
            "width": binary_mask.shape[1],
            "height": binary_mask.shape[0]
        }

    return annotation_info
