# -*- coding: utf-8 -*-
import re
from codecs import open
import lingoist.core.prints as prints
from lingoist.core.Tup import Tup
from lingoist.core.Seq import Seq
from lingoist.core.io import SPACES_REGEX, tup_from, line_to_word_word, line_to_word_sound, \
    line_to_sound_sound, lines_from
from lingoist.fuzzy.base import GAP

DIR = 'C:/Users/Jose/project-workspace/britphone/'
FREQ_FILE, VOCAB_FILE, SEED_FILE = DIR + 'all.num', DIR + 'vocabulary.txt', DIR + 'britfone.0.1.0.main.csv'

def vocabulary(cmudict_seed=DIR + 'cmudict.ipa.csv', britfone_seed=SEED_FILE, frequency_list=FREQ_FILE,
               vocabulary=VOCAB_FILE):
    cmudict = set(lines_from(cmudict_seed, lambda line: line.split(',')[0].strip().upper()))
    britfone = set(lines_from(britfone_seed, lambda line: line.split(',')[0].strip().upper()))
    expansions = set(lines_from(DIR + 'britfone.0.1.0.expansions.csv', lambda line: line.split(',')[0].strip().upper()))

    frequency_sorted = tup_from(frequency_list, lambda line: SPACES_REGEX.split(line)[1].strip().upper())

    vocab, OOV = set(), set()
    for w in frequency_sorted:
        if '_' in w or \
                re.match(
                    '^(2?1ST|2ND|3RD|\d{1,3}TH|\-?\d+|I{2,}|IV|VI+|19\d0S|(&POUND;)?\d{1,3},\d{3}|&POUND;\d+|\d+%|\d+\.\d+)$',
                    w) or \
                        w in unknown: continue

        if len(vocab) == 10000: break
        is_in = False
        for a in abbreviations.get(w, {}):
            vocab.add(a)
            is_in = True
        if mistyped.get(w, None):
            vocab.add(mistyped[w])
            is_in = True

        vars = [w, w.replace('-', ''), w.replace('ISE', 'IZE'), w.replace('ISA', 'IZA'), w.replace('ISI', 'IZI'),
                w.replace('YSI', 'YZI'), w.replace('YSE', 'YZE'),
                w.replace('OUR', 'OR'), w.replace('TRE', 'TER')]
        no_vars = True
        for v in vars:
            if v not in cmudict and v not in britfone and v not in expansions and not is_in:
                pass
            else:
                no_vars = False
                break
        if not no_vars:
            vocab.add(w)
        else:
            if re.match('^[A-Z]+$', w): print v
            OOV.add(w)

    print len(OOV)
    print len(vocab)

    # collection_to(vocabulary, sorted(vocab))

def collection_to(file_name, items):
    with open(file_name, 'w', 'utf-8') as _file:
        for item in items:
            _file.write('%s\n' % (item))

abbreviations = \
    {
        "N'T": {'NOT'},
        "'VE": {'HAVE'},
        "'RE": {'ARE'},
        "'LL": {'WILL', 'SHALL'},
        "'D": {'WOULD', 'HAD'}
    }

unknown = {'GON', '&FORMULA', "D'", "'E", '&AGR', '&BGR', 'AT&AMP;T'}
mistyped = {'&AMP': 'AND', '&TIMES': 'TIMES', u'*': 'STAR', u'&POUND;1': u'£', u'=': 'EQUALS', u'+': 'PLUS',
            "'": 'QUOTE', '%': 'PERCENT', '&FRAC12': 'HALF', '/': 'SLASH', 'CAF&EACUTE': 'CAFE'}

if __name__ == '__main__':
    vocabulary()
