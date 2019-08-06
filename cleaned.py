import csv
import datetime
import re
from nltk import word_tokenize 
from nltk.util import ngrams
import operator
import pprint

INPUT_CSV_NAME = 'black_news'
INPUT_FILE_PATH = 'black_news.csv'
OUTPUT_FILE_BASE = 'cleaned/cleaned_'

BAD_BIGRAMS = [
    'black tea', 
    'africano para', 
    'african bean',
    'black hills',
]

def has_only_relevant_blacks(sent):
    pat = r'(\w*%s\w*)' % 'black'
    matches = re.findall(pat, sent.lower())
    for match in matches:
        if (match not in ['black', 'blacks', 'nonblack']):
            print(match)
            return False
    
    return True

def should_select_sentence(sent, connected_bigrams):
    ends_with_period = sent[-1] == '.'
    no_newlines = "\n" not in sent
    not_about_trypanosomiasis = 'trypanosomiasis' not in sent
    only_relevant_black = has_only_relevant_blacks(sent)
    contains_bad_bigram = any(term in connected_bigrams for term in BAD_BIGRAMS)
    if contains_bad_bigram:
        print("Contains Bad Bigram", contains_bad_bigram)
        print(sent, "\n")

    return ends_with_period and no_newlines and not_about_trypanosomiasis and only_relevant_black and not contains_bad_bigram

def main():
    sentences = []
    bigrams_dict = {}
    with open(INPUT_FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        invalid_count = 0
        for row in csv_reader:
            sent = row[1].strip()
            
            text = sent.lower()
            token = word_tokenize(text)
            bigrams = list(ngrams(token, 2)) 
            connected_bigrams = []
            for bigram in bigrams:
                connected_bigram = ' '.join(bigram)
                if (any(term in bigram[0] for term in ['african', 'black'])):
                    connected_bigrams.append(connected_bigram)
                    if (connected_bigram in bigrams_dict):
                        bigrams_dict[connected_bigram] += 1
                    else:
                        bigrams_dict[connected_bigram] = 1

            if (should_select_sentence(sent, connected_bigrams)):
                sentences.append(sent)
                line_count += 1
            else:
                invalid_count += 1
        print("Initial Sentence Lines: ", line_count)
        print("Invalid Count: ", invalid_count)
    
    sentences = list(set(sentences))
    print("Num Unique Sentence Lines: ", len(sentences))

    sorted_bigrams_dict = sorted(bigrams_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("\n\n Bigram Counts in Descending Order:")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sorted_bigrams_dict)

    write_time = datetime.datetime.now()
    output_file = OUTPUT_FILE_BASE + "_" + INPUT_CSV_NAME + "_" + str(write_time) + '.csv'
    with open(output_file, mode='a') as out_file:
        for cnt, sent in enumerate(sentences):
            out_file.write(sent + '\n')

main()