#!/usr/bin/env python2
# coding: utf-8

# 스프레드시트
# 제약조건
# 1. 데이터 열과 공식을 사용해 문제를 스프레드시트처럼 모델링한다.
# 2. 어떤 데이터는 공식에 의해 다른 데이터에 의존한다. 데이터가 바뀌면
#    그에 의존하는 데이터 역시 자동으로 바뀐다.

import sys
import re
import itertools
import operator


# 열, 각 열은 데이터 요소와 공식이다.
# 처음 두 열은 입력 데이터이므로 공식이 아니다.

all_words = [(), None]
stop_words = [(), None]
non_stop_words = [(), lambda: \
    map(lambda w: w if w not in stop_words[0] else '', all_words[0])]
unique_words = [(), lambda: set([w for w in non_stop_words[0] if w != ''])]
counts = [(), lambda: map(lambda w, word_list: word_list.count(w),
                          unique_words[0],
                          itertools.repeat(non_stop_words[0],
                                           len(unique_words[0])))]
sorted_data = [(), lambda: sorted(zip(list(unique_words[0]),
                                      counts[0]),
                                  key=operator.itemgetter(1),
                                  reverse=True)]

# 전체 스프레드시트
all_columns = [all_words, stop_words, non_stop_words,
               unique_words, counts, sorted_data]


# 데이터 열 전체에 대한 활성 프로시저.
# 입력 데이터가 바뀔 때마다 또는 주기적으로 이를 호출한다.
def update():
    global all_columns
    # 각 열에 공식을 적용한다.
    for c in all_columns:
        if c[1] != None:
            c[0] = c[1]()


# 처음 두 열에 고정 데이터를 적재한다.
all_words[0] = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
stop_words[0] = set(open('../stop_words.txt').read().split(','))
# 공식을 사용해 해당 열을 갱신한다.
update()

for (w, c) in sorted_data[0][:25]:
    print "{} - {}".format(w, c)
