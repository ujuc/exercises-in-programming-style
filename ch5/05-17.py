#!/usr/bin/env python2
# coding: utf-8

# 반영
# 제약조건
# 1. 프로그램은 자기 자신에 관한 정보에 접근한다. 즉, 자기 관찰.
# 2. 프로그램은 실행 중에 추상화, 변수 등을 추가하는 식으로 자신을 변경할 수 있다.

import sys
import string
import os

# 현실적 두 가지
stops = set(open("../stop_words.txt").read().split(",")
            + list(string.ascii_lowercase))


def frequencies_imp(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


# 함수를 문자열로 작성해 보자
if len(sys.argv) > 1:
    extract_words_func = "lambda name : [x.lower()" \
                         "for x in re.split('[^a-zA-Z]+', open(name).read()) " \
                         "if len(x) > 0 and x.lower() not in stops]"
    frequencies_func = "lambda wl : frequencies_imp(wl)"
    sort_func = "lambda word_freq: sorted(word_freq.iteritems()," \
                "key=operator.itemgetter(1), reverse=True)"
    filename = sys.argv[1]
else:
    extract_words_func = "lambda x: []"
    frequencies_func = "lambad x: []"
    sort_func = "lambda x: []"
    filename = os.path.basename(__file__)

# 지금까지 이 프로그램에는 단어 빈도에 관한 내용이 별로 없으며, 함수처럼 보이는 문자열 더미만 보인다.
# 그 함수를 '기본' 프로그램에 동적으로 추가해보자.
exec ('extract_words = ' + extract_words_func)
exec ('frequencies = ' + frequencies_func)
exec ('sort = ' + sort_func)

# 주 함수, 이 함수는 다음과 같이 잘 작동한다:
#  word_freqs = sort(frequencies(extract_words(filename)))
word_freqs = locals()['sort'](locals()['frequencies']
                              (locals()['extract_words'](filename)))

for (w, c) in word_freqs[0:25]:
    print "{} - {}".format(w, c)
