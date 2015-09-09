#!/usr/bin/env python2
# coding: utf-8

# 구성주의
# 제약조건
# 1. 모든 함수에서는 이자의 무결성을 확인하고 그 인자가 적절하지 않으면 그에 따른 어떤 값을 변환하거나
#    그 인자에 적절한 값을 대입한다.
# 2. 모든 코드 구역은 발생 가능한 오류를 확인하고 뭔가가 잘못되면 해당 사태를 적절하게 설정하고
#    해당 구역을 탈출한 다음, 해당 함수의 나머지 부분을 계속 실행한다.

import sys
import re
import operator
import string


# 함수
def extract_words(path_to_file):
    if type(path_to_file) is not str or not path_to_file:
        return []

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except IOError as e:
        print "I/O error({0}) when opening {1}: {2}".format(e.errno,
                                                            path_to_file,
                                                            e.strerror)
        return []

    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    return word_list


def remove_stop_words(word_list):
    if type(word_list) is not list:
        return []

    try:
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
    except IOError as e:
        print "I/O error({0}) when opening ../stops_words.txt: {1}" \
            .format(e.errno, e.strerror)
        return word_list

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    if type(word_list) is not list or word_list == []:
        return {}

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    if type(word_freq) is not dict or word_freq == {}:
        return []

    return sorted(word_freq.iteritems(), key=operator.itemgetter(1),
                  reverse=True)


# main
filename = sys.argv[1] if len(sys.argv) > 1 else "../input.txt"
word_freqs = sort(frequencies(remove_stop_words(extract_words(filename))))

for tf in word_freqs[0:25]:
    print "{} - {}".format(tf[0], tf[1])
