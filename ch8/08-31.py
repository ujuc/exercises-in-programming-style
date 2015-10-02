#!/usr/bin/env python2
# coding: utf-8

# 이중 맵리듀스
# 제약조건
# 1. 입력 데이터를 여러 구역으로 나눈다.
# 2. 맵 함수는 주어진 작업 함수를 잠재적으로 각 데이터 구역에 병렬로 적용한다.
# 3. 여러 작업 함수에서 얻은 결과를 다시 섞는다.
# 4. 리듀스 함수를 입력으로 취하는 두 번째 맵 함수에 다시 섞은 데이터 구역을
#    입력으로 넣는다.
# 5. 선택 단계: 리듀스 함수는 여러 작업 함수의 결과를 재결합해 일관된 출력
#    결과로 만들어 낸다.

import sys
import re
import operator
import string


# 맵리듀스용 함수
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
    Takes a string, returns a list of pairs (word, 1), one for each word in
    the input, so [(w1, 1), (w2, 1), ..., (wn, 1)]

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

    # 실제 작업
    result = []
    words = _remove_stop_words(_scan(data_str))
    for w in words:
        result.append((w, 1))
    return result


def regroup(pairs_list):
    """
    Takes a list of lists of pairs of the form [(w1, 1), (w2, 1), ..., (wn, 1)],
    [(w1, 1), (w2, 1), ..., (wn, 1)], ...]
    and returns a dictionary mapping each unique word to the corresponding list
    of pairs, so { w1: [(w1, 1), (w1, 1) ...], w2: [(w2, 1), (w2, 1), ...],
    ...}

    :param pairs_list:
    :return:
    """
    mapping = {}
    for pairs in pairs_list:
        for p in pairs:
            if p[0] in mapping:
                mapping[p[0]].append(p)
            else:
                mapping[p[0]] = [p]
    return mapping


def count_words(mapping):
    """
    Takes a mapping of the form (word, [(word, 1), (word, 1) ...)]) and returns
    a pair (word, frequency), where frequency is the sum of all the reported
    occurrences

    :param mapping:
    :return:
    """

    def add(x, y):
        return x + y

    return (mapping[0], reduce(add, (pair[1] for pair in mapping[1])))


# 보조 함수
def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data


def sort(word_freq):
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)


# main
splits = map(split_words, partition(read_file(sys.argv[1]), 200))
splits_per_word = regroup(splits)
word_freqs = sort(map(count_words, splits_per_word.items()))

for (w, c) in word_freqs[0:25]:
    print w, ' - ', c
