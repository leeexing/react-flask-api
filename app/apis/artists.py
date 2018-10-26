# -*- coding: utf-8 -*-
"""歌手api"""
import requests
from flask import Blueprint
from flask_restplus import Namespace, Resource
from bs4 import BeautifulSoup
from ..util import ResponseHelper, stripBlank, extractDigitFromStr
from ..conf import headers

ns = Namespace('artists', description='豆瓣音乐-音乐人')
api_artists = Blueprint('artists', __name__)

@api_artists.route('/artists')
def get_artists_data():
    """豆瓣音乐人列表"""
    music_crawler_content = requests.get('https://music.douban.com/artists/', headers=headers).content
    music_crawler_soup = BeautifulSoup(music_crawler_content, 'lxml')
    data = {
        'hotArtists': [],
        'artistsEvents': [],
        'artistsNotes': [],
        'artistsVideo': [],
        'generList': [], # 流派
        'hotStyle': [],
        'topArtistList': [],
        'hotAudioBlog': [],
        'hotBrand': [],
    }
    music_crawler = music_crawler_soup.select('.slide-page')
    # !热门音乐人
    for mod in music_crawler:
        for item in mod.select('li'):
            obj = {
                'cover': item.select('a img')[0].get('src'),
                'artist': item.select('span a')[0].get_text(),
                'href': item.select('span a')[0].get('href'),
                'isFleece': True if item.select('.icon-fleece-id') else False
            }
            data['hotArtists'].append(obj)
    # !推荐活动
    # print(data)
    for item in music_crawler_soup.select('#artists-events li'):
        obj = {
            'id': extractDigitFromStr(item.select('.pic a')[0].get('href')),
            'cover': item.select('.pic img')[0].get('src'),
            'artistName': item.select('.artist-name')[0].get_text(),
            'title': item.select('.title a')[0].get_text(),
            'desc': item.select('.desc')[0].get_text()
        }
        data['artistsEvents'].append(obj)
    # !流派
    for item in music_crawler_soup.select('.genre-nav li'):
        obj = {
            'pageId': extractDigitFromStr(item.select('a')[0].get('href')),
            'name': item.select('a')[0].get_text()
        }
        data['generList'].append(obj)
    # !风格
    for item in music_crawler_soup.select('#artists-tags .cloud1'):
        data['hotStyle'].append(item.select('a')[0].get_text())
    # !最受欢迎音乐人
    popularArtists = music_crawler_soup.find('div', attrs={'data-dstat-areaid':'129'}) # -比较新颖的查找方式
    for item in popularArtists.select('li'):
        obj = {
            'href': item.select('a')[0].get('href'),
            'albumName': item.select('a')[0].get_text(),
            'type': item.get_text().strip().split('/')[1]
        }
        data['topArtistList'].append(obj)
    # !最受欢迎博客
    hotAudioBlog = music_crawler_soup.find('div', attrs={'data-dstat-areaid':'131'})
    for item in hotAudioBlog.select('li'):
        obj = {
            'link': item.select('.pic a')[0].get('href'),
            'cover': item.select('.pic img')[0].get('src'),
            'name': item.select('.info a')[0].get_text(),
            'style': stripBlank(item.select('.info br')[0].next_sibling.strip(), 3) if item.select('.info br') else None,
        }
        data['hotAudioBlog'].append(obj)
    # !最受欢迎厂牌
    hotBrand = music_crawler_soup.find('div', attrs={'data-dstat-areaid':'132'})
    for item in hotBrand.select('li'):
        obj = {
            'link': item.select('.pic a')[0].get('href'),
            'cover': item.select('.pic img')[0].get('src'),
            'name': item.select('.info a')[0].get_text(),
            'style': stripBlank(item.select('.info br')[0].next_sibling.strip(), 3) if item.select('.info br') else None
        }
        data['hotBrand'].append(obj)
    return ResponseHelper.return_true_data(data=data)


@ns.route('')
class Artists(Resource):

    def get(self):
        """获取音乐人列表数据"""
        return get_artists_data()
