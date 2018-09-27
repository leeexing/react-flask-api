# -*- coding: utf-8 -*-
"""登录/注册"""
from flask import Blueprint

api_login = Blueprint('login', __name__)

@api_login.route('/login', methods=['post'])
def login():
    """login"""
    return 'login api ...'

