# -*- coding: utf-8 -*-
import requests
import re
from flask import Blueprint, request
from bs4 import BeautifulSoup
from ..util import ResponseHelper, extractDigitFromStr
from ..conf import headers

api_tag = Blueprint('tag', __name__)

reg_num = re.compile(r'\d+')

@api_tag.route('/tags')
def get_tag_data():
    """分类浏览"""
    music_tag_content = requests.get('https://music.douban.com/tag/', headers=headers).content
    music_tag_soup = BeautifulSoup(music_tag_content, 'lxml')
    data = []
    music_tag_mods = music_tag_soup.select('.mod')
    for mod in music_tag_mods:
        obj = {
            'title': mod.select('h2')[0].get_text(),
            'content': []
        }
        tags = mod.select('td')
        for tag in tags:
            tag_obj = {
                'name': tag.select('a')[0].get_text(),
                'number': extractDigitFromStr(tag.select('b')[0].get_text())
            }
            obj['content'].append(tag_obj)
        data.append(obj)
    return ResponseHelper.return_true_data(data=data)

@api_tag.route('/tags/cloud')
def get_tag_cloud_data():
    """所有热门标签"""
    music_tag_content = requests.get('https://music.douban.com/tag/?view=cloud', headers=headers).content
    music_tag_soup = BeautifulSoup(music_tag_content, 'lxml')
    data = []
    music_tag_mods = music_tag_soup.select('.tagCol td')
    for tag in music_tag_mods:
        tag_obj = {
            'name': tag.select('a')[0].get_text(),
            'number': extractDigitFromStr(tag.select('b')[0].get_text())
        }
        data.append(tag_obj)
    return ResponseHelper.return_true_data(data=data)

@api_tag.route('/tag/<tag_name>/related')
def get_tag_link_data(tag_name=None):
    """相关的标签"""
    url = 'https://music.douban.com/tag/{}'.format(tag_name)
    music_tag_content = requests.get(url, headers=headers).content
    music_tag_soup = BeautifulSoup(music_tag_content, 'lxml')
    data = []
    music_tag_links = music_tag_soup.select('.aside .tags-list a')
    for link_tag in music_tag_links:
        tag_obj = {
            'href': link_tag.get('href'),
            'tagName': link_tag.get_text(),
        }
        data.append(tag_obj)
    return ResponseHelper.return_true_data(data=data)

@api_tag.route('/tag/<tag_name>')
def get_tag_detail_data(tag_name=None):
    """豆瓣音乐标签:<tagName>"""
    query = request.args
    queryType = query.get('type', 'T')
    start = query.get('start', 0)
    url = 'https://music.douban.com/tag/{}?start={}&type={}'.format(tag_name, start, queryType)
    music_tag_content = requests.get(url, headers=headers).content
    music_tag_soup = BeautifulSoup(music_tag_content, 'lxml')
    data = {
        'detailItems': []
    }
    music_tag_detail = music_tag_soup.select('.article table')
    for tag in music_tag_detail:
        tag_obj = {
            'href': tag.select('.nbg')[0].get('href'),
            'subjectId': extractDigitFromStr(tag.select('.nbg')[0].get('href')),
            'avatar': tag.select('.nbg img')[0].get('src'),
            'title': tag.select('.pl2 a')[0].get_text().strip().split('\n')[0],
            'subTitle': tag.select('.pl2 a span')[0].get_text() if tag.select('.pl2 a span') else None,
            'author': tag.select('.pl2 p')[0].get_text(),
            'stars': extractDigitFromStr(tag.select('.star span')[0].get('class')[0]) / 10,
            'score': tag.select('.pl2 .rating_nums')[0].get_text(),
            'peopleNum': extractDigitFromStr(tag.select('.pl2 .pl')[1].get_text()),
        }
        data['detailItems'].append(tag_obj)
    data['total'] = int(music_tag_soup.select('.paginator > a')[-1].get_text()) * 10
    return ResponseHelper.return_true_data(data=data)
