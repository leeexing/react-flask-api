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
    print(data)
    return ResponseHelper.return_true_data(data=data)
