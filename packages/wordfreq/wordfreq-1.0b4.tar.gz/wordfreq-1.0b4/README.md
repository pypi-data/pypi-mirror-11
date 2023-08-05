Tools for working with word frequencies from various corpora.

Author: Rob Speer

## Installation

wordfreq requires Python 3 and depends on a few other Python modules
(msgpack-python, langcodes, and ftfy). You can install it and its dependencies
in the usual way, either by getting it from pip:

    pip3 install wordfreq

or by getting the repository and running its setup.py:

    python3 setup.py install

To handle word frequency lookups in Japanese, you need to additionally install
mecab-python3, which itself depends on libmecab-dev. These commands will
install them on Ubuntu:

    sudo apt-get install mecab-ipadic-utf8 libmecab-dev
    pip3 install mecab-python3

## Unicode data

The tokenizers used to split non-Japanese phrases use regexes built using the
`unicodedata` module from Python 3.4, which uses Unicode version 6.3.0.  To
update these regexes, run `scripts/gen_regex.py`.

## License

`wordfreq` is freely redistributable under the MIT license (see
`MIT-LICENSE.txt`), and it includes data files that may be
redistributed under a Creative Commons Attribution-ShareAlike 4.0
license (https://creativecommons.org/licenses/by-sa/4.0/).

`wordfreq` contains data extracted from Google Books Ngrams
(http://books.google.com/ngrams) and Google Books Syntactic Ngrams
(http://commondatastorage.googleapis.com/books/syntactic-ngrams/index.html).
The terms of use of this data are:

    Ngram Viewer graphs and data may be freely used for any purpose, although
    acknowledgement of Google Books Ngram Viewer as the source, and inclusion
    of a link to http://books.google.com/ngrams, would be appreciated.

It also contains data derived from the following Creative Commons-licensed
sources:

- The Leeds Internet Corpus, from the University of Leeds Centre for Translation
  Studies (http://corpus.leeds.ac.uk/list.html)

- The OpenSubtitles Frequency Word Lists, by Invoke IT Limited
  (https://invokeit.wordpress.com/frequency-word-lists/)

- Wikipedia, the free encyclopedia (http://www.wikipedia.org)

Some additional data was collected by a custom application that watches the
streaming Twitter API, in accordance with Twitter's Developer Agreement &
Policy. This software only gives statistics about words that are very commonly
used on Twitter; it does not display or republish any Twitter content.

