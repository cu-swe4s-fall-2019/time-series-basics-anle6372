"""Unittesting framework for data_import.py
Parameters
----------
None
Returns
-------
None
"""

import numpy as np
import pandas as pd
import datetime as dt
from os import listdir
from os.path import isfile, join
from pathlib import Path


def main():

    folder_path = Path('smallData')

    # pull all the files from folder_name into list
    files_lst = [f for f in
                 listdir(folder_path) if isfile(join(folder_path, f))]

    # import all the files into a list of ImportData objects
    data_lst = []
    for files in files_lst:
        data_lst.append(pd.read_csv(str(
            folder_path / files), parse_dates=['time'], index_col=['time']))

    # Eliminate rows with strings in value column
    # Force all value entries to float
    # Rename value to correspond to file name
    for i in range(len(data_lst)):
        data_lst[i] = data_lst[i][pd.to_numeric(
            data_lst[i]['value'], errors='coerce').notnull()]
        data_lst[i]['value'] = data_lst[i]['value'].astype(float)
        data_lst[i].rename(columns={'value': str(
            files_lst[i].replace('_small.csv', ''))}, inplace=True)

    # Get cgm parallel array location
    for i in range(len(files_lst)):
        if 'cgm' in files_lst[i]:
            cgmloc = i

    # Join files on time index with cgm as base
    baseDF = data_lst[cgmloc]
    framelist = data_lst
    framelist.pop(cgmloc)
    baseDF = baseDF.join(framelist)

    # Replace all NaN values with 0
    baseDF = baseDF.fillna(0)

    # Add time5 and time15 columns with rounded index times
    baseDF.insert(baseDF.shape[1], 'time5', baseDF.index.round('5min'))
    baseDF.insert(baseDF.shape[1], 'time15', baseDF.index.round('15min'))

    # Initalize the 5min and 15min dataframes with just the important columns
    sum_baseDF = baseDF[['activity', 'bolus', 'meal', 'time5', 'time15']]
    mean_baseDF = baseDF[['smbg', 'hr', 'basal', 'cgm', 'time5', 'time15']]

    # Create groups and average/sum overlaps
    five_min_mean = mean_baseDF.groupby(['time5']).mean()
    five_min_sum = sum_baseDF.groupby(['time5']).sum()
    fifteen_min_mean = mean_baseDF.groupby(['time15']).mean()
    fifteen_min_sum = sum_baseDF.groupby(['time15']).sum()

    # Join the two resulting frames
    five_min = five_min_mean.join(five_min_sum)
    fifteen_min = fifteen_min_mean.join(fifteen_min_sum)

    # Print frames to csv files
    five_min.to_csv('five_min.csv', index=True, header=True)
    fifteen_min.to_csv('fifteen_min.csv', index=True, header=True)

if __name__ == '__main__':
    main()