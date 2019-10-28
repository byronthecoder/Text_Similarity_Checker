"""\
------------------------------------------------------------
USE: python <PROGNAME> (options) file1...fileN
OPTIONS:
    -h : print this help message
    -b : use BINARY weights (default: count weighting)
    -s FILE : use stoplist file FILE
    -I PATT : identify input files using pattern PATT, 
              (otherwise uses files listed on command line)
------------------------------------------------------------
"""

import sys, re, getopt, glob, itertools
from collections import Counter

opts, args = getopt.getopt(sys.argv[1:], 'hs:bI:')
opts = dict(opts)
filenames = args

##############################
# HELP option

if '-h' in opts:
    help = __doc__.replace('<PROGNAME>', sys.argv[0], 1)
    # print(help, file=sys.stderr)
    sys.exit()

##############################
# Identify input files, when "-I" option used

if '-I' in opts:
    filenames = sorted(glob.glob(opts['-I']))

print('INPUT-FILES:', ' '.join(filenames))

##############################
# STOPLIST option

stops = set()
if '-s' in opts:
    with open(opts['-s'],'r') as stop_fs:
        for line in stop_fs:
            stops.add(line.strip())

##############################
# COMPARE doc pairs


# Read files and tokenize
def count_words(doc):
    with open(doc, 'r') as doc:
        words = []
        for line in doc:
            line = line.lower()
            line = line.strip()
            sent = re.findall(r'[A-Za-z]+', line)
            sent = [word for word in sent if word not in stops]
            for word in sent:
                words.append(word)
        vocab = Counter(words)

    return vocab


# Simple jaccard coefficient
def compare_docs(filenames):
    doc1 = filenames[0]
    doc2 = filenames[1]
    vocab1 = count_words(doc1)
    word_type1 = set(vocab1)

    vocab2 = count_words(doc2)
    word_type2 = set(vocab2)

    words_inter = word_type1.intersection(word_type2)
    words_union = word_type1.union(word_type2)
    count_min = sum([min(vocab1[word], vocab2[word]) for word in words_inter])
    count_max = sum([max(vocab1[word], vocab2[word]) for word in words_union])

    # sim = len(word_type1.intersection(word_type2)) / len(word_type1.union(word_type2))
    sim = count_min / count_max
    print(str(doc1) + '<>' + str(doc2) + '=', sim)


filenames = [i for i in itertools.combinations(filenames, 2)]

for i in filenames:
    compare_docs(i)