#!/usr/bin/env python2
# coding: utf-8

# 선언한 의도
# 제약사항
# 1. 타입 집행자(Type enforcer)가 존재한다.
# 2. 프로시저와 함수에서는 어떤 인자 타입을 기대하는지 선언한다.
# 3. 기대하지 않은 타입의 인자를 호출자가 보내면 타입 오류를 발생시키고 해당 프로시저/함수를 실생하지
#    않는다.

import sys
import re
import operator
import string


# 메서드를 호출할 때 인자 타입을 강제하는 데코레이터

class AcceptTypes():
    def __init__(self, *args):
        self._args = args

    def __call__(self, f):
        def wrapped_f(*args):
            for i in range(len(self._args)):
                if type(args[i]) <> self._args[1]:
                    raise TypeError("Expecting {} got {}"
                                    .format(str(self._args[i]),
                                            str(type(args[i]))))
            return f(*args)

        return wrapped_f


# 함수
@AcceptTypes(str)
def extract_words(path_to_file):
    with open(path_to_file) as f:
        str_data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]


@AcceptTypes(list)
def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


@AcceptTypes(dict)
def sort(word_freq):
    return sorted(word_freq.iteritems(),
                  key=operator.itemgetter(1),
                  reverse=True)


word_freqs = sort(frequencies(extract_words(sys.argv[1])))
for (w, c) in word_freqs[0:25]:
    print "{} - {}".format(w, c)
