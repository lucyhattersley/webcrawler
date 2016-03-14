import csv
#with open('eggs.csv', 'wb') as csvfile:
#    spamwriter = csv.writer(csvfile)
#    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
with open('eggs.csv', 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    print dialect.delimiter()
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

