import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


# open file, create a reader from csv.DictReader, and read input times and values
class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []

        with open(data_csv, "r") as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                try:
                    int(row['Id'])
                except ValueError:
                    continue
                if not row['time']:
                    self._time.append(None)
                    if not row['value']:
                        self._value.append(None)
                        continue
                    continue
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print('Bad input format for time')
                    print(row['time'])
                    raise ValueError
                if row['value'] == 'low':
                    self._value.append(int(40))
                    print('low value replaced with 40')
                    continue
                if row['value'] == 'high':
                    self._value.append(int(300))
                    print('high value replaced with 300')
                    continue
                try:
                    self._value.append(int(row['value']))
                except ValueError:
                    print('Bad input for value')
                    print(row['value'])
                    raise ValueError

            if self._time == []:
                self._time = None
                print('File missing time')
            if self._value == []:
                self._value = None
                print('File missing values')

            file_handle.close()


    def linear_search_value(self, key_time):
        pass
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

    def binary_search_value(self,key_time):
        pass
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

def roundTimeArray(obj, res):
    pass
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned


def printArray(data_list, annotation_list, base_name, key_file):
    pass
    # combine and print on the key_file

if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    parser.add_argument('output_file', type=str, help = 'Name of Output file')

    parser.add_argument('sort_key', type = str, help = 'File to sort on')

    parser.add_argument('--number_of_files', type = int,
    help = "Number of Files", required = False)

    args = parser.parse_args()


    #pull all the folders in the file
    #files_lst = # list the folders


    #import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    #create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = [] # a list with time rounded to 5min
    data_15 = [] # a list with time rounded to 15min

    #print to a csv file
    printLargeArray(data_5,files_lst,args.output_file+'_5',args.sort_key)
    printLargeArray(data_15, files_lst,args.output_file+'_15',args.sort_key)
