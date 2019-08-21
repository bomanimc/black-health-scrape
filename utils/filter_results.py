import csv
import datetime
import re
from nltk import word_tokenize 
from nltk.util import ngrams
import operator
import pprint
import getopt
import sys
import os

write_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

INPUT_FILE_PATH = None
OUTPUT_FILE_PATH = 'data/test/cleaned/cleaned_results_' + write_time + '.csv'
BAD_BIGRAMS = [
    'black tea', 
    'africano para', 
    'african bean',
    'black hills',
    'african plum',
    'african mango',
    'black beans',
    'black henna',
    'black-ish ,',
    'black box',
    'black pepper',
    'african forests'
]

def has_only_relevant_blacks(sent):
    pat = r'(\w*%s\w*)' % 'black'
    matches = re.findall(pat, sent.lower())
    for match in matches:
        if (match not in ['black', 'blacks', 'nonblack']):
            print(match)
            return False
    
    return True

def get_bigrams_in_sentence(sent):
    text = sent.lower()
    token = word_tokenize(text)
    bigrams = list(ngrams(token, 2)) 
    connected_bigrams = []

    for bigram in bigrams:
        connected_bigram = ' '.join(bigram)
        if (any(term in bigram[0] for term in ['african', 'black'])):
            connected_bigrams.append(connected_bigram)
    
    return connected_bigrams

def should_select_sentence(sent):
    connected_bigrams = get_bigrams_in_sentence(sent)

    ends_with_period = sent[-1] == '.'
    no_newlines = "\n" not in sent
    not_about_trypanosomiasis = 'trypanosomiasis' not in sent
    only_relevant_black = has_only_relevant_blacks(sent)
    contains_bad_bigram = any(term in connected_bigrams for term in BAD_BIGRAMS)
    if contains_bad_bigram:
        print("Contains Bad Bigram", contains_bad_bigram)
        print(sent, "\n")

    return ends_with_period and no_newlines and not_about_trypanosomiasis and only_relevant_black and not contains_bad_bigram

def processArgs():
    global INPUT_FILE_PATH
    global OUTPUT_FILE_PATH

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    gnuOptions = [
        'input-file=',
        'output-file=',
    ]

    try:
        arguments, values = getopt.getopt(argument_list, "", gnuOptions)
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("--output-file"):
            OUTPUT_FILE_PATH = currentValue
        elif currentArgument in ("--input-file"):
            INPUT_FILE_PATH = currentValue
            print("Using search results links from input file:", INPUT_FILE_PATH)

def validateArgs():
    if (OUTPUT_FILE_PATH == None or INPUT_FILE_PATH == None):
        if (OUTPUT_FILE_PATH == None):
            print ("Must set output file path.")
        elif (INPUT_FILE_PATH == None):
            print ("Must set input file path.")

        sys.exit(2)

def main():
    processArgs()
    validateArgs()

    sentences = []
    bigrams_dict = {}
    with open(INPUT_FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        invalid_count = 0
        for row in csv_reader:
            sent = row[1].strip()
            
            connected_bigrams = get_bigrams_in_sentence(sent)
            for connected_bigram in connected_bigrams:
                if (connected_bigram in bigrams_dict):
                    bigrams_dict[connected_bigram] += 1
                else:
                    bigrams_dict[connected_bigram] = 1

            if (should_select_sentence(sent)):
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

    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH), exist_ok=True) 
    with open(OUTPUT_FILE_PATH, mode='a') as out_file:
        for cnt, sent in enumerate(sentences):
            out_file.write(sent + '\n')

if __name__ == "__main__":
    main()