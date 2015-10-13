# -*- coding: utf-8 -*-
from collections import defaultdict, Counter
from functools import partial
import re
from codecs import open
from lingoist.core.Tup import Tup
from lingoist.fuzzy import alignment
from lingoist.core.io import SPACES_REGEX, tup_from, lines_from, line_to_word_sound, spaced_to_tuple
from lingoist.prob import markov_chain
from lingoist.sequence_metrics import logmarginal
from britfone.align import uniform_alignment, estimate_cost_fn, order_biased

DIR = 'C:/Users/Jose/project-workspace/britphone/'
FREQ_FILE, VOCAB_FILE, SEED_FILE = DIR + 'count_1w.txt', DIR + 'vocabulary.txt', DIR + 'britfone.0.1.0.main.csv'

EXPANSIONS_FILE, GUESSED = DIR + 'britfone.0.1.0.expansions.csv', DIR + 'britfone.guessed.csv'

def check_unlikely():
    seqs = tup_from(SEED_FILE, lambda line: line_to_word_sound(re.sub('\d+|\(|\)', '', line)))

    order, delta = 1, 1e-55
    mc = markov_chain(seqs.unzip()[0].map(tuple) >> set > Tup, order, delta)

    for w, s, lik in seqs.map(lambda (w, s): (w, s, logmarginal(w, mc, order))).sorted(lambda (w, s, lik): lik):
        print '%-20.20s %-20.20s %3.3f' % (''.join(w), ''.join(s), lik)

def unmerge_j(sound):
    spaced = ' '.join(sound)

    primary_stressed = re.sub(u'[ˈ]j', u' j ˈ', spaced)
    secondary_stress = re.sub(u'[ˌ]j', u' j ˌ', primary_stressed)
    unstressed = re.sub(u'(?=j[ʊu])j', u' j ', secondary_stress)

    return spaced_to_tuple(unstressed)

def unmerge_all_js():
    britfone = tup_from(SEED_FILE, line_to_word_sound)

    unmerged = []
    for w, s in britfone:
        unmerged.append('%s, %s' % (''.join(w), ' '.join(split_schwa_diphthongs(s))))
        # print unmerged.pop()

    collection_to(SEED_FILE+'x',unmerged)

def split_schwa_diphthongs(sound):
    split_ = []

    for phoneme in sound:
        if len(phoneme) in{ 2,3} and  phoneme[-1] == u'ə':
            split_.append(phoneme[:-1])
            split_.append(phoneme[-1])
        else:
            split_.append(phoneme)

    return Tup(split_)
def find_suspect_alignments(data=SEED_FILE+'x'):
    sounds_words = tup_from(data, lambda line: line_to_word_sound(re.sub('\d+|\(|\)', '', line))).map(lambda (w, s): (s, w)) >> set > Tup
    cost_fn, aligned = estimate_cost_fn(sounds_words, None, uniform_alignment(sounds_words))

    ob = order_biased(alignment.edit_with_sim)
    align_fn = lambda (s, w): ob(s, w, cost_fn)
    # .where(lambda (s, w, sim): sim >= .7) \
    count = 0
    for sound, word, d in sounds_words \
            .map(align_fn) \
            .sorted(lambda (s, w, sim): sim):
        count += 1
        print '%-20.20s %-20.20s %3.3f' % (''.join(word), ''.join(sound), d)

    print count

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
    britfone = set(lines_from(SEED_FILE, lambda line: line.split(',')[0].split('(')[0].strip()))
    expansions = set(lines_from(EXPANSIONS_FILE, lambda line: line.split('\t')[0].strip()))
    extant = britfone | expansions
    print len(extant)

    # frequency_sorted = lines_from(DIR + 'all.num', lambda line: re.split('\s+', line)[1].strip().upper())
    # frequency_sorted = lines_from(FREQ_FILE, lambda line: line.split('\t')[0].strip().upper())
    # frequency_sorted = lines_from(DIR+'wikipedia.csv', lambda line: re.split('\s+',line)[1].strip().upper())
    # frequency_sorted = lines_from(DIR + 'en.txt', lambda line: re.split('\s+', line)[0].strip().upper())
    frequency_sorted = lines_from(DIR + 'new_vocab.csv', lambda line: re.split('\s+', line)[0].strip().upper())
    vocab, OOV = set(), set()
    c = 0
    for i, w in enumerate(frequency_sorted):
        c = i
        # if w in google_ignore or w in bnc_ignore: continue
        # if re.match('^(\d+(,\d{3})?%?|&.+|2?1ST|2ND|3RD|\d{1,3}TH|19\d0S)$', w): continue
        # if (i < 5000): continue
        # if (i > 10000):
        #     break
        OOV.add(w)
        if w not in extant and '_' not in w:
            print i, ' ', w
            #     OOV.add(w)
            # elif u'_' in w:
            #     for which in w.split('_'):
            #         if which not in extant:
            #             print i, ' ', w
            #             OOV.add(w)
            # else:
            #     vocab.add(w)

    print c, len(OOV), len(vocab), len(extant)

    word_sound = lines_from(DIR + 'cmudict.ipa.csv', lambda line: [col.strip() for col in line.split(',')])
    # word_sound = lines_from(GUESSED, lambda line: [col.strip() for col in line.split(',')])

    word_to_sounds = defaultdict(set)
    for w, s in word_sound:
        word_to_sounds[w].add(s)

    f = open(DIR + 'xxxnew_vocab.csv', 'w', 'utf-8')
    for w in sorted(OOV):
        for s in word_to_sounds[w]:
            print '%s, %s' % (w, s)
            f.write('%s, %s\n' % (w, s.decode('utf-8')))

def checks_for_missing():
    britfone = set(lines_from(SEED_FILE, lambda line: line.split(',')[0].split('(')[0].strip()))
    expansions = set(lines_from(EXPANSIONS_FILE, lambda line: line.split('\t')[0].strip()))
    extant = britfone | expansions

    bnc = set(lines_from(DIR + 'all.num', lambda line: re.split('\s+', line)[1].strip().upper())[:10000])
    google = set(lines_from(FREQ_FILE, lambda line: line.split('\t')[0].strip().upper())[:10000])
    freqs = bnc | google

    vocab, OOV = set(), set()
    # for i, w in enumerate(freqs):
    #     if re.match('^(\d+(,\d{3})?%?|.+_.+|&.+|2?1ST|2ND|3RD|\d{1,3}TH|19\d0S)$', w): continue
    #     if w not in extant:
    #         OOV.add(w)

    for i, w in enumerate(extant):
        if w not in freqs:
            OOV.add(w)

    for w in sorted(OOV):
        print w

    print len(OOV)

def finds_multiples():
    word_sound = lines_from(SEED_FILE, lambda line: [col.strip() for col in line.split(',')])

    word_to_sounds = defaultdict(set)
    for w, s in word_sound:
        word_to_sounds[w].add(s)

    m = {w for w, sounds in word_to_sounds.iteritems() if len(sounds) > 1}

    for w in sorted(m): print w
    print len(m)

def resort(_file=None):
    lines = sorted(set(lines_from(_file, lambda line: line.strip().decode('UTF-8'))))

    collection_to(_file, lines)

def reformat_csv(_file=SEED_FILE):
    def tuplise(line):
        # print line.strip()
        word, sound = line.split(',')
        return tuple(re.sub('\s+', ' ', word).strip()), tuple(re.sub('\s+', ' ', sound.strip()).split(' '))

    word_sound = tup_from(_file, tuplise).map(lambda (w, s): '%s, %s' % (''.join(w), ' '.join(s)))
    collection_to(SEED_FILE, word_sound)

def spot_bad_characters(_file=SEED_FILE):
    lines = linesx_from(_file, lambda c: c.strip())
    chars = []

    for line in lines:
        for char in re.split('\s+',line):
            chars.append(char)
    for ch, c in Counter(chars).most_common():
        print '%s = %s' % (ch, c)

def linesx_from(file_name, pipe=lambda x: x, where=lambda count, line: True):
    lines = []

    with open(file_name, 'r', 'utf-8') as f:
        c = 0
        for line in f:
            if where(c, line):
                lines.append(pipe(line))
            c += 1

    return lines

def reformat_tsv(_file=EXPANSIONS_FILE):
    def tuplise(line):
        return tuple(tuple(re.sub('\s+', ' ', col).strip()) for col in line.split('\t'))

    word_sound = tup_from(_file, tuplise).map(lambda (w, s): '%s\t%s' % (''.join(w), ''.join(s)))
    collection_to(_file, word_sound)

def expansions_not_in_britfone():
    britfone = set(lines_from(SEED_FILE, lambda line: line.split(',')[0].strip()))
    expansions = set(lines_from(EXPANSIONS_FILE, lambda line: line.split('\t')[1].strip()))

    for e in expansions:
        for chunk in e.split(' '):
            if chunk not in britfone:
                print chunk, ' ', e

google_ignore = \
    {
        'RSS', 'URL', 'HTML', 'PDF',
        'USR', 'PRE', 'LOS', 'HP', 'EG',
        'TEL', 'IE', 'EST', 'GMT', 'MB', 'PREV', 'INT', 'USB', 'ED', 'PHP',
        'MSN', 'MIN', 'ISBN', 'PST', 'XXX', 'KB', 'VOL', 'PP', 'WWW', 'AU',
        'LLC', 'RD', 'MID', 'KM', 'DEL', 'IM', 'XP', 'CVS', 'LCD',
        'DJ', 'CM', 'HR', 'RW', 'VHS', 'NT', 'GB', 'BC', 'PR', 'FR', 'AA', 'VAR',
        'OZ', 'USD', 'MG', 'CH', 'DEVEL', 'RS', 'AVG', 'PDA', 'DSL', 'ZUM', 'SQL',
        'SS', 'SEXO', 'OP', 'ACC', 'CE', 'LIB', 'TM', 'SP', 'PDT',
        'PT', 'PSP', 'DS', 'EA', 'UND', 'LG', 'NW', 'FF', 'ISO', 'MISC', 'PS', 'BR', 'ML',
        'RES', 'CS', 'QUE', 'PUERTO', 'VOIP', 'SF', 'KG', 'CSS', 'UNIPROTKB', 'VON', 'EDT', 'PMID',
        'BA', 'PARA', 'CR', 'PG', 'KS', 'FTP', 'SW', 'HD', 'GCC', 'ASP', 'EXP', 'CPU', 'NR', 'DEF', 'NL',
        'EPA', 'TR', 'BB', 'NZ', 'HIST', 'VBULLETIN', 'AV', 'TION', 'NSW', 'PCI', 'RC', 'MPEG', 'RICO', 'CST',
        'HTTP', 'EC', 'RM', 'PDAS', 'API', 'CF', 'VT', 'URW', 'NEC', 'FOTO', 'XX', 'GM', 'RT', 'CP', 'DD',
        'AUD', 'PL', 'CRM', 'RF', 'TD', 'USC', 'TREMBL', 'NS', 'BS', 'HRS', 'CAL', 'IMG', 'TVS',
        'MHZ', 'LAT', 'GI', 'SUR', 'LL', 'CL', 'IEEE', 'GT', 'AE', 'NYC', 'HS', 'RIO', 'RV', 'STRUCT', 'RICA',
        'YR', 'IC', 'ZUA', 'ENT', 'MX', 'GR', 'XHTML', 'EXT', 'GE', 'NCAA', 'NG', 'PE', 'TT', 'XL', 'CAD', 'TCP',
        'DV', 'DIR', 'FY', 'GHZ', 'RR', 'TITTEN', 'EP', 'GBP', 'JP', 'AF', 'RFC', 'SL', 'SEO', 'ISP',
        'HP', 'JPG', 'SSL', 'MLB', 'GP', 'IR', 'OCLC', 'MSG', 'CV', 'CB', 'GEN', 'ESPN', 'NHL', 'FC',
        'FW', 'GS', 'BP', 'STD', 'OO', 'BBW', 'FDA', 'HDTV', 'TRI', 'NN', 'KDE', 'VB', 'PROC', 'FX', 'DL', 'ALT',
        'PHBB', 'LT', 'EQ', 'JE', 'LANG', 'UV', 'CMS', 'SG', 'VIC', 'PHYS', 'MEGA',
        'NAV', 'FA', 'IST', 'LC', 'LIL', 'SYS', 'ICQ', 'SCSI', 'CU', 'DNS', 'PTY', 'UNIV', 'NP', 'TFT',
        'JVC', 'TRAVESTI', 'DT', 'CGI', 'GC', 'CI', 'YN', 'KIJIJI', 'VII', 'CRF', 'PMC', 'NB', 'RX', 'GSM',
        'DDR', 'REC', 'PB', 'CHEM', 'OE', 'JD', 'GPL', 'IRC', 'DM', 'MLS', 'CET', 'PPC', 'JC', 'ONS', 'DIST',
        'XNXX', 'AVI', 'BDSM', 'RPG', 'PROT', 'TGP', 'LIVESEX', 'ARG', 'UR', 'GEO', 'WORLDSEX',
        'ATI', 'WAL', 'RNA', 'UC', 'BUF', 'LD', 'WEBSHOTS', 'MSGID', 'MF', 'MSGSTR', 'MW', 'NU', 'ICT',
        'DP', 'SKU', 'HT', 'ZA', 'PTS', 'RH', 'RRP', 'FG', 'OOO', 'HZ', 'BK', 'COMM', 'STE', 'MENT',
        'COL', 'DX', 'SK', 'BIOL', 'YU', 'SQ', 'OC', 'AJ', 'TREO', 'UNE', 'TEXS', 'SUBLIMEDIRECTORY', 'OM',
        'TP', 'JM', 'DPI', 'GIS', 'LOC', 'CN', 'VER', 'RN', 'DIS', 'CG', 'SER', 'HREF', 'FWD', 'AUS', 'ENDIF',
        'HWY', 'NAM', 'UNA', 'FT', 'SRC', 'AP', 'UTC', 'NH', 'QTY', 'BIO', 'VI', 'SB', 'SM', 'ZUS',
        'FOTOS', 'HB', 'TC', 'MINS', 'OEM', 'POR', 'MEM', 'IDE', 'PD', 'WP', 'YRS',
        'LYCOS', 'MINOLTA', 'MULTI', 'NANO', 'NIKON', 'POLY', 'RHODE', 'SALEM', 'SCOTIA',
        'SOLARIS', 'TIFFANY', 'TRIVIA', 'TROY', 'XANAX', 'ANGELES', 'DAS',
        'NI', 'DICKE', 'ELLIS', 'ENG', 'EPSON', 'FI', 'KLEIN', 'LANKA', 'LEXMARK',
        'MACROMEDIA', 'MENS', 'TEX', 'ING', 'CHILDRENS', 'AB', 'ABU', 'AC', 'AG', 'AKA', 'ALA', 'ATA', 'ATM',
        'BMW', 'BT', 'CBS', 'CC', 'CIA', 'DOW', 'DUI', 'FBI', 'FM', 'FS', 'GDP', 'GMBH', 'GPS', 'IO', 'IP', 'IRS',
        'KA', 'LN', 'MBA', 'MC', 'MH', 'MTV', 'NBA', 'NBC', 'OG', 'PC', 'PHD', 'POS', 'PSI', 'RPM', 'SAO', 'SAS', 'SCI',
        'SIE', 'UL', 'TY', 'VE', 'VP', 'VS', 'WS', 'XEROX', 'XML', 'YANG', 'ALOT',
        'ALTO', 'AMD', 'CALVIN', 'CDS', 'CEO', 'CHAN', 'CHEN', 'CNN', 'DK', 'DVD', 'DVDS',
        'EOS', 'HU', 'INS', 'ITALIA', 'ITALIANO', 'KO', 'LAS', 'LP', 'LS', 'MAI', 'MIT',
        'NEXTEL', 'NFL', 'OT', 'PASO', 'PCS', 'PIX', 'PPM', 'ROSA', 'SMS', 'SPARC', 'TAHOE',
        'TB', 'TS', 'URI', 'TULSA', 'ANAHEIM', 'BON', 'CARLO',
        'ISA', 'CAS', 'CASA', 'CASEY', 'CLARA', 'CORNELL', 'CREST', 'CURTIS', 'DANA', 'DEUTSCHE',
        'DEUTSCHLAND', 'DOM', 'EAU', 'EDMONTON', 'FAIRFIELD', 'GARCIA', 'GREENE',
        'GREENSBORO', 'GRENADA', 'GRIFFIN', 'HANS', 'HARLEY', 'HARPER', 'HARTFORD',
        'KENNY', 'KENO', 'KRUGER', 'LAFAYETTE', 'LAUDERDALE', 'LEON', 'LEONE',
        'LEU', 'LEXINGTON', 'LEXUS', 'LOGAN', 'LOLITA', 'LUIS', 'MARDI', 'MARCO',
        'MAS', 'MAUI', 'MESA', 'METALLICA', 'MONTE', 'NEWARK', 'NEWFOUNDLAND',
        'PAC', 'PAS', 'PETERSON', 'PROZAC', 'REID', 'REYNOLDS', 'RICHARDSON',
        'ROBERTSON', 'SHAKIRA', 'SHANNON', 'SHERMAN', 'SMITHSONIAN', 'STAN',
        'VERDE', 'VERNON', 'WALT', 'WHATS', 'WINSTON', 'YUKON', 'WANG', 'WU', 'PONTIAC', 'JESSE', 'DAT',
        'CZECHOSLOVAKIA', 'HERBERT', 'ISABEL', 'LAMONT', 'ROBYN',
        'BELKIN', 'BETH', 'SINGH', 'KAI', 'UK', 'PHENTERMINE', 'IBM',
        'SITEMAP', 'PUBMED', 'TRIPADVISOR', 'VERZEICHNIS', 'WEBLOG',
        'EPINIONS', 'CONST', 'DONT', 'HOLDEM', 'SEXCAM', 'MILFHUNTER',
        'BEASTIALITY', 'SHEMALE', 'TRACKBACK', 'ABC', 'LIVECAM', 'MEDLINE',
        'DEBIAN', 'MP', 'POSTPOSTED', 'CIALIS', 'CITYSEARCH', 'TWIKI', 'CONFIG',
        'WISHLIST', 'CUMSHOTS', 'NUTTEN', 'EMINEM', 'PLUGIN', 'DEALTIME',
        'GAMECUBE', 'TRAMADOL', 'JELSOFT', 'SLIDESHOW', 'PLC', 'THATS', 'ASIN',
        'EXPANSYS', 'FILENAME', 'PHPBB', 'UPSKIRTS', 'UTILS', 'VERIZON', 'SIGNUP',
        'WORDPRESS', 'GAMESPOT', 'CFR', 'STARSMERCHANT', 'MYSPACE', 'LEVITRA',
        'AMPLAND', 'SHOPZILLA', 'FREEBSD', 'THUMBZILLA', 'TRANSEXUALES',
        'PICHUNTER', 'PROSTORES', 'ZOPE', 'DIY', 'SUSE', 'ADIPEX', 'KELKOO', 'THEHUN',
        'IPAQ', 'NHS', 'DOD', 'VIEWPICTURE', 'ANDALE',
        'TRACKBACKS', 'FINDLAW', 'GBA', 'BM', 'HOWTO',
        'STR', 'SHEMALES', 'VIP', 'RJ', 'SOC', 'VOYEURWEB',
        'LOGITECH', 'DEM', 'WAV', 'GRATUIT', 'RP', 'TBA',
        'USGS', 'HC', 'RCA', 'FP', 'HYDROCODONE', 'GST', 'MAILTO',
        'JJ', 'OBJ', 'DANS', 'METADATA', 'DEPT', 'DANS',
        'RL', 'ERP', 'GL', 'UI', 'DH', 'VPN', 'FCC', 'EDS',
        'DF', 'ZSHOPS', 'ACDBENTITY', 'AMBIEN', 'WORLDCAT',
        'CDT', 'EZ', 'PF', 'UW', 'BD', 'BANGBUS', 'EVAL',
        'MUZE', 'GMC', 'HH', 'ADSL', 'FD', 'ASN', 'LISTPRICE',
        'LIBS', 'PK', 'SAGEM', 'KNOWLEDGESTORM', 'INF',
        'VCR', 'PCT', 'WB', 'SN', 'QLD', 'FINDARTICLES', 'ISSN', 'BLAKE',
        'MYSIMON', 'OECD', 'HANSEN', 'WOMENS', 'CUMSHOT', 'BIZRATE', 'PLUGINS',
        'WEBLOGS', 'FIREWIRE', 'MODS', 'VSNET', 'MSIE', 'WN', 'CCD', 'SV', 'ZU',
        'LLP', 'BOC', 'DG', 'ASUS', 'TECHREPUBLIC', 'VG', 'FILME', 'FO', 'TMP', 'OL',
        'JS', 'PN', 'NVIDIA', 'INCL', 'HQ', 'PROPECIA', 'WT', 'MV', 'CARB', 'CIO', 'RUNTIME', 'DSC',
        'RB', 'UPC', 'KINASE', 'PVC', 'FEOF', 'USDA', 'URLS', 'ENB', 'GG', 'INVISION',
        'EMACS', 'WTO', 'WW', 'GD', 'BASENAME', 'BW', 'MJ', 'CINGULAR', 'LF', 'BUFING',
        'WC', 'SBJCT', 'HK', 'POWERSELLER', 'CJ', 'NAMESPACE', 'CHANGELOG', 'QC',
        'PGP', 'TF', 'PJ', 'CW', 'WR', 'FIORICET', 'RG', 'BL', 'VC', 'WX', 'FRONTPAGE',
        'PAXIL', 'NTSC', 'APNIC', 'USPS', 'BG', 'SEQ', 'CONF', 'WMA', 'CIR',
        'LOOKSMART', 'ACM', 'KW', 'IPS', 'GTK', 'VOYUER', 'GARMIN', 'RICHARDS', 'MRNA', 'TIONS', 'QT',
        'CDNA', 'MEYER', 'SOA', 'LU', 'BEASTALITY', 'MICHEL', 'NOTRE', 'KIRK', 'CHO', 'BOOL', 'IND', 'BBS', 'QUI',
        'ULTRAM', 'ZOLOFT', 'CZ', 'HL', 'OB', 'IDG', 'CTRL', 'ROBBIE', 'NEWMAN', 'INTL', 'SLR', 'VAIO', 'RFID', 'IDS',
        'WUKET', 'JOHNSTON', 'MEDIAWIKI', 'LM', 'SMTP', 'SEN', 'DTS',
        'CARMEN', 'MORRISON', 'MYRTLE', 'ROLAND', 'WEBSTER', 'TELECHARGER', 'HUGO', 'WAGNER',
        'KEYNES', 'GAULLE', 'MUCOSA', 'HEWLETT-PACKARD',
        'EMAILINC', 'EEC', 'CLAUDIA', 'DOYLE', 'FRANCO', 'W.L.R.', 'ITV', 'HILARY',
        'GOULD', 'MACMILLAN', 'LIGHTBOX', 'WORDSWORTH', 'TWENTY-FOUR',
    }

bnc_ignore = \
    {
        'BBC', 'DNA', 'HIV', 'IRA', 'K', 'PH', 'TH', 'USA', 'CD', 'DA', 'DC', 'SRI', "ONE'S", 'PM',
        "N'T", 'ERM', 'GON', 'MPS', 'USSR', 'AND/OR', "D'", 'Q.V.', 'GEN.', 'REAGAN', 'ICI',
        'TWO-THIRDS', 'TWENTY-FIVE', 'ORD', 'E.R', 'UX', '2.5', 'A.C.',
        'ROS', '3.1', 'Q.V', 'REX', 'CROHN', 'ONE-THIRD', 'JULIUS',
        'JENKINS', 'STOCKTON', 'FERGUSON', 'DEXTER', 'ANGLIA',
        'MIDLAND', 'NEVILLE', 'HUSSEIN', 'GILES',
        'HESELTINE', 'ATHELSTAN', 'MEREDITH', 'SHARPE', 'BALDWIN',
        'OESOPHAGEAL', 'COLONIC', 'MIDFIELD',
        'MORTON', 'NICHOLSON', 'PATTEN', 'MEG',
        'ULCERATIVE'

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
    # checks_for_missing()
    # vocabulary2()
    # finds_multiples()
    # resort(EXPANSIONS_FILE)
    # reformat_csv()
    # reformat_tsv()
    # spot_bad_characters()
    # expansions_not_in_britfone()
    # check_unlikely()
    find_suspect_alignments()
    # unmerge_all_js()