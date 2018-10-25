# -*- coding: utf-8 -*-
"""api主文件"""
from flask_restplus import Api
from .home import api_home
from .artists import api_artists
from .topic import api_topic
from .tag import api_tag
from .subject import api_subject
from .review import api_review
from .songlist import api_songlist

from .detail import ns as detail_api
from .topic import ns as topic_api

api = Api(
    title='Douban Music API',
    version='1.0',
    prefix='/v1/api',
    description='Douban Music API for react-flask project!',
)
api.add_namespace(detail_api)
api.add_namespace(topic_api)
