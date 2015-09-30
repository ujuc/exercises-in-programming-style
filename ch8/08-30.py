#!/usr/bin/env python2
# coding: utf-8

# 맵리듀스
# 제약조건
# 1. 입력 데이터를 여러 구역으로 나눈다.
# 2. 맵(map) 함수는 주어진 작업 함수를 잠재적으로 각 데이터 구역에 병렬로
#    적용한다.
# 3. 리듀스(reduce) 함수는 여러 작업 함수의 결과를 재결합해 일관된 출력 결과로
#    만들어 낸다.

import sys
import re
import operator
import string


# 맵듀리스용 함수
def partition(data_str, nlines):
    """
    Partitions the input data_str (a big string) into chunks of nlines.

    :param data_str:
    :param nlines:
    :return:
    """
    lines = data_str.split('\n')
    for i in xrange(0, len(lines), nlines):
        yield '\n'.join(lines[i:i + nlines])


def split_words(data_str):
    """
    Takes a string, returns a list of pairs (word, 1), one for each word
    in the input, so [(w1, 1), (w2, 1), ..., (wn, 1)]

    :param data_str:
    :return:
    """

    def _scan(str_data):
        pattern = re.compile('[\W_]+')
        return pattern.sub(' ', str_data).lower().split()

    def _remove_stop_words(word_list):
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    # 입력 내용을 단어로 나누는 실제 작업
    result = []
    words = _remove_stop_words(_scan(data_str))
    for w in words:
        result.append((w, 1))
    return result


def count_words(pairs_list_1, pairs_list_2):
    """
    Takes two lists of pairs of the form [(w1, 1), ...]
    and return a list of pairs [(w1, frequency), ...],
    where frequency is the sum of all the reported occurrences

    :param pairs_list_1:
    :param pairs_list_2:
    :return:
    """
    mapping = dict((k, v) for k, v in pairs_list_1)
    for p in pairs_list_2:
        if p[0] in mapping:
            mapping[p[0]] += p[1]
        else:
            mapping[p[0]] = 1
    return mapping.items()


# 보조함수
def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data


def sort(word_freq):
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)


# main
splits = map(split_words, partition(read_file(sys.argv[1]), 200))
splits.insert(0, [])  # 리듀스 처리를 위해 입력을 정규화 한다.
word_freqs = sort(reduce(count_words, splits))

for (w, c) in word_freqs[0:25]:
    print w, ' - ', c
