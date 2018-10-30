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
ns = Namespace('chart', description='音乐排行榜')

@api_chart.route('/chart')
def get_chart():
    """音乐排行榜"""
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
            'id': int(item.select('.intro .icon-play')[0].get('data-sid')),
            'cover': item.select('.face img')[0].get('src') if item.select('.face img') else None,
            'href': item.select('.face')[0].get('href') if item.select('.face') else None,
            'title': item.select('.intro a')[0].get_text(),
            'infoText': item.select('.intro p a')[0].next_sibling if item.select('.intro p a') else item.select('.intro p')[0].get_text(),
            'days': item.select('.days')[0].get_text(),
            'trend': int(item.select('.trend')[0].get_text().strip()),
            'trendArrow': item.select('.trend')[0].get('class')[1]
        }
        data['hotList'].append(obj)
    # 豆瓣新碟榜
    for item in music_crawler_soup.select('.aside .mod')[0].select('.clearfix'):
        obj = {
            'title': item.select('.entry a')[0].get_text(),
            'author': item.select('.entry a')[0].next_sibling.strip().replace('/', ''),
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


@ns.route('')
class Chart(Resource):

    def get(self):
        """豆瓣音乐排行榜"""
        return get_chart()