#http://www.pythonforbeginners.com/systems-programming/using-the-csv-module-in-python/

#To be able to read csv formatted files, we will first have to import the
#csv module.
# import csv
# with open('eggs.csv','rb') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print row

#Example2
#import csv
#import sys

#f=open(sys.argv[1],'rU') #opens the csv file
#try:
#    reader = csv.reader(f) # creates the reader object
#    for row in reader: # iterates the rows of the file in orders      
#        print row
#finally:
#    f.close()    #closing

import csv
ifile = open('eggs.csv', "rb")
reader = csv.reader(ifile)

rownum = 0
for row in reader:
    # Save header row.
    if rownum == 0:
        header = row
    else:
        colnum = 0
        for col in row:
            print '%-8s: %s' % (header[colnum], col)
            colnum += 1
    rownum += 1

ifile.close()
