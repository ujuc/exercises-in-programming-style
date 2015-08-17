#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 요리책
# 제약조건
# 1. Long jump가 없다.
# 2. 절차적 추상화를 이용해 규모가 큰 문제를 더 작은 단위로 분할함으로써 제어 흐름 복잡도를
#    완화한다.
# 3. 프로시저는 상태를 전역 변수 형태로 공유할 수 있다.
# 4. 규모가 큰 문제는 공유한 상태를 변경하거나 그 상태를 더 추가하는 프로시저를 차례로
#    적용해 해결한다.

import sys
import string

# 변경 가능한 공유 데이터
data = list()
words = list()
word_freqs = list()


# 프로시저
def read_file(path_to_file):
    """
    Takes a path to a file and assigns the entire
    contents of the file to the global variable data

    :param path_to_file:
    :return:
    """
    global data
    with open(path_to_file) as f:
        data = data + list(f.read())


def filter_chars_and_normalize():
    """
    Replaces all nonalphanumeric chars in data with white space

    :return:
    """
    global data
    for i in range(len(data)):
        if not data[i].isalnum():
            data[i] = ' '
        else:
            data[i] = data[i].lower()


def scan():
    """
    Scans data for words, filling the global variable words

    :return:
    """
    global data
    global words
    data_str = ''.join(data)
    words = words + data_str.split()


def remove_stop_words():
    global words
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # 한 글자로 된 단어를 추가한다.
    stop_words.extend(list(string.ascii_lowercase))
    indexes = list()
    for i in range(len(words)):
        if words[i] in stop_words:
            indexes.append(i)
    for i in reversed(indexes):
        words.pop(i)


def frequencies():
    """
    Creates a list of pairs associating
    words with frequencies

    :return:
    """
    global words
    global word_freqs
    for w in words:
        keys = [wd[0] for wd in word_freqs]
        if w in keys:
            word_freqs[keys.index(w)][1] += 1
        else:
            word_freqs.append([w, 1])


def sort():
    """
    Sorts word_freqs by frequency

    :return:
    """
    global word_freqs
    word_freqs.sort(lambda x, y: cmp(y[1], x[1]))


# 주함수
read_file(sys.argv[1])
filter_chars_and_normalize()
scan()
remove_stop_words()
frequencies()
sort()

for tf in word_freqs[0:25]:
    print tf[0], ' - ', tf[1]