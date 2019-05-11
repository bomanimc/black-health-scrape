import csv
import datetime

INPUT_CSV_NAME = 'black_news'
INPUT_FILE_PATH = 'black_news.csv'
OUTPUT_FILE_BASE = 'cleaned/cleaned_'

def main():
    sentences = []
    with open(INPUT_FILE_PATH, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        invalid_count = 0
        for row in csv_reader:
            sent = row[1].strip()
            if (sent[-1] == '.' and "\n" not in sent and 'trypanosomiasis' not in sent):
                sentences.append(sent)
                line_count += 1
            else:
                invalid_count += 1
        print("Initial Sentence Lines: ", line_count)
        print("Invalid Count: ", invalid_count)
    
    sentences = list(set(sentences))
    print("Num Unique Sentence Lines: ", len(sentences))

    write_time = datetime.datetime.now()
    output_file = OUTPUT_FILE_BASE + "_" + INPUT_CSV_NAME + "_" + str(write_time) + '.csv'
    with open(output_file, mode='a') as out_file:
        for cnt, sent in enumerate(sentences):
            out_file.write(sent + '\n')

main()