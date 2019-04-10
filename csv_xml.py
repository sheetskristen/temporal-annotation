import csv
from bs4 import BeautifulSoup


FILE = 'Full-Economic-News-DFE-839861.csv'
OUTPUT_1 = 'ECON-NEWS-1.xml'
OUTPUT_2 = 'ECON-NEWS-2.xml'
OUTPUT_3 = 'ECON-NEWS-3.xml'
HOLD_OUT = 'ECON-NEWS-HOLDOUT.xml'


def convert_row(row):
    soup = BeautifulSoup(row[14])
    return """<UNIT_ID="%s">
    <ARTICLE_DATE>%s</ARTICLE_DATE>
    <TEXT>%s</TEXT>
</UNIT_ID>""" % (row[0], row[10], soup.get_text())

def write_file(data_list, file_name):
    file = open(file_name, 'w')
    data = '\n'.join([convert_row(row) for row in data_list[0:]])

    file.write(data)


with open(FILE, encoding='utf-8', errors='ignore') as f:
    csv_f = csv.reader(f)
    data = []

    for row in csv_f:
        data.append(row[0:])
    f.close()

    hold_out = [data[i] for i in range(1, len(data)) if (i%13 == 0|i%13 ==2|i%13==3|i%13==4|i%13==5|i%13==6|i%13==7|i%13==8|i%13==9|i%13==10|i%13==11|i%13==12)]
    annotate = [data[i] for i in range(1, len(data)) if i%13 == 1]

    set_1 = [data[i] for i in range(0, len(annotate)) if i%3 == 0]
    set_2 = [data[i] for i in range(0, len(annotate)) if i % 3 == 1]
    set_3 = [data[i] for i in range(0, len(annotate)) if i % 3 == 2]

    write_file(set_1, OUTPUT_1)
    write_file(set_2, OUTPUT_2)
    write_file(set_3, OUTPUT_3)

    #print('\n'.join([convert_row(row) for row in data[1:]]))
