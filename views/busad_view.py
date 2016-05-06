# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

busad_blueprint = Blueprint('busad', __name__)


@busad_blueprint.route('/', methods=['GET'])
def upload():
    return render_template('upload.html')