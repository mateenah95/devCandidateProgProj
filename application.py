import csv



with open('sample-data.csv', 'r') as csv_file:
    csv_data = csv.reader(csv_file)

    for csv_line in csv_data:
        print(csv_line)