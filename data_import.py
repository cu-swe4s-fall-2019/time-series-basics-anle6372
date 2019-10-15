import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
from pathlib import Path

# simple linear search tool
def linear_search(entries, key_entry):
    for i in range(len(entries)):
        curr = entries[i]
        if key_entry == curr:
            return i
    return -1


# open file, create a reader from csv.DictReader, and read input times and values
class ImportData:
    def __init__(self, data_csv):
        self._file_name = data_csv
        self._time = []
        self._value = []
        self._roundtime = []
        self._roundvalue = []

        with open(data_csv, "r") as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                id = reader.fieldnames[0]
                # ensures valid row
                try:
                    int(row[id])
                except ValueError:
                    continue
                    # ensures time not empty
                if not row['time']:
                    self._time.append(None)
                    # ensures value not empty
                    if not row['value']:
                        self._value.append(None)
                        continue
                    continue
                # stores time
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print('Bad input format for time')
                    print(row['time'])
                    raise ValueError
                # adjusts value if necessary
                if row['value'] == 'low':
                    self._value.append(int(40))
                    print('low value replaced with 40')
                    continue
                if row['value'] == 'high':
                    self._value.append(int(300))
                    print('high value replaced with 300')
                    continue
                # stores value
                try:
                    self._value.append(float(row['value']))
                except ValueError:
                    print('Bad input for value')
                    print(row['value'])
                    self._value.append(0)
                    continue

            # checks for empty arrays
            if self._time == []:
                self._time = None
                print('File missing time')
            if self._value == []:
                self._value = None
                print('File missing values')

            file_handle.close()


    def linear_search_value(self, key_time):
        # returns list of value(s) associated with key_time
        values = []
        if type(key_time) == str:
            key_time = dateutil.parser.parse(key_time)
        for i in range(len(self._time)):
            curr = self._time[i]
            if key_time == curr:
                values.append(self._value[i])
                continue
        if values == []:
            print('No value associated with this time')
            return -1
        return values

    def binary_search_value(self, key_time):
        pass
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

    def roundTimeArray(self, res):
        # Inputs: obj (ImportData Object) and res (rounding resolution)
        # Creates a list of datetime entries and associated values
        # with the times rounded to the nearest rounding resolution (res)
        # ensure no duplicated times
        # handle duplicated values for a single timestamp based on instructions
        # return: iterable zip object of the two lists
        if 'activity' in str(self._file_name):
            file_code = 'a'
        if 'bolus' in str(self._file_name):
            file_code = 'b'
        if 'meal' in str(self._file_name):
            file_code = 'm'
        if 'smbg' in str(self._file_name):
            file_code = 's'
        if 'hr' in str(self._file_name):
            file_code = 'h'
        if 'cgm' in str(self._file_name):
            file_code = 'c'
        if 'basal' in str(self._file_name):
            file_code = 'ba'
        if not 'file_code' in locals():
            file_code = 'e'
        for times in self._time:
            minminus = datetime.timedelta(minutes=(times.minute % res))
            minplus = datetime.timedelta(minutes=res) - minminus
            if (times.minute % res) <= res / 2:
                newtime = times - minminus
            else:
                newtime = times + minplus
            value_idx = linear_search(self._roundtime, newtime)
            # checks if rounded time is already present in _roundtime list
            if not value_idx == -1:
                # takes average if more than one value for specific time
                value = sum(self.linear_search_value(times))/len(self.linear_search_value(times))
                # action for repeated time: sum or avg depending on file origin
                if file_code is 'a':
                    self._roundvalue.append(self._roundvalue[value_idx] + value)
                if file_code is 'b':
                    self._roundvalue.append(self._roundvalue[value_idx] + value)
                if file_code is 'm':
                    self._roundvalue.append(self._roundvalue[value_idx] + value)
                if file_code is 's':
                    self._roundvalue.append((self._roundvalue[value_idx] + value)/2)
                if file_code is 'h':
                    self._roundvalue.append((self._roundvalue[value_idx] + value)/2)
                if file_code is 'c':
                    self._roundvalue.append((self._roundvalue[value_idx] + value)/2)
                if file_code is 'ba':
                    self._roundvalue.append((self._roundvalue[value_idx] + value)/2)
                if file_code is 'e':
                    self._roundvalue.append((self._roundvalue[value_idx] + value)/2)

            # appends rounded time to _roundtime list
            self._roundtime.append(newtime)
            # locates value associated with rounded time and appends to _roundvalue list
            newvalue = float(self.linear_search_value(times)[0])
            self._roundvalue.append(newvalue)
        return zip(self._roundtime, self._roundvalue)

def printArray(data_list, annotation_list, base_name, key_file):
    # find index with data you want
    base_data = []
    key_idx = 0
    for i in range(len(annotation_list)):
        if annotation_list[i] == key_file:
            base_data = data_list[i]
            print(base_data)
            print('base data is: ' + annotation_list[i])
            key_idx = i
            break
        if i == len(annotation_list):
            print('Key not found')

    # write time and key_file headers
    file = open(base_name + '.csv', 'w')
    file.write('time, ')
    file.write(annotation_list[key_idx][0:-4] + ', ')
    # remove key_file from header list
    non_key = list(range(len(annotation_list)))
    non_key.remove(key_idx)
    # write remaining headers
    for idx in non_key:
        file.write(annotation_list[idx][0:-4] + ', ')
    file.write('\n')

    for time, value in base_data:
        file.write(time.strftime("%m/%d/%Y %H:%M") + ', ' + value + ', ')
        for n in non_key:
            if time in data_list[n]._roundtimeStr:
                file.write(str(data_list[n].linear_search_value(time)) + ', ')
            else:
                file.write('0, ')
        file.write('\n')
    file.close()


if __name__ == '__main__':

    #adding arguments
    parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    prog= 'dataImport')

    parser.add_argument('--folder_name', type = str, help = 'Name of the folder containing input files')

    parser.add_argument('--output_file', type=str, help = 'Name of output file')

    args = parser.parse_args()

    folder_path = Path(args.folder_name)

    # pull all the files from folder_name into list
    files_lst = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    # import all the files into a list of ImportData objects
    data_lst = []
    for files in files_lst:
        data_lst.append(ImportData(folder_path / files))

    # create two new lists of zip objects with 5min data and 15min data
    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min
    for data in data_lst:
        data_5.append(data.roundTimeArray(5))
        data_15.append(data.roundTimeArray(15))

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', 'cgm_small.csv')
    printArray(data_15, files_lst, args.output_file+'_15', 'cgm_small.csv')
