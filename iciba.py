import re
import csv
import requests
import parsel
import pprint
import uuid

"""
2020/3/12
已知单词，爬取iciba的单词相关内容，包括音标，中文解释，单词音频的访问地址
http://www.ichacha.net/zaoju 查询对应的中文例句

包含写入csv
"""

"""
获取一个单词的相关信息，返回list【"wordId","englishWord","pa","chineseWord","englishInstance1","chineseInstance1","englishInstance2","chineseInstance2"
    ,"collect","pron","fatherId"】
    对应的内容插入列表，未设置内容为空
"""


def get_all_By_one_word(word):
    """为单词生成唯一的UUID,指定命名空间和word生成唯一的id"""
    wordId = uuid.uuid3(uuid.NAMESPACE_DNS, word)
    # print(wordId)
    englishWord = word
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36 '

    }
    url = 'http://www.iciba.com/' + word
    response = requests.get(url, headers=headers)
    text = response.text
    sel = parsel.Selector(response.text)
    url_s = sel.css('span i')
    '''获取音频url'''
    UK_audio_url = ""
    US_audio_url = ""
    cnt = 0
    for i in url_s:
        audio_url = i.css('i::attr(ms-on-mouseover)').get()
        audio_url = audio_url[7:-2]
        if cnt == 0:
            UK_audio_url = audio_url
            cnt = cnt + 1
        else:
            US_audio_url = audio_url

    # print("英音：" + UK_audio_url)
    # print("美音:" + US_audio_url)
    pron = UK_audio_url
    '''获取音标'''
    pa_s = sel.css('.base-speak span span')
    cnt = 0
    UK_pa = ""
    US_pa = ""
    for span in pa_s:
        if cnt == 0:
            cnt = cnt + 1
            UK_pa = span.css('span').get()
        else:
            US_pa = span.css('span').get()
    l = 0
    r = 0
    for i in range(len(UK_pa)):
        if UK_pa[i] == '[':
            l = i
        elif UK_pa[i] == ']':
            r = i
            break
    UK_pa = UK_pa[l + 1: r]
    for i in range(len(US_pa)):
        if US_pa[i] == '[':
            l = i
        elif US_pa[i] == ']':
            r = i
            break
    US_pa = US_pa[l + 1: r]
    # print("英 ：" + UK_pa)
    # print("美 ：" + US_pa)
    pa = UK_pa
    '''获取中文意思'''
    chword_s = sel.css('.base-list .clearfix p span')
    chinese_word = ''
    for span in chword_s:
        chinese_word = chinese_word + span.css('span::text').get()
    # print("中文意思是：" + chinese_word)
    chineseWord = chinese_word

    """获取中英文例句,使用正则去掉了部分标签的内容解决掉了单词加粗或变更字体的问题"""
    url = 'http://www.ichacha.net/zaoju/' + word + '.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 '
                      'Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    text = response.text
    pattern = re.compile('<font[^>]*>')
    text = re.sub(pattern, '', text)
    pattern = re.compile('</font>')
    text = re.sub(pattern, '', text)
    pattern = re.compile('<br>')
    text = re.sub(pattern, '<p>', text)
    pattern = re.compile('</li>')
    text = re.sub(pattern, '</p></li>', text)
    # print(text)
    sel = parsel.Selector(text)
    english_instance_s = sel.css('.sent_list li')
    chinese_instance_s = sel.css('.sent_list li p')
    # print(english_instance_s)
    english_instance = []
    chinese_instance = []
    cnt = 0
    for li in english_instance_s:
        cnt = cnt + 1
        # print(cnt)
        # print(li.css('li::text').get())
        if cnt == 1 or cnt == 2 or cnt == 10:
            # english_instance = english_instance + li.css('li::text').get() + '\n'
            english_instance.append(li.css('li::text').get())
        elif cnt > 10:
            break
    cnt = 0
    for p in chinese_instance_s:
        cnt = cnt + 1
        # print(cnt)
        if cnt == 1 or cnt == 2 or cnt == 10:
            # print(p.css('p::text').get())
            # chinese_instance = chinese_instance +  + '\n'
            chinese_instance.append(p.css('p::text').get())
        elif cnt > 10:
            break
    # print("英文例句：")
    # print(english_instance)
    # print("中文例句：")
    # print(chinese_instance)
    chineseInstance2 = ""
    chineseInstance1 = ""
    englishInstance2 = ""
    englishInstance1 = ""
    """获取到的例句可能不够或者没有"""
    if len(chinese_instance) > 2:
        chineseInstance2 = chinese_instance[2]
        chineseInstance1 = chinese_instance[1]
    elif len(chinese_instance) > 1:
        chineseInstance2 = chinese_instance[1]
        chineseInstance1 = chinese_instance[0]
    elif len(chinese_instance) > 0:
        chineseInstance1 = chinese_instance[0]

    if len(english_instance) > 2:
        englishInstance2 = english_instance[2]
        englishInstance1 = english_instance[1]
    if len(english_instance) > 1:
        englishInstance2 = english_instance[1]
        englishInstance1 = english_instance[0]
    if len(english_instance) > 0:
        englishInstance1 = english_instance[0]

    res = [wordId, englishWord, pa, chineseWord, englishInstance1, chineseInstance1, englishInstance2, chineseInstance2
        , 0, pron, '']
    # print(res)
    return res


# get_all_By_one_word('masterpiece')

"""
获取单词列表中所有单词的信息,输入参数为单词的列表，返回值为单词详细信息的列表
"""


def get_words_list(words):
    wordsList = []

    for i in words:
        """存在一次爬取未爬取到的情况，再次进行爬取"""
        cnt = 0
        p = get_all_By_one_word(i)
        while p[2] == "" and p[3] == "" and cnt < 2:
            p = get_all_By_one_word(i)
            cnt = cnt + 1
        print(p)
        wordsList.append(p)
    return wordsList


"""将信息写入新的csv【"wordId","englishWord","pa","chineseWord","englishInstance1","chineseInstance1","englishInstance2","chineseInstance2"
    ,"collect","pron","fatherId"】 """

"""
将记录单词的txt读入，组成wordlist
"""


def input_word_txt(url):
    wordlist = []
    with open(url, 'r', encoding='utf-8') as fp:
        line = fp.readlines()
        for l in line:
            if l != '' and l != '\n':
                l = l.strip('\n').strip('\r').strip()
                wordlist.append(l)
        # print(wordlist)
        return wordlist


def write_into_csv(csvurl, words):
    with open(csvurl, "w", encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["wordId", "englishWord", "pa", "chineseWord", "englishInstance1", "chineseInstance1", "englishInstance2",
             "chineseInstance2"
                , "collect", "pron", "fatherId"])
        wordslist = get_words_list(words)
        for i in wordslist:
            writer.writerow(i)


write_into_csv("derive.csv", input_word_txt('derive.txt'))


# get_all_By_one_word('reactive')
