# -*- coding: utf-8 -*-
import requests
from flask import Blueprint, request
from flask_restplus import Namespace, Resource
from app.fields import tag_detail_field
from bs4 import BeautifulSoup
from ..util import ResponseHelper, extractDigitFromStr
from ..conf import headers

api_tag = Blueprint('tag', __name__)
ns = Namespace('tags', description='豆瓣音乐--标签')
tag_detail_model = ns.model('tagDetail', tag_detail_field)

@api_tag.route('/tags')
def get_tags_data():
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
def get_tag_cloud():
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

@api_tag.route('/tags/<tag_name>/related')
def get_tag_related(tag_name=None):
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

@api_tag.route('/tags/<tag_name>')
def get_tag_detail(tag_name=None):
    """豆瓣音乐标签:<tagName>"""
    query = request.args
    if not query:
        query = request.get_json()
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


@ns.route('')
class Tags(Resource):

    def get(self):
        """分类浏览"""
        return get_tags_data()


@ns.route('/cloud')
class TagsCloud(Resource):

    def get(self):
        """所有热门标签"""
        return get_tag_cloud()


@ns.route('/<tag_name>')
class TagDetail(Resource):

    @ns.expect(tag_detail_model)
    def post(self, tag_name=None):
        """具体标签详情"""
        return get_tag_detail(tag_name)

@ns.route('/<tag_name>/related')
class TagRelated(Resource):

    def get(self, tag_name=None):
        """获取该标签相关联的标签"""
        return get_tag_related(tag_name)