import csv

line1 = ['Spam', 'Spam', 'Spam']
line2 = ['Spam', 'Spam', 'Spam']
line3 = ['Spam', 'Spam', 'Lovely Spam']
line4 = ['Spam', 'Spam', 'Eggs', 'Sugar']
lines = []
lines.append(line1)
lines.append(line2)
lines.append(line3)
lines.append(line4)

f = open('sw.csv', 'a+')
writer = csv.writer(f)

for line in lines:
    writer.writerow(line)
