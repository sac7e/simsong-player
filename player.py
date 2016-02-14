from flask import Flask, request, render_template
import requests
import xmltodict
from urllib.parse import unquote


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/wangyi/<id>')
def wangyi(id):

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    }

    url = 'http://music.163.com/api/song/detail?ids=[' + id + ']'

    try:
        r = requests.get(url,headers=headers)
    except:
        return "no"

    info = r.json()
    resolved_url=info['songs'][0].get('mp3Url').replace('http://m','http://p')

    return render_template('wangyi.html', resolved_url=resolved_url)


def xiami_resolve(location):
    num = int(location[0])
    avg_len, remainder = int(len(location[1:]) / num), int(len(location[1:]) % num)
    result = [location[i * (avg_len + 1) + 1: (i + 1) * (avg_len + 1) + 1] for i in range(remainder)]
    result.extend([location[(avg_len + 1) * remainder:][i * avg_len + 1: (i + 1) * avg_len + 1]
                   for i in range(num-remainder)])
    url = unquote(''.join([''.join([result[j][i] for j in range(num)]) for i in range(avg_len)]) +
                         ''.join([result[r][-1] for r in range(remainder)])).replace('^','0')
    return url


@app.route('/xiami/<id>')
def xiami(id):
    url = 'http://www.xiami.com/song/playlist/id/' + id
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
    'Referer': url}

    status = 1
    try:
        r = requests.get(url,headers=headers)
        r.encode='uft-8'
    except:
        return "no"

    info = xmltodict.parse(r.text)
    resolved_url=xiami_resolve(info['playlist']['trackList']['track'].get('location'))

    return render_template('xiami.html', resolved_url=resolved_url)






if __name__ == '__main__':
    app.run()
