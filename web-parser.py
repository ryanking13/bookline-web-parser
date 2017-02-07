# -*- coding: utf-8 -*-
from urllib import request
import re


def get_date():
    date = input('검색할 년 월 주를 입력하세요(xxxx-xx-x) : ')
    #date = '2017-02-1'

    if not bool(re.match('\d{4}-\d{2}-\d{1}', date)):
        print('포맷이 올바르지 않습니다.')
        exit(0)

    return date


def read_bids(page):
    bids = re.findall('http://book\.naver\.com/bookdb/book_detail\.nhn\?bid=\d+', page)
    bids = set(bids)
    return bids


def parse_instance(page, instance):

    parsed_instance = re.findall(("class=\"N=a:bil\.%s.+?</a>" % instance), page)[0]
    parsed_instance = re.findall("(?<=>).+?(?=</a>)", parsed_instance)[0]
    parsed_instance = re.findall(".+?(?=&nbsp|$)", parsed_instance)[0]
    return parsed_instance


def parse_phrases(page):
    phrases = re.findall("(<h3 class=\"tit order35\">(.|\s)+?</div>)", page)[0][0]
    phrases = re.findall("((?<=<p>)(.|\s)+?(?=</p>))", phrases)[0][0]
    phrases = re.split('<br/><br/>|</p>\\r\\n\\t \\t\\t<p>', phrases)

    length = len(phrases)
    for i in range(length):
        phrases[i] = re.sub('<br/>', '\n', phrases[i])
        phrases[i] = re.sub('\n*---.+$|\n.+?중에서$', '', phrases[i])
        phrases[i] = re.sub('&nbsp;<em>|</em>', '', phrases[i])
        phrases[i] = re.sub('<b>.*?</b>', '', phrases[i])

    phrases = [phrases[i] + '\n' for i in range(length) if phrases[i] != '']
    return phrases


def main():

    kyobo = {'cp': 'kyobo', 'max_index': 6}

    date = get_date()
    save_file = open('save.txt', 'w')
    print('[*] parsing started')

    for i in range(1,kyobo['max_index']+1):
        page = request.urlopen("http://book.naver.com/bestsell/bestseller_list.nhn?cp=%s&cate=01&bestWeek=%s&indexCount=1&type=list&page=%d" % (kyobo['cp'], date, i))
        data = page.read().decode('utf-8')

        book_ids = read_bids(data)

        for book_id in book_ids:
            book_page = request.urlopen(book_id)
            book_page_data = book_page.read().decode('utf-8')

            if not bool(re.search('tit order35', book_page_data)):  # 대사 정보 유무
                continue

            title = parse_instance(book_page_data, 'title')
            author = parse_instance(book_page_data, 'author')
            publisher = parse_instance(book_page_data, 'publisher')
            save_file.write('Title: ' + title + '\n')
            save_file.write('Author: ' + author + '\n')
            save_file.write('Publisher: ' + publisher + '\n\n')

            phrases = parse_phrases(book_page_data)

            for phrase in phrases:
                save_file.write(phrase + '\n')

            save_file.write('-----\n\n')

    save_file.close()
    print('[*] parsing done, file saved')
if __name__ == '__main__':
    main()