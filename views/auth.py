# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, url_for, abort
from forms.auth import LoginForm, RegisterForm
from models.user import User
from flask_login import login_user
from utils import make_response
from sqlalchemy.exc import IntegrityError
from jinja2 import TemplateNotFound

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            user, authenticated = User.authenticate(form.username.data,
                                                form.password.data)

            if user and authenticated:
                login_user(user, remember=form.remember_me.data)
                return url_for('map.devices_on_map')
            else:
                return make_response(422, message='Incorrect username or password.')

    return render_template('login.html', title='Sign In', form=form)


@auth_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # if form.validate_username():
            try:
                user = form.save()
            except IntegrityError as e:
                return make_response(422, message='User name is existed')
            login_user(user)
            return url_for('busad.upload')
    try:
        return render_template('register.html', title='Register', form=form)
    except TemplateNotFound:
        abort(404)
