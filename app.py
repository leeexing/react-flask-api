from flask import Flask
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    num = 3
    name = '王菲'
    urlString = '''http://s.music.qq.com/fcgi-bin/music_search_new_platform?
                  t=0&n={}&aggr=1&cr=1&loginUin=0&format=json&inCharset=GB2312&
                  outCharset=utf-8&notice=0&platform=jqminiframe.json&needNewCode=0&p=1&
                  catZhida=0&remoteplace=sizer.newclient.next_song&w={}'''.format(num, name)
    print(urlString)
    # data = requests.get('https://api.github.com/events').json()
    data = requests.get(urlString).json()
    print(data)
    return 'hello, react'

@app.route('/list', methods=['POST'])
def getMusicList():

    postData = {
        "TransCode": "020112",
        "OpenId": "123456789",
        "Body": {
            "SongListId": "141998290"
        }
    }
    data = requests.post('https://api.hibai.cn/api/index/index', postData).json()
    print(data)
    return 'welcome, react'


if __name__ == '__main__':
    app.run(port=7012, debug=True)
