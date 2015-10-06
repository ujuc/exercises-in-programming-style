#!/usr/bin/env python2
# coding: utf-8

# REST 방식
# 제약조건
# 1. 쌍방향 활성 행위자(예를 들면, 사람)와 백엔드 간
# 2. 클라이언트와 서버의 분리, 둘 간의 통신은 요청-응답 형태로 동기화한다.
# 3. 무상태(statelessness) 통신: 서버에 대해 클라이언트가 하는 모든 요청에는
#    해당 서버가 그 요청을 처리하는 데 필요한 모든 정보가 꼭 있어야 한다.
#    서버는 진행 중인 상호작용에 관한 문맥(context)을 저장하지 않아야 하며,
#    섹션 상태는 클라이언트에 존재한다.
# 4. 일관된(uniform) 인터페이스 클라이언트와 서버에서는 유일한 식별자를 지닌
#    자원을 다룬다. 자원에 대해서는 생성, 변경, 검색, 삭제로 구성된 제한적인
#    인터페이스로 연산이 이뤄진다. 자원 요청의 결과는 응용 프로그램 상태에도
#    영향을 주는 파이퍼미디어 표현이다.

import re
import string
import sys

with open("../stop_words.txt") as f:
    stops = set(f.read().split(",") + list(string.ascii_lowercase))
# '데이터베이스'
data = {}


# '서버'측 응용 프로그램의 내부 함수
def error_state():
    return "Something wrong", ["get", "default", None]


# '서버' 측 응용 프로그램 처리자
def default_get_handler(args):
    rep = "What would you like to do?"
    rep += "\n1 - Quit" + "\n2 - Upload file"
    links = {"1": ["post", "execution", None], "2": ["get", "file_form", None]}
    return rep, links


def quit_handler(args):
    sys.exit("Goodbye cruel world...")


def upload_get_handler(args):
    return "Name of file to upload?", ["post", "file"]


def upload_post_handler(args):
    def create_data(filename):
        if filename in data:
            return
        word_freqs = {}
        with open(filename) as f:
            for w in [x.lower()
                      for x in re.split("[^a-zA-Z]+", f.read())
                      if len(x) > 0 and x.lower() not in stops]:
                word_freqs[w] = word_freqs.get(w, 0) + 1
        word_freqsl = word_freqs.items()
        word_freqsl.sort(lambda x, y: cmp(y[1], x[1]))
        data[filename] = word_freqsl

    if args == None:
        return error_state()
    filename = args[0]
    try:
        create_data(filename)
    except:
        return error_state()
    return word_get_handler([filename, 0])


def word_get_handler(args):
    def get_word(filename, word_index):
        if word_index < len(data[filename]):
            return data[filename][word_index]
        else:
            return ("no more words", 0)

    filename = args[0]
    word_index = args[1]
    word_info = get_word(filename, word_index)
    rep = "\n#{0}: {1} - {2}".format(word_index + 1, word_info[0], word_info[1])
    rep += "\n\nWhat would you like to do next?"
    rep += "\n1 - Quit" + "\n2 - Upload file"
    rep += "\n3 - See next most-frequently occurring word"
    links = {"1": ["post", "execution", None],
             "2": ["get", "file_form", None],
             "3": ["get", "word", [filename, word_index + 1]]}
    return rep, links


# 처리자 등록
handlers = {"post_execution": quit_handler,
            "get_default": default_get_handler,
            "get_file_form": upload_get_handler,
            "post_file": upload_post_handler,
            "get_word": word_get_handler}


# '서버' 핵심
def handle_request(verb, uri, args):
    def handler_key(verb, uri):
        return verb + "_" + uri

    if handler_key(verb, uri) in handlers:
        return handlers[handler_key(verb, uri)](args)
    else:
        return handlers[handler_key("get", "default")](args)


# 매우 간단한 클라이언트 '브라우저'
def render_and_get_input(state_representation, links):
    print state_representation
    sys.stdout.flush()
    if type(links) is dict:  # 여러 가지 가능한 다음 상태
        input = sys.stdin.readline().strip()
        if input in links:
            return links[input]
        else:
            return ["get", "default", None]
    elif type(links) is list:  # 유일하게 가능한 다음 상태
        if links[0] == "post":  # '폼' 데이터를 얻는다
            input = sys.stdin.readline().strip()
            links.append([input])
            return links
        else:  # 행동하지만 사용자 입력은 얻지 않는다
            return links
    else:
        return ["get", "default", None]


request = ["get", "default", None]
while True:
    # '서버' 쪽 계산
    state_representation, links = handle_request(*request)
    # '클라이언트' 쪽 계산
    request = render_and_get_input(state_representation, links)
