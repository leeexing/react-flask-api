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
from .chart import api_chart

# !swagger
from .detail import ns as detail_api
from .topic import ns as topic_api
from .artists import ns as artists_api
from .tag import ns as tag_api
from .home import ns as home_api

api = Api(
    title='Douban Music API',
    version='1.0',
    prefix='/v1/api',
    description='Douban Music API for react-flask project!',
)
api.add_namespace(home_api)
api.add_namespace(detail_api)
api.add_namespace(topic_api)
api.add_namespace(artists_api)
api.add_namespace(tag_api)
