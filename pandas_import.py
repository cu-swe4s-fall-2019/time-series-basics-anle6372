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

folder_path = Path('smallData')
# pull all the files from folder_name into list
files_lst = [f for f in
             listdir(folder_path) if isfile(join(folder_path, f))]
# import all the files into a list of ImportData objects
data_lst = []
for files in files_lst:
    data_lst.append(pd.read_csv(str(folder_path / files), parse_dates=['time'], index_col=['time']))
