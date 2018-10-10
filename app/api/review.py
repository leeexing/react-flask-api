# -*- coding: utf-8 -*-
"""歌手api"""
import requests
import re
from flask import Blueprint
from bs4 import BeautifulSoup
from ..util import ResponseHelper
from ..conf import headers

api_review = Blueprint('reivew', __name__)

reg_num = re.compile(r'\d+')

@api_review.route('/review/<review_type>')
def get_review_data(review_type='latest'):
    """豆瓣最受欢迎的乐评"""
    url = 'https://music.douban.com/review/{}?app_name=music'.format(review_type)
    music_crawler_content = requests.get(url, headers=headers).content
    music_crawler_soup = BeautifulSoup(music_crawler_content, 'lxml')
    data = []
    # music_crawler = music_crawler_soup.select('.article')[0]
    music_crawler = music_crawler_soup.find('div', class_='article')
    # !乐评类型
    for item in music_crawler.select('.review-list > div'):
        obj = {
            'id': int(reg_num.findall(item.select('.subject-img')[0].get('href'))[0]),
            'albumCover': item.select('.subject-img img')[0].get('src'),
            'albumName': item.select('.subject-img img')[0].get('title'),
            'avatar': item.select('.avator img')[0].get('src'),
            'name': item.select('.name')[0].get_text(),
            'stars': item.select('.main-title-rating')[0].get('class')[0],
            'time': item.select('.main-meta')[0].get_text(),
            'title': item.select('.main-bd h2')[0].get_text(),
            'shortContent': item.select('.short-content a')[0].previous_sibling[:-1].strip(),
            'up': 0 if not item.select('.up span')[0].get_text().strip() else int(item.select('.up span')[0].get_text().strip()),
            'down': 0 if not item.select('.up span')[0].get_text().strip() else int(item.select('.up span')[0].get_text().strip()),
            'reply': int(reg_num.findall(item.select('.reply')[0].get_text())[0]),
        }
        data.append(obj)
    return ResponseHelper.return_true_data(data=data)