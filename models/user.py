# -*- coding: utf-8 -*-
from flask import g
from wtforms.validators import Email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from extentions import db,bcrypt
from sqlalchemy import and_
# from server.app.main import app
from hashlib import sha1
from utils import create_salt

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.SmallInteger, default=1)                               # 超级管理员：0， 管理员：1， 一般员工：2
    status = db.Column(db.SmallInteger, default=1)                             # 0 不可以， 1 可用
    phone = db.Column(db.String(128))
    company_name = db.Column(db.String(128))
    token = db.Column(db.String(128))
    salt = db.Column(db.String(32), nullable=False)
    # progress_code = db.Column(db.String(128))                                  # redis记录进度标识码

    def __init__(self, username, password, salt=None):

        self.username = username
        if not salt:
            salt = create_salt()
        self.salt = salt
        sha1_obj = sha1()
        sha1_obj.update((password+salt).encode('utf-8'))
        self.password = sha1_obj.hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python

    @classmethod
    def get(cls, user_id):
        user_id = int(user_id)
        return cls.query.filter(User.id == user_id).first()

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false"""

        if self.password is None:
            return False

        sha1_obj = sha1()
        sha1_obj.update(password+self.salt)

        return self.password == sha1_obj.hexdigest()

    @classmethod
    def create_user(cls, username, password):
        user = User(username=username, password=password)
        return user.save()

    @classmethod
    def authenticate(cls, login, password):
        """A classmethod for authenticating users
        It returns true if the user exists and has entered a correct password

        :param login: This can be either a username or a email address.

        :param password: The password that is connected to username and email.
        """

        user = cls.query.filter_by(username=login).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False
        return user, authenticated

    def save(self):
        """
        Saves a user and return a user object.
        :param username: user name
        :param wechat_id: wechat id
        :param telephone:
        :param mobile_phone:
        :return:
        """

        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return self

    def delete(self):
        """
        delete a user
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_user(self, user_id):
        return User.query.filter_by(id=user_id).first()


    @classmethod
    def get_user_by_name(cls, username):
        return cls.query.filter(User.username == username).first()

