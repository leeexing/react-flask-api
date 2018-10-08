# -*- coding: utf-8 -*-
import requests
import re
from flask import Blueprint
from bs4 import BeautifulSoup
from ..util import ResponseHelper
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
                'number': int(reg_num.findall(tag.select('b')[0].get_text())[0])
            }
            obj['content'].append(tag_obj)
        data.append(obj)
    # print(data)
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
            'number': int(reg_num.findall(tag.select('b')[0].get_text())[0])
        }
        data.append(tag_obj)
    return ResponseHelper.return_true_data(data=data)

@api_tag.route('/tag/<tag_name>')
def get_tag_detail_data(tag_name=None):
    """所有热门标签"""
    print(tag_name, '9999')
    url = 'https://music.douban.com/tag/{}'.format(tag_name)
    music_tag_content = requests.get(url, headers=headers).content
    music_tag_soup = BeautifulSoup(music_tag_content, 'lxml')
    data = []
    music_tag_detail = music_tag_soup.select('.article table')
    for tag in music_tag_detail:
        tag_obj = {
            'name': tag.select('.nbg img')[0].get('src'),
            'title': tag.select('.pl2 a')[0].get_text(),
            'author': tag.select('.pl2 p')[0].get_text(),
            'score': tag.select('.pl2 .rating_nums')[0].get_text(),
            'people': int(reg_num.findall(tag.select('.pl2 .pl')[1].get_text())[0])
        }
        data.append(tag_obj)
    return ResponseHelper.return_true_data(data=data)
