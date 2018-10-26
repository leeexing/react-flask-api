# -*- coding: utf-8 -*-
"""首页api"""
from flask import Blueprint, jsonify
import requests, re, json
from bs4 import BeautifulSoup
from ..util import ResponseHelper
from ..conf import headers

api_home = Blueprint('home', __name__)
reg = re.compile(r'React\.render\(React.createElement\(component,(.*)\), \$el\[0\]\);')

def get_home_hotsongs(src):
    """本周单曲榜
        - 这里的数据是后面渲染出来的。爬虫的时候获取不到
        * 查看了网络请求，发现有三个部分的数据是通过 react js渲染出来的。数据似乎是后台直接就组装好了的
        * 这里直接就是获取对应的js，然后提取出相关的数据出来
    """
    music_data = requests.get(src)
    music_data.encoding = 'utf-8'
    js_text = music_data.text
    reg_data = reg.findall(js_text)
    react_data = [json.loads(item) for item in reg_data]
    data = {
        'newAlbumList': react_data[0],
        'hotProgramme': react_data[1],
        # 'weekTop10': react_data[2], #-豆瓣那边更改后，只返回两个。估计后面还有可能修改
    }
    return data

@api_home.route('/home')
def get_home_page():
    """获取首页相关数据"""

    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')

    # !总数据
    data = {
        'bannerImgs': [],
        'popularArtists': [],
        'newArtists': [],
        'editorFeatureSongs': [],
        'joinInfo': [],
        'doubanMusic250': [],
        'weekTop10': []
    }

    hot_song_src = [item.get('src') for item in soup.select('script') if item.get('src') and 'mixed_static' in item.get('src')][0]
    hot_song_data = get_home_hotsongs(hot_song_src)
    data = dict(data, **hot_song_data)
    # !本周单曲榜
    js_text_arr = [item.get_text() for item in soup.select('script') if item.get_text() and 'React.createElement' in item.get_text()]
    if len(js_text_arr):
        js_text = js_text_arr[0]
        reg_data = reg.findall(js_text)
        react_data = [json.loads(item) for item in reg_data][0]
        data['weekTop10'] = react_data
        # print(react_data)
    # print(data)

    # ^左侧数据获取
    # !banner轮播图
    banner_imgs = soup.select('.top-banner img')
    for img in banner_imgs:
        img_src = img.get('src')
        data['bannerImgs'].append(img_src)
    # !本周流行音乐人
    top_artists = soup.select('.artists .artist-item')
    for artist in top_artists:
        obj = {
            'name': artist.select('.title')[0].get_text(),
            'type': artist.select('.genre')[0].get_text(),
            'artistPhotoImg': 'https://images.weserv.nl/?url=' + re.match(".*\('(http.*)'\)",
                artist.select('.artist-photo-img')[0].get('style')).groups()[0][8:],
            'hoverTexts': [item.get_text() for item in artist.select('.hoverlay p')]
        }
        data['popularArtists'].append(obj)
    # !上升最快音乐人
    new_artists = soup.select('.new-artists .artist-item')
    for new_artist in new_artists:
        obj = {
            'name': new_artist.select('.title')[0].get_text(),
            'type': new_artist.select('.genre')[0].get_text(),
            'artistPhotoImg': 'https://images.weserv.nl/?url=' + re.match(".*\('(http.*)'\)",
                new_artist.select('.artist-photo-img')[0].get('style')).groups()[0][8:],
            'hoverTexts': [item.get_text() for item in new_artist.select('.hoverlay p')]
        }
        data['newArtists'].append(obj)
    # !编辑推荐
    feature_items = soup.select('.feature-item')
    for item in feature_items:
        obj = {
            'cover': 'https://images.weserv.nl/?url=' + re.match(".*\((http.*)\)", \
                item.select('.cover')[0].get('style')).groups()[0][8:],
            'type': item.select('> p')[0].get_text(),
            'name': item.select('.primary-link')[0].get_text(),
            'focus': item.select('h4')[0].get_text(),
            'detail': item.select('> p')[1].get_text(),
        }
        data['editorFeatureSongs'].append(obj)

    # ^右侧数据获取
    # !我要加入
    joins = soup.select('.join-block')
    for join in joins:
        obj = {
            'typeName': join.select('p')[0].get_text(),
            'endValue': int(join.select('a')[0].get_text()),
        }
        data['joinInfo'].append(obj)
    # !豆瓣音乐250
    hot_songs = soup.select('#music_rec dl')
    for hot_song in hot_songs:
        obj = {
            'cover': hot_song.select('img')[0].get('src'),
            'name': hot_song.select('dd')[0].get_text(),
        }
        data['doubanMusic250'].append(obj)

    # !返回数据
    return ResponseHelper.return_true_data(data=data)
