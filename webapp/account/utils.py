from flask import current_app
from PIL import Image

import os
import secrets


def save_image(image):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(image.filename)
    image_file = random_hex + file_extension

    i = Image.open(image)
    i.save(os.path.join(current_app.root_path, 'static\images', image_file))
    i.thumbnail(100,100)
    i.save(os.path.join(current_app.root_path, 'static\images_preview', image_file))

    return image_file

def save_file(file):
    file.save