# -*- coding: utf-8 -*-

import os
from operator import itemgetter

from bottle import route, run, template, request, static_file


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


def find_words(letters, board_string):
    dots = letters.count('.')
    min_len = len(board_string) + 1
    max_len = len(letters) + min_len - 1
    letters = letters.replace('.', '')

    for word in WORDS:
        word_len = len(word)

        if word_len > max_len or word_len < min_len:
            continue

        test_word = word
        if board_string:
            test_word = test_word.replace(board_string, '', 1)
            if len(test_word) == len(word):
                continue

        for c in letters:
            test_word = test_word.replace(c, '', 1)
            if not test_word:
                break

        if len(test_word) <= dots:
            yield word


@route('/')
def index():
    return template('templates/index.html')


@route('/static/<filename>')
def static(filename):
    return static_file(
        filename,
        root=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'static'))


def get_word_cost(word, letters, board_letters):
    cost = sum(COSTS.get(c, 0) for c in board_letters)
    word = word.replace(board_letters, '', 1)
    for c in word:
        if c in letters:
            cost += COSTS.get(c, 0)
            letters = letters.replace(c, '', 1)
    return cost


@route('/words/')
def get_words():
    my_letters = request.query['my_letters'].decode('utf8')
    board_letters = request.query['board_letters'].decode('utf8')
    words = [[word, get_word_cost(word, my_letters, board_letters)]
             for word in find_words(my_letters, board_letters)]
    words.sort(key=itemgetter(1), reverse=True)
    from bottle import response
    from json import dumps
    response.content_type = 'application/json'
    return dumps(words)

run(host='0.0.0.0', port=8080)
