import requests
import parsel
import pprint
import os

"""
2020/2/8
url:https://www.yinbiao5.com
通过url，下载对应的序号，单词，音标和翻译
存储到对应的文件夹下
"""


def get_txt_by_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    sel = parsel.Selector(response.text)
    tem = sel.css('b')
    if tem.css('b::text').get() == '抱歉！您输入的网址不存在。':
        return
    tem = sel.css('.dic_c a')
    """
    获得对应书目信息
    """
    form = ""
    edition = ""
    grade = ""
    unit = ""
    cnt = 1
    for a in tem:
        text = a.css('a::attr(title)').get()
        if cnt == 1:
            form = text
        elif cnt == 2:
            edition = text
        elif cnt == 3:
            grade = text
        elif cnt == 4:
            unit = text
        cnt = cnt + 1
    """
    获得单词内容
    """
    filepath = 'yinbiao5.com/' + form + '/' + edition + '/' + grade
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open('yinbiao5.com/' + form + '/' + edition + '/' + grade + '/' + unit + '.txt', 'w', encoding='utf-8') as fp:
        tem = sel.css('.dic_table tr')
        for a in tem:
            td = a.css('span::text').getall()
            if len(td):
                fp.write(' '.join(td))
                fp.write('\n')
            # print(td)


# get_txt_by_url('https://www.yinbiao5.com/22-1010111-0.html')


"""
2020/2/8
遍历url，获取所有的词库
"""


def get_all_words():
    # for i in range(1010101, 3510322):
    #     get_txt_by_url('https://www.yinbiao5.com/22-' + str(i) + '-0.html')
    num = ''
    for i in range(1, 6):
        for j in range(1, 8):
            for k in range(1, 9):
                num = '10' + str(i) + '0' + str(j) + '0' + str(k)
                get_txt_by_url('https://www.yinbiao5.com/22-' + num + '-0.html')
            for k in range(10, 99):
                num = '10' + str(i) + '0' + str(j) + str(k)
                get_txt_by_url('https://www.yinbiao5.com/22-' + num + '-0.html')

    for j in range(1, 5):
        for k in range(1, 9):
            num = '201' + '0' + str(j) + '0' + str(k)
            get_txt_by_url('https://www.yinbiao5.com/22-' + num + '-0.html')
        for k in range(10, 20):
            num = '201' + '0' + str(j) + str(k)
            get_txt_by_url('https://www.yinbiao5.com/22-' + num + '-0.html')

    for j in range(1, 6):
        for k in range(1, 9):
            num = '3010' + str(j) + '0' + str(k)
            get_txt_by_url('https://www.yinbiao5.com/22-' + num + '-0.html')
        for k in range(10, 99):
            num = '3010' + str(j) + str(k)
            get_txt_by_url('https://www.yinbiao5.com/22-' + num + '-0.html')


get_all_words()
