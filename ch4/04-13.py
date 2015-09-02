#!/usr/bin/env python2
# coding: utf-8

# 추상사물
# 제약조건
# 1. 규모가 큰 문제를 문제 영역에 합당한 추상 사물(abstract thing)로 분해한다.
# 2. 각 추상 사물은 그 추상화한 사물이 최종적으로 할 수 있는 연산으로 기술한다.
# 3. 그런 다음 구체 사물은 어떻게든 해당 추상화와 결합하여, 그 메커니즘은 다양하다.
# 4. 응용 프로그램의 나머지 부분에서는 그 사물을, 추상화한 형태가 아니라 해당 추상화로
#    무엇을 할 수 있느냐에 따라 사용한다.

import abc
import sys
import re
import operator
import string


# 추상 사물

class IDataStorage(object):
    """
    Models the contents of the file
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def words(self):
        """
        Returns the words in storage
        :return:
        """
        pass


class IStopWordFilter(object):
    """
    Models the stop word filter
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_stop_word(self, word):
        """
        Checks whether the given word is a stop word
        :param word:
        :return:
        """
        pass


class IWordFrquencyCounter(object):
    """
    Keeps the word frequency data
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def increment_count(self, word):
        """
        Increments the count for the given word
        :param word:
        :return:
        """
        pass

    @abc.abstractmethod
    def sorted(self):
        """
        Returns the words and their frequencies, sorted by frequency
        :return:
        """
        pass


# 구체 사물

class DataStorageManager:
    _data = ''

    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()
        self._data = ''.join(self._data).split()

    def words(self):
        return self._data


class StopWordManager:
    _stop_words = []

    def __int__(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words


class WordFrequencyManager:
    _word_freqs = {}

    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.iteritems(), key=operator.itemgetter(1),
                      reverse=True)


# 추상 사물과 구체 사물간 연결
IDataStorage.register(DataStorageManager)
IStopWordFilter.register(StopWordManager)
IWordFrquencyCounter.register(WordFrequencyManager)


# 응용 프로그램 객체
class WordFrequencyController:
    def __init__(self, path_to_file):
        self._storage = DataStorageManager(path_to_file)
        self._stop_word_manager = StopWordManager()
        self._word_freq_counter = WordFrequencyManager()

    def run(self):
        for w in self._storage.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_counter.increment_count(w)

        word_freqs = self._word_freq_counter.sorted()
        for (w, c) in word_freqs[0:25]:
            print "{} - {}".format(w, c)


# 주 함수
WordFrequencyController(sys.argv[1]).run()
