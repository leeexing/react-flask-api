# -*- coding: utf-8 -*-
"""歌手api"""
import requests
import re
import json
import copy
from flask import Blueprint
from bs4 import BeautifulSoup
from ..util import ResponseHelper
from ..conf import headers

api_songlist = Blueprint('songlist', __name__)

_headers = copy.copy(headers) # 不能直接修改headers，否则会影响全局的headers
# headers['host'] = 'douban.fm'
_headers['host'] = 'img3.doubanio.com'
_headers['Referer'] = 'https://artist.douban.com/abilu/2017/'

reg_num = re.compile(r'\d+')

@api_songlist.route('/songlist/<genre_type>')
def get_review_data(genre_type='hot'):
    """豆瓣最受欢迎的乐评"""
    url = 'https://douban.fm/j/v2/songlist/explore?type=hot&genre={}&limit=20&sample_cnt=5'.format(genre_type)
    music_crawler_content = requests.get(url, headers=_headers).content
    data = json.loads(music_crawler_content)
    return ResponseHelper.return_true_data(data=data)
 
@api_songlist.route('/abilu')
def get_abilu_data():
    """豆瓣最受欢迎的乐评"""
    url = 'https://artist.douban.com/abilu/2017/'
    music_crawler_content = requests.get(url, headers=_headers)
    data = []
    print(music_crawler_content)
    # data = json.loads(music_crawler_content)
    return ResponseHelper.return_true_data(data=data)
