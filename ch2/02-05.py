#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 파이프라인
# 제약조건
# 1. 규모가 큰 문제를 함수형 추상화를 사용해 분해한다. 함수는 입력을 취해 출력을 만들어
#    낸다.
# 2. 함수는 상태를 서로 공유하지 않는다.
# 3. 수학적 함수 합성의 결과를 신뢰할 수 있는 것처럼 규모가 큰 문제는 함수를 차례차례
#    파이프라인으로 합성해 해결한다.

import sys
import re
import operator
import string


# 함수

def read_file(path_to_file):
    """
    Takes a path to a file and returns the entire
    contents of the file as a string

    :param path_to_file:
    :return data:
    """
    with open(path_to_file) as f:
        data = f.read()
    return data


def filter_chars_and_normalize(str_data):
    """
    Takes a string and returns a copy with all nonalphanumeric
    chars replaced by white space

    :param str_data:
    :return pattern.sub(' ', str_data).lower():
    """
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', str_data).lower()


def scan(str_data):
    """
    Takes a string and scans for words, returning
    a list of words.

    :param str_data:
    :return str_data.split():
    """
    return str_data.split()


def remove_stop_words(word_list):
    """
    Takes a list of words and returns a copy with all stop
    words removed

    :param word_list:
    :return:
    """
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # 한 글자로 된 단어를 추가한다.
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    """
    Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence

    :param word_list:
    :return:
    """
    word_freqs = dict()
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    """
    Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency

    :param word_freq:
    :return:
    """
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1),
                  reverse=True)


def print_all(word_freqs):
    """
    Takes a list of pairs where the entries are sorted by
    frequency and print them recursively.

    :param word_freqs:
    :return:
    """
    if(len(word_freqs) > 0):
        print word_freqs[0][0], ' - ', word_freqs[0][1]
        print_all(word_freqs[1:])


# 주함수
print_all(
    sort(
        frequencies(
            remove_stop_words(
                scan(
                    filter_chars_and_normalize(
                        read_file(
                            sys.argv[1]
                        )
                    )
                )
            )
        )
    )
    [0:25]
)
