from flask import Flask, jsonify
import requests, re, json
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'host': 'music.douban.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.jianshu.com/p/410e0a3c28cd',
    'Upgrade-Insecure-Requests': '1'
}

@app.route('/api/home')
def get_home_data():
    """获取首页相关数据"""

    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')

    # ^左侧数据获取
    # !banner轮播图
    banner_imgs = soup.select('.top-banner img')
    data = {
        'bannerImgs': [],
        'popularArtists': [],
        'editorFeatureSongs': [],
        'joinInfo': [],
        'doubanMusic250': [],
    }
    for img in banner_imgs:
        img_src = img.get('src')
        data['bannerImgs'].append(img_src)
    # !本周流行音乐人
    top_artists = soup.select('.artists .artist-item')
    for artist in top_artists:
        obj = {
            'name': artist.select('.title')[0].get_text(),
            'type': artist.select('.genre')[0].get_text(),
            'artistPhotoImg': 'https://images.weserv.nl/?url=' + re.match(".*\('(http.*)'\)", artist.select('.artist-photo-img')[0].get('style')).groups()[0][8:],
            'hoverTexts': [item.get_text() for item in artist.select('.hoverlay p')]
        }
        data['popularArtists'].append(obj)
    # !编辑推荐
    feature_items = soup.select('.feature-item')
    for item in feature_items:
        obj = {
            'cover': 'https://images.weserv.nl/?url=' + re.match(".*\((http.*)\)", item.select('.cover')[0].get('style')).groups()[0][8:],
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
    return jsonify(data)

@app.route('/api/home/reactData')
def get_home_react_data():
    """本周单曲榜
        - 这里的数据是后面渲染出来的。爬虫的时候获取不到
        * 查看了网络请求，发现有三个部分的数据是通过 react js渲染出来的。数据似乎是后台直接就组装好了的
        * 这里直接就是获取对应的js，然后提取出相关的数据出来
    """
    music_data = requests.get('https://img3.doubanio.com/misc/mixed_static/e2291d495c46b31.js')
    music_data.encoding = 'utf-8'
    music_text = music_data.text
    # print(music_text)
    reg = re.compile(r'React\.render\(React.createElement\(component,(.*)\), \$el\[0\]\);')
    reg_data = reg.findall(music_text)
    # print(reg_data)
    data = {
        'reactRenderData': [json.loads(item) for item in reg_data]
    }
    return jsonify(data)

@app.route('/topBanner')
def get_banner_imgs():
    """获取顶部banner轮播图"""
    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')
    banner_imgs = soup.select('.top-banner img')
    data = {
        'imgList': []
    }
    for img in banner_imgs:
        img_src = img.get('src')
        data['imgList'].append(img_src)
    return jsonify(data)

@app.route('/popularArtist')
def popular_artist():
    """本周流行音乐人
        - 图片地址前面 添加'https://images.weserv.nl/?url=' 替换之前的 https:// 是解决豆瓣限制图片加载的问题。就是加了一个图片缓存
        * 参考 [https://blog.csdn.net/jsyxiaoba/article/details/79628983]
    """
    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')
    top_artists = soup.select('.artists .artist-item')
    data = {
        'topArtists': []
    }
    for artist in top_artists:
        obj = {
            'name': artist.select('.title')[0].get_text(),
            'type': artist.select('.genre')[0].get_text(),
            'artistPhotoImg': 'https://images.weserv.nl/?url=' + re.match(".*\('(http.*)'\)", artist.select('.artist-photo-img')[0].get('style')).groups()[0][8:],
            'hoverTexts': [item.get_text() for item in artist.select('.hoverlay p')]
        }
        data['topArtists'].append(obj)
    return jsonify(data)

@app.route('/editorFeature')
def editor_feature():
    """编辑推荐"""
    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')
    feature_items = soup.select('.feature-item')
    data = {
        'editorFeatureSongs': []
    }
    for item in feature_items:
        obj = {
            'cover': 'https://images.weserv.nl/?url=' + re.match(".*\((http.*)\)", item.select('.cover')[0].get('style')).groups()[0][8:],
            'type': item.select('> p')[0].get_text(),
            'name': item.select('.primary-link')[0].get_text(),
            'focus': item.select('h4')[0].get_text(),
            'detail': item.select('> p')[1].get_text(),
        }
        data['editorFeatureSongs'].append(obj)
    return jsonify(data)

@app.route('/joinInfo')
def join_info():
    """加入我们"""
    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')
    joins = soup.select('.join-block')
    data = {
        'joinInfo': []
    }
    for join in joins:
        obj = {
            'typeName': join.select('p')[0].get_text(),
            'endValue': int(join.select('a')[0].get_text()),
        }
        data['joinInfo'].append(obj)
    return jsonify(data)

@app.route('/douban250')
def douban_songs():
    """豆瓣音乐250"""
    music_data = requests.get('https://music.douban.com/', headers=headers).content
    soup = BeautifulSoup(music_data, 'lxml')
    hot_songs = soup.select('#music_rec dl')
    data = {
        'douban250': []
    }
    for hot_song in hot_songs:
        obj = {
            'cover': hot_song.select('img')[0].get('src'),
            'name': hot_song.select('dd')[0].get_text(),
        }
        data['douban250'].append(obj)
    return jsonify(data)

@app.route('/reactRenderData')
def hot_artist_songs():
    """本周单曲榜
        - 这里的数据是后面渲染出来的。爬虫的时候获取不到
        * 查看了网络请求，发现有三个部分的数据是通过 react js渲染出来的。数据似乎是后台直接就组装好了的
        * 这里直接就是获取对应的js，然后提取出相关的数据出来
    """
    music_data = requests.get('https://img3.doubanio.com/misc/mixed_static/e2291d495c46b31.js')
    music_data.encoding = 'utf-8'
    js_text = music_data.text
    # print(js_text)
    reg = re.compile(r'React\.render\(React.createElement\(component,(.*)\), \$el\[0\]\);')
    reg_data = reg.findall(js_text)
    # print(reg_data)
    data = {
        'reactRenderData': [json.loads(item) for item in reg_data]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=7012, debug=True)
