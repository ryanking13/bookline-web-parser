# -*- coding: utf-8 -*-
from urllib import request, parse
from bs4 import BeautifulSoup
from bookstores import kyobo
import re


# 사용자로부터 날짜 정보를 입력받는다
def get_date():
    date = input('검색할 년 월 주를 입력하세요(xxxx-xx-x) : ')
    #date = '2017-02-1'

    if not bool(re.match('\d{4}-\d{2}-\d{1}', date)):
        print('포맷이 올바르지 않습니다.')
        exit(0)

    return date


# 책 리스트에서 각 책 페이지 링크를 parsing 한다
def read_bids(page):
    soup = BeautifulSoup(page, 'html.parser')
    title_class = 'N=a:bel.title'
    bids = []

    for link in soup.find_all('a'):
        if link.get('class') is not None and link.get('class')[0] == title_class:
            bids.append(link.get('href'))

    bids = set(bids)
    return bids


# 책 소개 페이지에서 지정된 정보를 parsing 한다
def parse_instance(page, instance):
    soup = BeautifulSoup(page, 'html.parser')
    instance_class = 'N=a:bil.' + instance

    for link in soup.find_all('a'):
        if link.get('class') is not None and link.get('class')[0].startswith(instance_class):
            text = re.findall("(?<=>).+?(?=</a>)", str(link))[0]
            text = re.findall(".+?(?=<|$)", text)[0].strip()  # removing additional tags
            return text


# 책 소개 페이지에서 대사부를 parsing 한다
def parse_phrases(page):
    soup = BeautifulSoup(page, 'html.parser')
    phrase_class = 'order35'

    for header in soup.find_all('h3'):
        if header.get('class') is not None and len(header.get('class')) > 1 \
                and header.get('class')[1] == phrase_class:

            phrases = str(header.parent.p)
            phrases = re.findall("((?<=<p>)(.|\s)+?(?=</p>))", phrases)[0][0]
            phrases = re.split('<br/><br/>|</p>\\r\\n\\t \\t\\t<p>', phrases)

            length = len(phrases)
            for i in range(length):
                phrases[i] = re.sub('<br/>', '\n', phrases[i])  # html <br> tag to newline
                phrases[i] = re.sub('<em>|</em>', '', phrases[i])  # html <em> tag remove
                phrases[i] = re.sub('<b>.*?</b>', '', phrases[i])  # title remove

                # page info remove
                # TODO: optimize
                phrases[i] = re.sub('\n*---.+$|\n.+?중에서$', '', phrases[i])
                phrases[i] = re.sub('---.+\n', '\n', phrases[i])
                phrases[i] = re.sub('- .+?중에서', '', phrases[i])
                phrases[i] = re.sub('- \d+쪽에서', '', phrases[i])
                phrases[i] = re.sub('\d+$', '', phrases[i])

            phrases = [phrases[i] + '\n' for i in range(length) if phrases[i] != '']
            return phrases


def main():

    # 책 정보를 찾아오고자 하는 주를 입력받는다
    date = get_date()

    # 최종 output이 저장될 파일
    save_file = open('save.txt', 'w', encoding='utf-8')

    bid_link = "http://book.naver.com/bookdb/book_detail.nhn?bid="

    print('[*] parsing started')

    for i in range(1, kyobo['max_index']+1):

        url = "http://book.naver.com/bestsell/bestseller_list.nhn"
        data = parse.urlencode({'cp': kyobo['cp'], 'cate': kyobo['category']['novel'], 'bestWeek': date, 'page': i}).encode('utf-8')
        book_list_page = request.urlopen(url, data=data)
        book_list_page = book_list_page.read().decode('utf-8')

        book_ids = read_bids(book_list_page)

        for book_id in book_ids:
            book_page = request.urlopen(book_id)
            book_page = book_page.read().decode('utf-8')

            if not bool(re.search('tit order35', book_page)):  # 대사 정보 유무
                continue

            title = parse_instance(book_page, 'title')
            author = parse_instance(book_page, 'author')
            publisher = parse_instance(book_page, 'publisher')

            save_file.write('Title: ' + title + '\n')
            save_file.write('Author: ' + author + '\n')
            save_file.write('Publisher: ' + publisher + '\n')
            save_file.write('Link: ' + book_id + '\n')
            save_file.write('ID: ' + book_id.split('=')[-1] + '\n\n')

            phrases = parse_phrases(book_page)

            for phrase in phrases:
                save_file.write(phrase + '\n')

            save_file.write('-----\n\n')

    save_file.close()
    print('[*] parsing done, file saved')

if __name__ == '__main__':
    main()