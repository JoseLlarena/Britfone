## Britfone



British English (RP/Standard Southern British ) pronunciation dictionary:

* +12,000 entries including the top 10,000 most frequent words as per [BNC](http://www.kilgarriff.co.uk/bnc-readme.html)
 and [Google Web Corpus](http://norvig.com/ngrams)
* IPA transcription including primary and secondary stress
* MIT license
* separate expansion dictionary spelling out punctuation and abbreviations
* both American and British spelling variants

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

Stress marks are attached to the stressed vowel.

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
## Issues


* **strict IPA versus traditional phonetic symbols**: the phonetic symbols are strictly as defined by the IPA, as opposed to how
they have traditionally been used in the linguist literature. In particular:

  ** /ɐ/ instead of traditional /ʌ/
  ** /ɹ/ instead of traditional /r/
  ** /ɛ/ instead of traditional /e/
  ** /ɜː/ instead of traditional /əː/

* **unstressed vowels as  /ə/ and  /ɪ/**: due to the diversity of the sources for phonetic transcription, there's a fair amount of inconsistency in how weak vowels
 are transcribed. See the wikipedia discussion of [weak-vowel merger] (https://en.wikipedia.org/wiki/Phonological_history_of_English_high_front_vowels#Weak-vowel_merger)

* **final _i_**: final _i's_ are given the 'long i' /iː/ phoneme to reflect [happy-tensing](https://en.wikipedia.org/wiki/Phonological_history_of_English_high_front_vowels#Happy-tensing), even
though some dictionaries show a tense but short /i/, different from both /iː/ and /ɪ/ ([see wikipedia discussion](https://en.wikipedia.org/wiki/English_phonology)).

* **secondary stress**: secondary stress is not always marked (the primary always is).

* **stems and inflections**: not all inflected words have all their inflected variants, and not all variants show all of the alternative pronunciations. The possesive form _-'s_
of nouns is not included.

* **Acronyms vs initialisms**: The expansions' dictionary only contains _acronyms_, i.e., words that are _not_ pronounced by spelling
 out the individual letters, i.e.,  _initialisms_ (e.g. _BBC_, _NHS_) are excluded. The pronunciation of these can
 be obtained by looking up the [names of the individual letters](https://en.wikipedia.org/wiki/English_alphabet)
 in the main dictionary, then concatenating them.

## Sources

The initial source of the phonetic transcriptions is cmudict, plus a number of online sources for specifics of British English.
The main sources of the word frequency-filtered vocabulary are the top 10K in the British National Corpus and the Google Web Corpus. Not all words in this list are included
since due to sampling bias there uncommon words like _ATHELSTAN_ or _PHENTERMINE_, as well as foreign words. Also excluded are initialisms.


## MIT License (MIT)

Copyright (c) 2015 by Jose Llarena

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