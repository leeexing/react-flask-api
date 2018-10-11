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

@api_review.route('/review/detail/<review_id>')
def get_review_detail_data(review_id=None):
    """获取乐评的详情"""
    url = 'https://music.douban.com/review/{}'.format(review_id)
    music_crawler_content = requests.get(url, headers=headers).content
    music_crawler_soup = BeautifulSoup(music_crawler_content, 'lxml')
    data = {
        'paragraphList': [],
        'subjectInfo': []
    }
    data['title'] = music_crawler_soup.select('h1')[0].get_text()
    data['avatar'] = music_crawler_soup.select('.avatar img')[0].get('src')
    data['author'] = music_crawler_soup.select('.main-hd a')[0].select('span')[0].get_text()
    data['albumName'] = music_crawler_soup.select('.main-hd a')[1].get_text()
    data['stars'] = music_crawler_soup.select('.main-hd > span')[0].get('class')[0]
    data['reviewTime'] = music_crawler_soup.select('.main-hd > span')[2].get_text()
    data['subjectImgCover'] = music_crawler_soup.select('.subject-img img')[0].get('src')
    for item in music_crawler_soup.select('.review-content p'):
        data['paragraphList'].append(item.get_text().strip())
    for item in music_crawler_soup.select('.info-list li'):
        obj = {
            'key': item.select('.info-item-key')[0].get_text(),
            'val': item.select('.info-item-val')[0].get_text()
        }
        data['subjectInfo'].append(obj)
    return ResponseHelper.return_true_data(data=data)
