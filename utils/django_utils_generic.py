import os
from datetime import datetime
import string
import random


def random_string(length=4):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_upload_path(instance, filename):
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    timestamp = datetime.now().strftime("%Y/%m/%d")
    new_filename = f"{random_chars}.jpg"
    return os.path.join('products', 'covers', timestamp, new_filename)
