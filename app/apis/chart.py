# -*- coding: utf-8 -*-
"""排行榜
"""
import requests
from flask import Blueprint
from flask_restplus import Namespace, Resource
from bs4 import BeautifulSoup
from ..util import ResponseHelper, extractDigitFromStr
from ..conf import headers

api_chart = Blueprint('chart', __name__)
ns = Namespace('chart', decorators='乐评')

@api_chart.route('/chart')
def get_chart():
    """音乐排行榜"""
    print(9999)
    url = 'https://music.douban.com/chart'
    music_crawler_content = requests.get(url, headers=headers).content
    music_crawler_soup = BeautifulSoup(music_crawler_content, 'lxml')
    data = {
        'hotList': [],
        'newAlbum': [],
        'popMusician': [],
    }
    for item in music_crawler_soup.select('.article .clearfix'):
        obj = {
            # 'id': item.select('.intro h3')[0].get('data-sid'),
            'cover': item.select('.face img')[0].get('src') if item.select('.face img') else None,
            'href': item.select('.face')[0].get('href') if item.select('.face') else None,
            'title': item.select('.intro a')[0].get_text(),
            'infoText': item.select('.intro p')[0].get_text(),
            'days': item.select('.days')[0].get_text(),
            'trend': item.select('.trend')[0].get_text(),
            'trendArrow': item.select('.trend')[0].get('class')[1]
        }
        data['hotList'].append(obj)
    # 豆瓣新碟榜
    for item in music_crawler_soup.select('.aside .mod')[0].select('.clearfix'):
        obj = {
            'title': item.select('.entry a')[0].get_text(),
            'author': item.select('.entry a')[0].next_sibling.strip(),
            'info': item.select('.days')[0].get_text().strip()
        }
        data['newAlbum'].append(obj)
    # 本周流行音乐人
    for item in music_crawler_soup.select('.aside .mod')[1].select('.clearfix'):
        obj = {
            'cover': item.select('.face img')[0].get('src'),
            'author': item.select('.intro a')[0].get_text().strip(),
            'info': item.select('.intro p br')[0].previous_sibling.strip(),
            'focus': item.select('.intro p br')[0].next_sibling.strip(),
        }
        data['popMusician'].append(obj)
    return ResponseHelper.return_true_data(data=data)
