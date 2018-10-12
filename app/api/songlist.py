# -*- coding: utf-8 -*-
"""歌手api"""
import requests
import re
import json
from flask import Blueprint
from bs4 import BeautifulSoup
from ..util import ResponseHelper
from ..conf import headers

api_songlist = Blueprint('songlist', __name__)

headers['host'] = 'douban.fm'

reg_num = re.compile(r'\d+')

@api_songlist.route('/songlist/<genre_type>')
def get_review_data(genre_type='hot'):
    """豆瓣最受欢迎的乐评"""
    url = 'https://douban.fm/j/v2/songlist/explore?type=hot&genre={}&limit=20&sample_cnt=5'.format(genre_type)
    print(url)
    music_crawler_content = requests.get(url, headers=headers).content
    # music_crawler_soup = BeautifulSoup(music_crawler_content, 'lxml')
    # print(music_crawler_content)
    data = json.loads(music_crawler_content)
    # music_crawler = music_crawler_soup.select('.article')[0]
    # music_crawler = music_crawler_soup.find('div', class_='article')
    # !乐评类型
    return ResponseHelper.return_true_data(data=data)
 