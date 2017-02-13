## Britfone



British English (RP/Standard Southern British ) pronunciation dictionary:

* +16,000 entries including the top 10,000 most frequent words as per [BNC](http://www.kilgarriff.co.uk/bnc-readme.html)
 and [Google Web Corpus](http://norvig.com/ngrams)
* IPA transcription including primary and secondary stress
* MIT license
* separate expansion dictionary spelling out punctuation and abbreviations
* both American and British spelling variants
* all UK counties
* all London boroughs
* all major UK towns
* all common irregular plurals
* all common irregular verbs

## Format

The main dictionary's words are in upper case, comma-separated from their space-separated pronunciation. For words
with multiple pronunciations, a parenthesised number is attached to the end:

```
RAINBOW, ɹ ˈeɪ n b ˌəʊ
RAINING, ɹ ˈeɪ n ɪ ŋ
RAISE, ɹ ˈeɪ z
RAISED, ɹ ˈeɪ z d
RAISES, ɹ ˈeɪ z ɪ z
RAISING, ɹ ˈeɪ z ɪ ŋ
RAISINS, ɹ ˈeɪ z ɪ n z
RALEIGH(1), ɹ ˈɑː l iː
RALEIGH(2), ɹ ˈɔː l iː
```

Stress marks are attached to the stressed vowel/diphthong.

In the expansions dictionary entries are also in upper case, tab-separated from their expansions:


```
MON	MONDAY(1)
MON.	MONDAY(1)
MPG	MILES PER(1) GALLON
MPH	MILES PER(1) HOUR
MR	MISTER
MR.	MISTER
MRS	MISSIS
MRS.	MISSIS
```
## Issues and remarks


* **strict IPA versus traditional phonetic symbols**: the phonetic symbols are strictly as defined by the IPA, as opposed to how
they have traditionally been used in many dictionaries and the language learning literature. In particular:

  - /ɐ/ instead of traditional /ʌ/
  - /ɹ/ instead of traditional /r/
  - /ɛ/ instead of traditional /e/
  - /ɜː/ instead of traditional /əː/

* **unstressed vowels as /ə/ and /ɪ/**: due to the diversity of the sources for phonetic transcription, there's some inconsistency in how [weak vowels](https://en.wikipedia.org/wiki/Phonological_history_of_English_high_front_vowels#Weak-vowel_merger)
 are transcribed, though in most cases /ɪ/ is used, following the Collins Dictionary.

* **final _i_**: final unstressed _i's_ are given the "long i" /iː/ phoneme to reflect [happy-tensing](https://en.wikipedia.org/wiki/Phonological_history_of_English_high_front_vowels#Happy-tensing). However
most dictionaries show either a tense but [short /i/](https://en.wikipedia.org/wiki/English_phonology), different from both /iː/ and /ɪ/, or the short tense /ɪ/. The plan is to represent this sound separately as /i/ in the next version of Britfone.
Additionally, there's some inconsistency in the transcription as happy-tensing is preserved in inflected variants in spoken English (e.g., _studied_ derives it from _study_, and it contrasts with _studded_) yet this is not always reflected in the dictionary.

* **secondary stress**: secondary stress is not always marked (the primary always is).

* **stems and inflections**: not all inflected open-class words (noun, verbs, adjectives and adverbs) have all their inflected variants, and not all variants show all of the alternative pronunciations. The possessive form _-'s_
of nouns is not included, and neither is the superlative form of most adjectives and adverbs.

* **acronyms vs initialisms**: The expansions dictionary only contains _acronyms_, i.e., words that are _not_ pronounced by spelling
 out the individual letters, i.e.,  _initialisms_ (e.g. _BBC_, _NHS_) are excluded. The pronunciation of these can
 be obtained by looking up the [names of the individual letters](https://en.wikipedia.org/wiki/English_alphabet)
 in the main dictionary, then concatenating them.

## Sources

The initial source of the phonetic transcriptions is [cmudict](https://github.com/cmusphinx/cmudict), plus a number of other sources for British English specifics: Wiktionary, Wikipedia, the Collins Dictionary, the Oxford Dictionary, the Cambridge Dictionary and the MacMillan Dictionary.

The main sources of the word frequency-filtered vocabulary are the top 10K in the British National Corpus, the Google Web Corpus and the New General Service Lists. Not all words in these lists are included
since due to sampling bias there are uncommon words like _athelstan_ or _phentermine_, as well as foreign words. Also excluded are initialisms.

## Changelog

See commit history

## MIT License (MIT)

Copyright (c) 2017 by Jose Llarena

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.