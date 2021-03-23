from pathlib import Path
import json

from PIL import Image
import numpy as np

from pycococreatortools import pycococreatortools

SAMPLE_IMAGE_PATH = Path(__file__).parent / "sample.png"
assert SAMPLE_IMAGE_PATH.exists()

raw_image_bitmask = Image.open(SAMPLE_IMAGE_PATH)
image_bitmask = np.asarray(raw_image_bitmask.convert("1")).astype(np.uint8)

annotation_infos = pycococreatortools.create_annotation_infos(
    1, 1, {"id": 1}, image_bitmask, raw_image_bitmask.size, tolerance=2, connectivity=1
)

print(f"Found {len(annotation_infos)} annotations in the image:")
print(json.dumps(annotation_infos, indent=4))
