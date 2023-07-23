from hashlib import sha256, md5
from colorthief import ColorThief
from PIL import Image
from datetime import datetime


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


def get_date():
    date = datetime.now()
    return str(date.day) + " " + str(date.month) + " " + str(date.year)


def get_date_with_hours():
    time = datetime.now()
    return time.strftime("%d.%m.%Y %H:%M")


def map_to_object(comment_tuple):
    comment = Comment(comment_tuple[0],
                      comment_tuple[1],
                      comment_tuple[2],
                      comment_tuple[3],
                      comment_tuple[4])
    return comment


class Comment:
    def __init__(self, comment_id, user_id, username, avatar, text):
        self.comment_id = comment_id
        self.user_id = user_id
        self.username = username
        self.avatar = "images/avatars/" + str(avatar)
        self.text = text


class Post:
    def __init__(self, user_id, username, usertag, avatar, post_id, title, date):
        self.user_id = user_id
        self.username = username
        self.usertag = usertag
        self.avatar = "images/avatars/" + avatar
        self.post_id = post_id
        self.title = title
        self.date = date


class Answear:
    def __init__(self, text, user_id, username, usertag, avatar):
        self.text = text
        self.user_id = user_id
        self.username = username
        self.usertag = usertag
        self.avatar = "images/avatars/" + str(avatar)


def create_youtube_player(link):
    return """<iframe
    width = '560'
    height = '315'
    src = 'https://www.youtube.com/embed/""" + link + """'
    title = 'YouTube video player'
    frameborder = '0'
    allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
    allowfullscreen></iframe>"""