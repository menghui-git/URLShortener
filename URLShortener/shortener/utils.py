import base64
import hashlib
import random

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def is_url_valid(url):
    from shortener.models import URL

    if not url:
        return False, "Please enter an URL."
    if len(url) > URL.URL_MAX_LENGTH:
        return False, "The max length of URL is 200."
    validate = URLValidator()
    try:
        validate(url)
        return True, ""
    except ValidationError:
        return False, "Invalid format of URL."


def generate_random_code():
    while True:
        random_key = str(random.random())
        hash = hashlib.md5(random_key.encode('utf-8')).digest()[-5:]
        code = base64.b64encode(hash).decode('utf-8')
        for c in ('/', '=', '+'):
            code = code.replace(c, '')
        api_paths = ('shorten', )
        if code and code not in api_paths:
            return code
