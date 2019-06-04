#importing the CSV module & easypost module
import csv, easypost

easypost.api_key = 'EZTKb4661e503603421d8dd125dc8e383aa4hY4mwPbdKTnhsCy2CwfUYA'

with open('sample-data.csv', 'r') as csv_file:
    csv_data = csv.reader(csv_file)

    for csv_line in csv_data:
        print(csv_line)