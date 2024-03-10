# Uses Heath Nutrition and Population statistics,
# stored in the file HNP_Data.csv.gz,
# assumed to be located in the working directory.
# Prompts the user for an Indicator Name. If it exists and is associated with
# a numerical value for some countries or categories, for some the years 1960-2015,
# then finds out the maximum value, and outputs:
# - that value;
# - the years when that value was reached, from oldest to more recents years;
# - for each such year, the countries or categories for which that value was reached,
#   listed in lexicographic order.
# 
# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv
import gzip
from collections import defaultdict


filename = 'HNP_Data.csv.gz'
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()

indicator_of_interest = input('Enter an Indicator Name: ')

first_year = 1960
number_of_years = 56
max_value = None
countries_for_max_value_per_year = defaultdict(list)

with gzip.open(filename) as csvfile:
    file = csv.reader(line.decode('utf8').replace('\0', '') for line in csvfile)
    row = []
    for line  in file :
        if line:
            row.append(line)
    row[0][0]='Country Name'
    length = len(row)
    length_1 = len(row[0])
    max_value_in = None
    max_row_data = ''
    max_data = ''
#    '''
    for i in range(1,length):
        if indicator_of_interest in row[i]:
            for m in range(4,length_1):
                if row[i][m] :
                    if max_row_data == '':
                        max_row_data = 0.0
                    elif max_row_data < float(row[i][m]) :
                        max_row_data = float(row[i][m])
                        max_data = row[i][m]
    max_value_in = max_row_data
    if max_value_in == '':
        max_value = None
    elif max_value_in%1 != 0:
        max_value = float(max_value_in)
    elif max_value_in%1 == 0:
        max_value = int(max_value_in)
    
    if max_value_in != '':
        for i in range(1,length):
            if indicator_of_interest in row[i] and max_data in row[i] :
                for m in range(4,length_1):
                    if row[i][m]==max_data :
                        year = row[0][m]
                        countries_for_max_value_per_year[year].append(row[i][0])
                        countries_for_max_value_per_year[year] = sorted(list(set(countries_for_max_value_per_year[year])))
                    
            
if max_value is None:
    print('Sorry, either the indicator of interest does not exist or it has no data.')
else:
    print('The maximum value is:', max_value)
    print('It was reached in these years, for these countries or categories:')
    print('\n'.join(f'    {year}: {countries_for_max_value_per_year[year]}'
                                  for year in sorted(countries_for_max_value_per_year)
                   )
         )
