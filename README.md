# Naver Book Crawler
  - 네이버 책 DB를 사용하여 책의 대사들을 크롤링 하는 프로그램
  - 검색할 년도-월-주를 지정하면 해당 주 소설 영역 베스트셀러를 기준으로 검색함
  - 현재 교보문고 베스트셀러를 기준으로 검색함

```
$ python web-parser.py

검색할 년 월 주를 입력하세요(xxxx-xx-x) : 2017-10-1
[*] parsing started
[*] parsing done, file saved
```

```
# --> save.txt

Title: 기사단장 죽이기
Author: 무라카미 하루키
Publisher: 문학동네
Link: http://book.naver.com/bookdb/book_detail.nhn?bid=12210808
ID: 12210808

시간이 흐른 뒤 돌이켜보면 우리 인생은 참으로 불가사의하게 느껴진다. 믿을 수 없이 갑작스러운 우연과 예측 불가능한 굴곡진 전개가 넘쳐난다. 하지만 그것들이 실제로 진행되는 동안에는 대부분 아무리 주의깊게 둘러보아도 불가해한 요소가 전혀 눈에 띄지 않는다. 우리 눈에는 쉼없이 흘러가는 일상 속에서 지극히 당연한 일이 지극히 당연하게 일어나는 것처럼 비치는 것이다.
...
```
## TODO
  - 출판사, 장르 별 지원
  - 파싱 알고리즘 업데이트
