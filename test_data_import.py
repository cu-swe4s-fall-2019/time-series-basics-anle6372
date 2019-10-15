"""Unittesting framework for data_import.py
Parameters
----------
None
Returns
-------
None
"""

import unittest
import data_import as d_i
import os
import csv
import random as rdm
import datetime


# function for generating random dates
def random_date():
    try:
        temporal_location = datetime.datetime(
            rdm.randint(1930, 2019), rdm.randint(1, 12), rdm.randint(1, 31),
            rdm.randint(0, 23), rdm.randint(0, 60))
    except ValueError:
        temporal_location = datetime.datetime(1999, 10, 20, 22, 38)
    return temporal_location


# Testing data_import empty file
class TestEmpty(unittest.TestCase):

    def setUp(self):
        with open('test_empty_file.csv', "w") as file_handle:
            file_handle.close()
        imported_data = d_i.ImportData('test_empty_file.csv')
        return imported_data

    def tearDown(self):
        os.remove('test_empty_file.csv')

    def test_empty_file_time(self):
        imported_data = self.setUp()
        self.assertEqual(imported_data._time, None, msg='File missing time')

    def test_empty_file_value(self):
        imported_data = self.setUp()
        self.assertEqual(imported_data._value, None, msg='File missing value')


# testing bad headers
class TestBadHeaders(unittest.TestCase):

    def test_header_only_file(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['header', 'with', 'no useful', 'info'])
            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data._time,
                             None, msg='File missing time')
            self.assertEqual(imported_data._value,
                             None, msg='File missing time')
        os.remove('test_file.csv')

    def test_bad_header_file(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['time', 'values',
                                  'no useful', 'info'])
            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data._time,
                             None, msg='File missing time')
            self.assertEqual(imported_data._value,
                             None, msg='File missing time')
        os.remove('test_file.csv')


# testing variable values
class TestVariableValues(unittest.TestCase):

    def test_random_file(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value', 'no useful', 'info'])
            Id = 1
            check_vals = [[], [], []]
            for i in range(100):
                time = random_date()
                Id += i
                value = rdm.randint(100, 1000)
                check_vals[0].append(Id)
                check_vals[1].append(time)
                check_vals[2].append(value)
                file_writer.writerow([Id, time, value])
            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data._time, check_vals[1])
            self.assertEqual(imported_data._value, check_vals[2])
        os.remove('test_file.csv')


# testing bad values
class TestBadValues(unittest.TestCase):

    def test_time_string(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value'])
            time = 'not a time'
            value = int(420)
            Id = int(4)
            file_writer.writerow([Id, time, value])
            file_handle.close()
            self.assertRaises(ValueError,
                              lambda: d_i.ImportData('test_file.csv'))
        os.remove('test_file.csv')

    def test_time_bool(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value'])
            time = True
            Id = int(4)
            file_writer.writerow([Id, time])
            file_handle.close()
            self.assertRaises(ValueError,
                              lambda: d_i.ImportData('test_file.csv'))
        os.remove('test_file.csv')

    def test_time_float(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value'])
            time = float(420.69)
            value = int(420)
            Id = int(4)
            file_writer.writerow([Id, time, value])
            file_handle.close()
            self.assertRaises(ValueError,
                              lambda: d_i.ImportData('test_file.csv'))
        os.remove('test_file.csv')

    def test_entry_empty(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value'])
            Id = 1
            check_vals = [[], [], []]
            for i in range(5):
                time = random_date()
                Id += i
                value = rdm.randint(100, 1000)
                check_vals[0].append(Id)
                check_vals[1].append(time)
                check_vals[2].append(value)
                file_writer.writerow([Id, time, value])
            time = None
            value = None
            Id = None
            file_writer.writerow([Id, time, value])
            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data._time, check_vals[1])
            self.assertEqual(imported_data._value, check_vals[2])
        os.remove('test_file.csv')

    def test_junk(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value'])
            Id = 1
            check_vals = [[], [], []]
            for i in range(5):
                time = random_date()
                Id += i
                value = rdm.randint(100, 1000)
                check_vals[0].append(Id)
                check_vals[1].append(time)
                check_vals[2].append(value)
                file_writer.writerow([Id, time, value])
            file_writer.writerow('asdfjkl:')
            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data._time, check_vals[1])
            self.assertEqual(imported_data._value, check_vals[2])
        os.remove('test_file.csv')


# testing values outside range
class TestValuesOutsideRange(unittest.TestCase):

    def test_outside_range(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value', 'no useful', 'info'])
            Id = 1
            check_vals = [[], [], []]
            for i in range(10):
                time = random_date()
                Id += i
                value = rdm.randint(100, 1000)
                check_vals[0].append(Id)
                check_vals[1].append(time)
                check_vals[2].append(value)
                file_writer.writerow([Id, time, value])
                time = random_date()
                value = str('low')
            Id = 11
            file_writer.writerow([Id, time, value])
            check_vals[0].append(Id)
            check_vals[1].append(time)
            check_vals[2].append(int(40))
            time = random_date()
            value = str('high')
            Id = 12
            file_writer.writerow([Id, time, value])
            check_vals[0].append(Id)
            check_vals[1].append(time)
            check_vals[2].append(int(300))

            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data._time, check_vals[1])
            self.assertEqual(imported_data._value, check_vals[2])
        os.remove('test_file.csv')


# test linear search
class TestLinearSearch(unittest.TestCase):

    def test_linear_search_single(self):
        for i in range(20):
            with open('test_file.csv', "w") as file_handle:
                file_writer = csv.writer(file_handle,
                                         delimiter=',', quotechar='"',
                                         quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow(['Id', 'time', 'value',
                                      'no useful', 'info'])
                Id = 0
                for i in range(rdm.randint(1, 20)):
                    time = str(random_date())
                    Id += i
                    value = rdm.randint(100, 1000)
                    file_writer.writerow([Id, time, value])
                time = str(datetime.datetime(1800, 10, 20, 22, 38))
                Id += 1
                value = rdm.randint(1, 1000)
                marked_time = time
                marked_value = value
                file_writer.writerow([Id, time, value])
                for i in range(rdm.randint(1, 20)):
                    time = str(random_date())
                    Id += i
                    value = rdm.randint(100, 1000)
                    file_writer.writerow([Id, time, value])
                file_handle.close()
                imported_data = d_i.ImportData('test_file.csv')
                self.assertEqual(
                    imported_data.linear_search_value(marked_time),
                    [marked_value])
            os.remove('test_file.csv')

    def test_linear_search_double(self):
        with open('test_file.csv', "w") as file_handle:
            file_writer = csv.writer(file_handle,
                                     delimiter=',', quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(['Id', 'time', 'value', 'no useful', 'info'])
            Id = 0
            for i in range(rdm.randint(1, 20)):
                time = str(random_date())
                Id += i
                value = rdm.randint(100, 1000)
                file_writer.writerow([Id, time, value])
            time = str(datetime.datetime(1800, 10, 20, 22, 38))
            Id += 1
            value = rdm.randint(100, 1000)
            marked_time = time
            marked_value_1 = value
            file_writer.writerow([Id, time, value])
            for i in range(rdm.randint(1, 20)):
                time = random_date()
                Id += i
                value = rdm.randint(100, 1000)
                file_writer.writerow([Id, time, value])
            time = str(datetime.datetime(1800, 10, 20, 22, 38))
            Id += 1
            value = rdm.randint(100, 1000)
            marked_value_2 = value
            file_writer.writerow([Id, time, value])
            file_handle.close()
            imported_data = d_i.ImportData('test_file.csv')
            self.assertEqual(imported_data.linear_search_value(marked_time),
                             [marked_value_1, marked_value_2])
        os.remove('test_file.csv')


if __name__ == '__main__':
    unittest.main()
