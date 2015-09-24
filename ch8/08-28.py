#!/usr/bin/env python2
# coding: utf-8

# 행위자
# 제약조건
# 1. 규모가 큰 문자는 문제 영역에 합당한 사물로 분해한다.
# 2. 각 사물에는 다른 사물에게 의미 있는 큐가 있으며, 그곳에 메시지를 둔다.
# 3. 각 사물은 데이터의 캡슐이며, 자신의 능력은 큐를 통해 메시지를 받을 때만
#    드러낸다.
# 4. 각 사물에는 다른 사물과 독립적인 자신만의 실행 스레드가 있다.

import sys
import re
import operator
import string
from threading import Thread
from Queue import Queue


class ActiveWFObject(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.name = str(type(self))
        self.queue = Queue()
        self._stop = False
        self.start()

    def run(self):
        while not self._stop:
            message = self.queue.get()
            self._dispatch(message)
            if message[0] == 'die':
                self._stop = True


def send(receiver, message):
    receiver.queue.put(message)


class DataStorageManager(ActiveWFObject):
    """
    Models the contents of the file
    """
    _data = ''

    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'send_word_freqs':
            self._process_words(message[1:])
        else:
            # 전달
            send(self._stop_word_manager, message)

    def _init(self, message):
        path_to_file = message[0]
        self._stop_word_manager = message[1]
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def _process_words(self, message):
        recipient = message[0]
        data_str = ''.join(self._data)
        words = data_str.split()
        for w in words:
            send(self._stop_word_manager, ['filter', w])
        send(self._stop_word_manager, ['top25', recipient])


class StopWordManager(ActiveWFObject):
    """
    Models the stp word filter
    """
    _stop_words = []

    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'filter':
            return self._filter(message[1:])
        else:
            # 전달
            send(self._word_freqs_manager, message)

    def _init(self, message):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))
        self._word_freqs_manager = message[0]

    def _filter(self, message):
        word = message[0]
        if word not in self._stop_words:
            send(self._word_freqs_manager, ['word', word])


class WordFrequencyManager(ActiveWFObject):
    """
    Keeps the word frequency data
    """
    _word_freqs = {}

    def _dispatch(self, message):
        if message[0] == 'word':
            self._increment_count(message[1:])
        elif message[0] == 'top25':
            self._top25(message[1:])

    def _increment_count(self, message):
        word = message[0]
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def _top25(self, message):
        recipient = message[0]
        freqs_sorted = sorted(self._word_freqs.iteritems(),
                              key=operator.itemgetter(1),
                              reverse=True)
        send(recipient, ['top25', freqs_sorted])


class WordFrequencyController(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'top25':
            self._display(message[1:])
        else:
            raise Exception("Message not understood " + message[0])

    def _run(self, message):
        self._storage_manager = message[0]
        send(self._storage_manager, ['send_word_freqs', self])

    def _display(self, message):
        word_freqs = message[0]
        for (w, f) in word_freqs[0:25]:
            print '{} - {}'.format(w, f)
        send(self._storage_manager, ['die'])
        self._stop = True


# main
word_freq_manager = WordFrequencyManager()

stop_word_manager = StopWordManager()
send(stop_word_manager, ['init', word_freq_manager])

storage_manager = DataStorageManager()
send(stop_word_manager, ['init', sys.argv[1], stop_word_manager])

wfcontroller = WordFrequencyController()
send(wfcontroller, ['run', storage_manager])

# 활동 객체가 마칠때까지 기다린다.
[t.join() for t in [word_freq_manager, stop_word_manager,
                    storage_manager, wfcontroller]]
