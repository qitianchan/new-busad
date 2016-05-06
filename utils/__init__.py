# -*- coding: utf-8 -*-
from random import Random
from flask import jsonify


def create_salt():
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(32):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt


def make_response(status_code, message='success', data=None):
    response = jsonify(message=message, data=data)
    response.status_code = status_code
    return response
