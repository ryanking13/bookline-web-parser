# -*- coding: utf-8 -*-

import sqlite3
import re

def main():
    con = sqlite3.connect('database.sqlite3')
    cursor = con.cursor()

    cursor.execute('SELECT * FROM entries')
    l = cursor.fetchall()
    idx = len(l)
    # print(l)

    # file_name = input("file name that contains info which will be saved in db :")
    file_name = "save.txt"
    file = open(file_name, 'rt', encoding='utf-8')
    data = file.read()
    data = data.split('-----')

    for d in data:
        try:
            d = d.strip()
            title = re.findall('(?<=Title: ).*?(?=\n)', d)[0]
            author = re.findall('(?<=Author: ).*?(?=\n)', d)[0]
            publisher = re.findall('(?<=Publisher: ).*?(?=\n)', d)[0]
            link = re.findall('(?<=Link: ).*?(?=\n)', d)[0]
            id = re.findall('(?<=ID: ).*?(?=\n)', d)[0]
            contents = re.findall('(?<=\n\n).*?(?=\n\n|$)', d, re.DOTALL)
        except IndexError as e:
            continue

        #print(title, author, publisher)
        for c in contents:
            #print(c)
            c = c.replace("'", "''")
            try:
                cursor.execute("INSERT INTO entries VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (id, title, author, publisher, link, c))
            except sqlite3.IntegrityError as e:
                print('FIND DUPLICATE')
                break

    con.commit()
    con.close()




if __name__ == '__main__':
    main()