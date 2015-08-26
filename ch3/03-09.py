#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 유일
# 제약 조건
# 1. 값이 변환될 대상인 추상화가 존재한다.
# 2. 이 추상화는 (1) 값을 감싸 그 값을 해당 추상화로 만들고 (2) 자신을 함수와 결합해
#    일련의 함수를 수립하여 (3) 최종 결과를 살펴볼 수 있도록 그 값을 풀어내는 연산을
#    제공한다.
# 3. 규모가 큰 문제를 함수 파이프라인을 함께 결합하고 마지막에 값을 다시 풀어내서
#    해결한다.
# 4. 유일 형식에서는 특히 결합 연산에서 주어진 함수를 단순히 호출하기만 하는데, 이때
#    연산에서 담고 있는 값을 그 함수에 전달한 다음 그 함수에서 반환된 값을 다시 담는다.

import sys
import re
import operator
import string


# 예제에서 사용할 유일한 클래스
class TFTheOne:
    def __init__(self, v):
        self._value = v

    def bind(self, func):
        self._value = func(self._value)
        return self

    def printme(self):
        print self._value


# 함수

def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data


def filter_chars(str_data):
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', str_data)


def normalize(str_data):
    return str_data.lower()


def scan(str_data):
    return str_data.split()


def remove_stop_words(word_list):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    # 한 글자로 된 단어를 추가한다.
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    word_freqs = dict()
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    return sorted(word_freq.iteritems(), key=operator.itemgetter(1),
                  reverse=True)


def top25_freqs(word_freqs):
    top25 = ""
    for tf in word_freqs[0:25]:
        top25 += str(tf[0]) + ' - ' + str(tf[1]) + '\n'
    return top25


# 주함수
TFTheOne(sys.argv[1]).bind(read_file).bind(filter_chars)\
    .bind(normalize).bind(scan).bind(remove_stop_words).bind(frequencies)\
    .bind(sort).bind(top25_freqs).printme()
