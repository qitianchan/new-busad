# -*- coding: utf-8 -*-
import os
_basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'busad.sqlite')

    # used in flask-login
    SECRET_KEY = '5b481368a8f69bc0df35b57e5a2775bb746be181274ef26947c3400fb9beb50326e4b3eb58627df9a75187a5d74d17c8b92e'
    # used in flask-wtf
    WTF_CSRF_SECRET_KEY = '5b481368a8f69bc0df35b57e5a2775bb746be181274ef26947c3400fb9beb50326e4b3eb58627df9a75187a5d74d17c8b92e'