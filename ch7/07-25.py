#!/sur/bin/evn python2
# coding: utf-8

# 영속 테이블
# 제약조건
# 1. 데이터는 해당 데이터를 사용하는 프로그램을 실행 너머에 존재하며, 이는 다른 여러 프로그램에서
#    사용된다는 것을 의미한다.
# 2. 데이터는 탐색을 더 쉽게/빠르게 할 수 있는 방법으로 저장한다. 예를 들면
#    * 문제에 대한 입력 데이터는 일련의 데이터 도메인(또는 타입)으로 모델링한다.
#    * 구체 데이터는 응용 프로그램의 데이터와 식별한 도메인 간에 관계를 형성하며, 몇몇 도메인의
#      구성 요소를 가진 것으로 모델링한다.
# 3. 문제는 해당 데이터를 질의하는 방식으로 해결한다.

import sys
import re
import string
import sqlite3
import os.path


# 이 문제에 대한 관계형 데이터베이스는 다음의 세 테이블로 구성된다.
# documents, words, characters
#
def create_db_schema(connection):
    c = connection.cursor()
    c.execute(
        '''CREATE TABLE documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name)''')
    c.execute('''CREATE TABLE words (id, doc_id, value)''')
    c.execute('''CREATE TABLE characters (id, word_id, value)''')
    connection.commit()
    c.close()


def load_file_into_database(path_to_file, connection):
    """
    Takes the path to a file and loads the contents into the database

    :param path_to_file:
    :param connection:
    :return:
    """

    def _extract_words(path_to_file):
        with open(path_to_file) as f:
            str_data = f.read()
        pattern = re.compile('[\W_]+')
        word_list = pattern.sub(' ', str_data).lower().split()
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    words = _extract_words(path_to_file)

    # 이제 데이터베이스에 데이터를 추가해보자.
    # 문서 자체를 데이터베이스에 추가한다.
    c = connection.cursor()
    c.execute("INSERT INTO documents (name) VALUES (?)", (path_to_file,))
    c.execute("SELECT id from documents WHERE name=?", (path_to_file,))
    doc_id = c.fetchone()[0]

    # 단어를 데이터베이스에 추가한다.
    c.execute("SELECT MAX(id) FROM words")
    row = c.fetchone()
    word_id = row[0]
    if word_id == None:
        word_id = 0
    for w in words:
        c.execute("INSERT INTO words VALUES (?, ?, ?)", (word_id, doc_id, w))
        # 문자를 데이터베이스에 추가한다.
        char_id = 0
        for char in w:
            c.execute("INSERT INTO characters VALUES (?, ?, ?)", (
                char_id, word_id, char
            ))
            char_id += 1
        word_id += 1
    connection.commit()
    c.close()


# 존재하지 않으면 생성한다.
if not os.path.isfile('tf.db'):
    with sqlite3.connect('tf.db') as connection:
        create_db_schema(connection)
        load_file_into_database(sys.argv[1], connection)

# 이제 질의해 보자
with sqlite3.connect('tf.db') as connection:
    c = connection.cursor()
    c.execute(
        "SELECT value, COUNT(*) AS C FROM words GROUP BY value ORDER BY C DESC")
    for i in range(25):
        row = c.fetchone()
        if row is not None:
            print "{} - {}".format(row[0], str(row[1]))
