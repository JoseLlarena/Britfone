# -*- coding: utf-8 -*-
from collections import defaultdict
import re
from codecs import open

from lingoist.core.io import SPACES_REGEX, tup_from, lines_from, line_to_word_sound

DIR = 'C:/Users/Jose/project-workspace/britphone/'
FREQ_FILE, VOCAB_FILE, SEED_FILE = DIR + 'count_1w.txt', DIR + 'vocabulary.txt', DIR + 'britfone.0.1.0.main.csv'

EXPANSIONS_FILE, GUESSED = DIR + 'britfone.0.1.0.expansions.csv', DIR + 'britfone.guessed.csv'

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

# FOO 8070 was last
def vocabulary2():
    britfone = set(lines_from(SEED_FILE, lambda line: line.split(',')[0].split('(')[0].strip().upper()))
    expansions = set(lines_from(EXPANSIONS_FILE, lambda line: line.split(',')[0].split('(')[0].strip().upper()))
    extant = britfone | expansions

    frequency_sorted = lines_from(FREQ_FILE, lambda line: line.split('\t')[0].strip().upper())

    vocab, OOV = set(), set()
    c = 0
    for i, w in enumerate(frequency_sorted):

        if w in google_ignore: continue

        if (len(OOV) + len(extant)) >= 10000:
            c = i
            break
        if w not in extant:
            # print i,' ' , w
            OOV.add(w)
        else:
            vocab.add(w)

    print c, len(OOV), len(vocab), len(extant)

    word_sound = lines_from(DIR+'cmudict.ipa.csv', lambda line: [col.strip() for col in line.split(',')])

    word_to_sounds = defaultdict(set)
    for w, s in word_sound:
        word_to_sounds[w].add(s)

    f = open(DIR+'new_vocab.csv', 'w', 'utf-8')
    for w in sorted(OOV):
        for s in word_to_sounds[w]:
            print '%s, %s' % (w, s)
            f.write('%s, %s\n' % (w, s.decode('utf-8')))

def finds_multiples():
    word_sound = lines_from(SEED_FILE, lambda line: [col.strip() for col in line.split(',')])

    word_to_sounds = defaultdict(set)
    for w, s in word_sound:
        word_to_sounds[w].add(s)

    m = {w for w, sounds in word_to_sounds.iteritems() if len(sounds) > 1}

    for w in sorted(m): print w
    print len(m)

def merge_entries():
    new_word_sound = set(
        lines_from(DIR + 'xxxnew_vocab.csv', lambda line: tuple(col.strip() for col in line.split(','))))
    old_word_sound = set(
        lines_from(DIR + 'britfone.0.1.0.main.csv', lambda line: tuple(col.strip() for col in line.split(','))))
    word_sound = new_word_sound | old_word_sound

    collection_to(DIR + 'britfone.0.1.0.main.merged.csv', sorted({'%s, %s' % (word, sound.decode('utf-8')) for word, sound in word_sound}))

google_ignore = \
    {
        'OCT', 'NOV', 'RSS', 'MAR', 'URL', 'APR', 'JUL', 'JUN', 'HTML', 'NY', 'EUR', 'PDF',
        'USR', 'MON', 'PRE', 'FRI', 'WED', 'CNET', 'LOS', 'HP', 'EG', 'TUE', 'THU',
        'TEL', 'TX', 'IE', 'EST', 'GMT', 'MD', 'FL', 'MB', 'PREV', 'IL', 'INT', 'USB', 'ED', 'PHP',
        'MSN', 'MIN', 'ISBN', 'AZ', 'PST', 'XXX', 'KB', 'VOL', 'PP', 'OS', 'XBOX', 'WWW', 'AU',
        'NC', 'LLC', 'VA', 'RD', 'SC', 'MID', 'KM', 'DEL', 'IM', 'XP', 'CVS', 'EU', 'LCD', 'AVE',
        'DJ', 'CM', 'WI', 'NJ', 'HR', 'RW', 'VHS', 'NT', 'GB', 'BC', 'PR', 'FR', 'AA', 'VAR',
        'OZ', 'USD', 'MG', 'CH', 'SD', 'DEVEL', 'RS', 'AVG', 'SC', 'PDA', 'DSL', 'ZUM', 'SQL',
        'SS', 'SEXO', 'NM', 'ND', 'OP', 'ACC', 'TN', 'CE', 'LIB', 'TM', 'SP', 'MYSQL', 'PDT', 'DB',
        'IA', 'PT', 'PSP', 'DS', 'EA', 'UND', 'LG', 'NW', 'FF', 'ISO', 'MISC', 'PS', 'KY', 'BR', 'ML',
        'RES', 'CS', 'QUE', 'PUERTO', 'VOIP', 'SF', 'KG', 'UT', 'CSS', 'UNIPROTKB', 'VON', 'EDT', 'PMID',
        'BA', 'PARA', 'CR', 'PG', 'KS', 'FTP', 'SW', 'HD', 'GCC', 'ASP', 'NV', 'EXP', 'CPU', 'NR', 'DEF', 'NL',
        'EPA', 'TR', 'BB', 'NZ', 'HIST', 'VBULLETIN', 'AV', 'TION', 'NSW', 'PCI', 'RC', 'MPEG', 'RICO', 'CST',
        'HTTP', 'EC', 'RM', 'PDAS', 'API', 'CF', 'VT', 'URW', 'NEC', 'FOTO', 'XX', 'GM', 'RI', 'RT', 'CP', 'DD',
        'AUD', 'PL', 'CRM', 'RF', 'AK', 'TD', 'USC', 'TREMBL', 'WV', 'NS', 'BS', 'HRS', 'CAL', 'IMG', 'TVS',
        'MHZ', 'LAT', 'GI', 'SUR', 'LL', 'CL', 'IEEE', 'GT', 'AE', 'NYC', 'HS', 'RIO', 'RV', 'STRUCT', 'RICA',
        'YR', 'IC', 'ZUA', 'ENT', 'MX', 'GR', 'XHTML', 'EXT', 'GE', 'NCAA', 'NG', 'PE', 'TT', 'XL', 'CAD', 'TCP',
        'DV', 'DIR', 'FLICKR', 'FY', 'GHZ', 'RR', 'TITTEN', 'EP', 'GBP', 'JP', 'AF', 'RFC', 'SL', 'SEO', 'ISP',
        'HP', 'JPG', 'SSL', 'MLB', 'GP', 'IR', 'ZDNET', 'OCLC', 'MSG', 'CV', 'CB', 'GEN', 'ESPN', 'NHL', 'FC',
        'FW', 'GS', 'BP', 'STD', 'OO', 'BBW', 'FDA', 'HDTV', 'TRI', 'NN', 'KDE', 'VB', 'PROC', 'FX', 'DL', 'ALT',
        'PENN', 'PHBB', 'HON', 'EBOOK', 'SEPT', 'LT', 'EQ', 'JE', 'LANG', 'UV', 'CMS', 'SG', 'VIC', 'PHYS', 'MEGA',
        'NAV', 'FA', 'IST', 'LC', 'LIL', 'SYS', 'ICQ', 'SCSI', 'CU', 'DNS', 'PTY', 'SOX', 'UNIV', 'NP', 'TFT',
        'JVC', 'TRAVESTI', 'DT', 'CGI', 'GC', 'CI', 'YN', 'KIJIJI', 'VII', 'CRF', 'PMC', 'NB', 'RX', 'GSM',
        'DDR', 'REC', 'PB', 'CHEM', 'OE', 'JD', 'GPL', 'IRC', 'DM', 'MLS', 'CET', 'PPC', 'JC', 'ONS', 'DIST',
        'XNXX', 'AVI', 'BDSM', 'RPG', 'PROT', 'TGP', 'LIVESEX', 'ARG', 'UR', 'GEO', 'WORLDSEX', 'JPEG',
        'ATI', 'WAL', 'RNA', 'UC', 'BUF', 'LD', 'WEBSHOTS', 'MSGID', 'MF', 'MSGSTR', 'MW', 'NU', 'ICT',
        'DP', 'XI', 'SKU', 'HT', 'ZA', 'PTS', 'RH', 'RRP', 'FG', 'OOO', 'HZ', 'BK', 'COMM', 'STE', 'MENT',
        'COL', 'DX', 'SK', 'BIOL', 'YU', 'SQ', 'OC', 'AJ', 'TREO', 'UNE', 'TEXS', 'SUBLIMEDIRECTORY', 'OM',
        'TP', 'JM', 'DPI', 'GIS', 'LOC', 'CN', 'VER', 'RN', 'DIS', 'CG', 'SER', 'HREF', 'FWD', 'AUS', 'ENDIF',
        'HWY', 'NAM', 'IX', 'UNA', 'FT', 'SRC', 'AP', 'MN', 'UTC', 'NH', 'QTY', 'BIO', 'VI', 'SB', 'SM', 'ZUS',
        'FOTOS', 'HB', 'TC', 'MINS', 'OEM', 'POR', 'MEM', 'IDE', 'PD', 'WP', 'YRS',
        'LYCOS', 'MINOLTA', 'MULTI', 'NANO', 'NIKON', 'POLY', 'RHODE', 'SALEM', 'SCOTIA',
        'SOLARIS', 'TIFFANY', 'TRIVIA', 'TROY', 'XANAX','ANGELES','DAS',
        'NI','DICKE','ELLIS','ENG','EPSON','FI','KLEIN','LANKA','LEXMARK',
        'MACROMEDIA','MENS','TEX','ING'

    }

def collection_to(file_name, items):
    with open(file_name, 'w', 'utf-8') as _file:
        for item in items:
            _file.write('%s\n' % item)

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
    vocabulary2()
    # finds_multiples()
    # merge_entries()
