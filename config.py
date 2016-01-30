# -*- coding: utf-8 -*-

import os


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
