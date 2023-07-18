from hashlib import sha256, md5
from colorthief import ColorThief
from PIL import Image


def hash_password(password):
    hash_pass = sha256(password.encode('utf-8'))
    hex_dig = hash_pass.hexdigest()
    return hex_dig


def hash_image_name(filename):
    hash_filename = md5(filename.encode('utf-8'))
    hex_dig = hash_filename.hexdigest()
    return hex_dig + ".jpg"


def createProfileBackground(image):
    color = findDominantColor(image)
    height = 200
    width = 800
    background_image = Image.new(mode="RGB", size=(width, height), color=color)
    return background_image


def findDominantColor(image):
    ct = ColorThief(image)
    dominant_color = ct.get_color(quality=1)
    print(str(type(dominant_color)))
    return dominant_color

