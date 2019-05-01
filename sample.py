import csv
import random
import datetime

FILE_PATH = 'black.csv'
OUTPUT_FILE_BASE = 'samples/sample_'

def random_sample_trial(sentences, write_time, sample_count):
    random_selection = random.sample(sentences, 10)
    output_file = OUTPUT_FILE_BASE + str(write_time) + '.txt'
    with open(output_file, mode='a') as out_file:
        out_file.write("SAMPLE " +  str(sample_count) + ":\n\n")
        for cnt, sent in enumerate(random_selection):
            out_file.write(sent + '\n')
        out_file.write("\n=======================\n\n ")
        sample_count += 1

def main():
    sentences = []
    with open(FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            sent = row[1].strip()
            if (sent[-1] == '.' and "\n" not in sent):
                sentences.append(sent)
                line_count += 1
        print("Initial Sentence Lines: ", line_count)
    
    sentences = list(set(sentences))
    print("Num Unique Sentence Lines: ", len(sentences))

    write_time = datetime.datetime.now()
    for i in range(0, 10):
        random_sample_trial(sentences, write_time, i)

main()