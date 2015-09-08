#!/usr/bin/env python2
# coding: utf-8

# 플러그인
# 제약조건
# 1. 문제를 어떤 추상 형태(프로시저, 함수, 색체 등)을 사용해 분해한다.
# 2. 그러한 추상의 전부 또는 일부를 일반적으로 미리 컴파일해 두는 자체적인 꾸러미(package)에
#    물리적으로 캡슐화한다. 주 프로그램과 각 꾸러미는 독립적으로 컴파일한다. 주 프로그램에서는
#    이러한 꾸러미를 일반적으로 (반드시 그런 것은 아니지만) 프로그램을 시작할 때 동적으로 적재한다.
# 3. 주 프로그램은 동적으로 적재한 꾸러미에서 함수/객체를 사용하지만 정확한 구현 내용은 모른다. 주
#    프로그램을 고치거나 다시 컴파일하지 않고 새로운 구현 내용을 사용할 수 있다.
# 4. 어느 꾸러미를 적재할지 지정하는 외부 명세가 존재한다. 이는 실행 중 적재할 코드에 관한 외부
#    명세를 위한 섲렁 파일, 약속해 둔 경로, 사용자 입력 또는 그 밖의 메커니즘으로 처리할 수 있다.

import sys
import ConfigParser
import imp


def load_plugins():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    words_plugin = config.get("Plugins", "words")
    frequencies_plugin = config.get("Plugins", "frequencies")
    global tfwords, tffreqs
    tfwords = imp.load_compiled('tfwords', words_plugin)
    tffreqs = imp.load_compiled('tffreqs', frequencies_plugin)


load_plugins()
word_freqs = tffreqs.top25(tfwords.extract_words(sys.argv[1]))

for (w, c) in word_freqs:
    print "{} - {}".format(w, c)
