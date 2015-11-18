import logging
import glob
import os
from PIL import Image

logging.debug(__file__ + ' imported')

field_images = []

for file in glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), '*.png')):
    try:
        field_images.append(Image.open(file))
    except IOError as e:
        logging.warning(e)
