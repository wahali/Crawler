import requests
import parsel
import pprint

"""
样例网址：https://www.ximalaya.com/waiyu/16301603/
爬取对应一业的所有的音频
"""
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/79.0.3945.88 Safari/537.36 '
# }
# # 获得某一页的所有音频 title 和 url
# response = requests.get('https://www.ximalaya.com/waiyu/16301603/', headers=headers)
# # print(response.status_code)
# sel = parsel.Selector(response.text)
# url_s = sel.css('.sound-list  ul ._Vc a')
# for a in url_s:
#     title = a.css('a::attr(title)').get()
#     url = a.css('a::attr(href)').get()
#     title = title.split('.')[-1]
#     print(title, url)
#
#     # # 标题和url获得标题对应的下载地址
#     # with open(' /i/ — sit 坐.m4a', 'wb') as f:
#     response = requests.get('https://fdfs.xmcdn.com/group45/M01/92/C0/wKgKjls_GxXh6C6SAABZ3KYjE4g228.m4a',
#                             headers=headers)
# #     f.write(response.content)

"""
下载一个音频
"""


def download_media(media_name, media_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36 '
    }
    response = requests.get(media_url, headers=headers)
    with open(media_name + '.mp3', 'wb') as fp:
        fp.write(response.content)


# 获得media真实的地址
def get_media_url_api(id_):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36 '
    }
    api_url = 'https://www.ximalaya.com/revision/play/v1/audio?id=' + str(id_) + '&ptype=1'
    response = requests.get(api_url, headers=headers)
    data = response.json()
    src = data['data']['src']
    return src


"""
获得标题和id
传入参数为网址
"""


def get_media_title_id_and_download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    sel = parsel.Selector(response.text)
    url_s = sel.css('.sound-list  ul ._Vc a')
    for a in url_s:
        title = a.css('a::attr(title)').get()
        id_ = a.css('a::attr(href)').get()
        title = title.split('.')[-1]
        title = title.replace('/', ' ')
        id_ = id_.split('/')[-1]
        # print(title, id_)
        download_media(title, get_media_url_api(id_))


get_media_title_id_and_download('https://www.ximalaya.com/waiyu/16301603/')
get_media_title_id_and_download('https://www.ximalaya.com/waiyu/16301603/p2/')
