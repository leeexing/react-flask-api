# -*- coding: utf-8 -*-
"""歌手api"""
from flask import Blueprint

api_artists = Blueprint('artists', __name__)

@api_artists.route('/artists')
def artists_api():
    """歌手"""
    return 'artists api'
