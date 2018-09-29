# -*- coding: utf-8 -*-
"""专题"""
import requests
from flask import Blueprint, request
from bs4 import BeautifulSoup
from ..conf import headers
from ..util import ResponseHelper

api_topic = Blueprint('topic', __name__)

@api_topic.route('/topics')
def get_topics_data():
    """获取专题页面数据"""
    url = 'https://music.douban.com/topics/'
    music_topic_content = requests.get(url, headers=headers).content
    music_topic_soup = BeautifulSoup(music_topic_content, 'lxml')
    data = {
        'slideTrack': music_topic_soup.select('#banner-section img')[0].get('src'),
        'topics': []
    }
    topics = music_topic_soup.select('#topics .topic')
    for topic in topics:
        obj = {
            'cover': topic.select('img')[0].get('src'),
            'coverText': topic.select('h2')[0].get_text(),
            'topicInfo': topic.select('p')[0].get_text(),
            'topicTime': topic.select('.time')[0].get_text()
        }
        data['topics'].append(obj)
    return ResponseHelper.return_true_data(data=data)

@api_topic.route('/topic/more')
def get_topics_more():
    """获取更多的专题"""
    start = request.args.get('start')
    limit = request.args.get('limit')
    print(start, limit)
    url = 'https://music.douban.com/topics/tmpl?start={start}&limit={end}'.format(start=start, end=limit)
    music_topic_content = requests.get(url, headers=headers).content
    music_topic_soup = BeautifulSoup(music_topic_content, 'lxml')
    data = {
        'topicsMore': []
    }
    topics = music_topic_soup.select('.topic')
    for topic in topics:
        obj = {
            'cover': topic.select('img')[0].get('src'),
            'coverText': topic.select('h2')[0].get_text(),
            'topicInfo': topic.select('p')[0].get_text(),
            'topicTime': topic.select('.time')[0].get_text()
        }
        data['topicsMore'].append(obj)
    return ResponseHelper.return_true_data(data=data)