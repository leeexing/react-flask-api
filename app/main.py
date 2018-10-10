# -*- coding: utf-8 -*-
"""主文件"""
from flask import Flask, Blueprint
from flask_cors import CORS
from app.api import api_home, api_artists, api_topic, api_tag, api_subject, api_review

def create_app():
    """创建基础app"""
    app = Flask('react-flask-api')
    CORS(app)
    bind_api_route(app)
    return app
    
def bind_api_route(app):
    """绑定api的路由"""
    app.register_blueprint(api_home, url_prefix='/api')
    app.register_blueprint(api_artists, url_prefix='/api')
    app.register_blueprint(api_topic, url_prefix='/api')
    app.register_blueprint(api_tag, url_prefix='/api')
    app.register_blueprint(api_subject, url_prefix='/api')
    app.register_blueprint(api_review, url_prefix='/api')