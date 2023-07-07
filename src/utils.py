from hashlib import sha256, md5


def hash_password(password):
    hash_pass = sha256(password.encode('utf-8'))
    hex_dig = hash_pass.hexdigest()
    return hex_dig


def hash_image_name(filename):
    hash_filename = md5(filename.encode('utf-8'))
    hex_dig = hash_filename.hexdigest()
    return hex_dig + ".jpg"
