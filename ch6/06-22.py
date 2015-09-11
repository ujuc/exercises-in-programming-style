#!/usr/bin/env python2
# coding: utf-8

# 수동공격
# 제약조건
# 1. 모든 프로시저와 함수에서는 인자의 무결성을 확인하고 그 인자가 적절하지 않으면 해당 함수를 벗어
#    나 계속 진행하기 ㄹ거부한다.
# 2. 다른 함수를 호출할 때 프로그램 함수에서는 그 자신이 의미 있는 반응을 할 수 있는 상태라면 오류만
#    확인한다.
# 3. 예외 처리는 어디서든 의미만 있다면 함수 호출 사슬의 상위 수준에서 수행한다.

import sys
import re
import operator
import string


# 함수
def extract_words(path_to_file):
    assert (type(path_to_file) is str), "I need a string! I quit!"
    assert (path_to_file), "I need a non-empty string! I quit!"

    with open(path_to_file) as f:
        data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', data).lower().split()
    return word_list


def remove_stop_words(word_list):
    assert (type(word_list) is list), "I need a list! I quit!"

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # 한 글자로 된 단어를 추가한다.
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    assert (type(word_list) is list), "I need a list! I quit!"
    assert (word_list <> []), "I need a non-empty list! I quit!"

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freqs):
    assert (type(word_freqs) is dict), "I need a dictionary! I quit!"
    assert (word_freqs <> []), "I need a non-empty dictionary! I quit!"

    return sorted(word_freqs.iteritems(), key=operator.itemgetter(1),
                  reverse=True)


# 주 함수
try:
    assert (len(sys.argv) > 1), "You idiot! I need an input file! I quit!"
    word_freqs = sort(
        frequencies(remove_stop_words(extract_words(sys.argv[1]))))

    assert (len(word_freqs) > 25), "OMG! Less than 25 words! I QUIT!"
    for tf in word_freqs[0:25]:
        print "{} - {}".format(tf[0], tf[1])
except Exception as e:
    print "Something wrong: {}".format(e)
