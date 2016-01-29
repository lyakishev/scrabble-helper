# -*- coding: utf-8 -*-

import re
import os
from operator import itemgetter

from bottle import route, run, request, static_file


ROOT = os.path.dirname(os.path.abspath(__file__))


COSTS = {
    u'а': 1,
    u'б': 3,
    u'в': 1,
    u'г': 3,
    u'д': 2,
    u'е': 1,
    u'ё': 3,
    u'ж': 5,
    u'з': 5,
    u'и': 1,
    u'й': 4,
    u'к': 2,
    u'л': 2,
    u'м': 2,
    u'н': 1,
    u'о': 1,
    u'п': 2,
    u'р': 1,
    u'с': 1,
    u'т': 1,
    u'у': 2,
    u'ф': 10,
    u'х': 5,
    u'ц': 5,
    u'ч': 5,
    u'ш': 8,
    u'щ': 10,
    u'ъ': 10,
    u'ы': 4,
    u'ь': 3,
    u'э': 8,
    u'ю': 8,
    u'я': 3
}


with open('dicts/zdb.txt') as f:
    WORDS = [word.decode('utf8').strip() for word in f]


def get_word_cost_if_match(word, letters, dots):
    word_len = len(word)
    cost = 0
    for c in letters:
        word = word.replace(c, '', 1)
        new_word_len = len(word)
        if new_word_len < word_len:
            cost += COSTS[c]
        if not word:
            break
        word_len = new_word_len

    if len(word) <= dots:
        return cost


def find_words(letters, board_string):
    dots = letters.count('.')
    min_len = len(board_string) + 1
    max_len = len(letters) + min_len - 1
    letters = letters.replace('.', '')
    re_board = re.compile(board_string) if '.' in board_string else None

    for word in WORDS:
        word_len = len(word)
        if word_len < min_len or word_len > max_len:
            continue

        if re_board:
            matched_strings = set()
            for i in range(len(word)):
                match = re_board.match(word[i:])
                if match:
                    matched_string = match.group(0)
                    if matched_string in matched_strings:
                        continue
                    matched_strings.add(matched_string)
                    test_word = word.replace(matched_string, '', 1)
                    cost = get_word_cost_if_match(test_word, letters, dots)
                    if cost is not None:
                        yield word, cost, matched_string
        else:
            test_word = word

            if board_string:
                test_word = test_word.replace(board_string, '', 1)
                if len(test_word) == len(word):
                    continue

            cost = get_word_cost_if_match(test_word, letters, dots)
            if cost is not None:
                cost += sum(COSTS[c] for c in board_string)
                yield word, cost, board_string


@route('/')
def index():
    return static_file('index.html', root=os.path.join(ROOT, 'templates'))


@route('/static/<filename>')
def static(filename):
    return static_file(filename, root=os.path.join(ROOT, 'static'))


@route('/words/')
def get_words():
    letters = request.query['letters'].decode('utf8')
    board_strings = request.query['board_strings'].decode('utf8').split(' ')
    words = sorted((word for board_string in board_strings
                    for word in find_words(letters, board_string)),
                   key=itemgetter(1, 0), reverse=True)
    from bottle import response
    from json import dumps
    response.content_type = 'application/json'
    return dumps({'data': [{'word': word, 'cost': cost, 'onboard': onboard}
                           for word, cost, onboard in words]})


run(host='0.0.0.0', port=8080)
