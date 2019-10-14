# time-series-basics
Time Series basics - importing, cleaning, printing to csv
Note date files are synthetic data.

## ImportData class

### Description

    - Inputs:
        1. csv file containing header with 'Id', 'time', values' where rows contain integer Id, datetime time and integer value 
    
    - Attributes:
        1. _time is type datetime
        2. _value is type int
        3. _roundtime is type list that contains rounded time values of type datetime
        4. _roundvalues is type list (parallel to _roundtime) that contains non-duplicate values corresponding to _roundtime 
    
    - Functions:
        
        1. linear_search_value(self, key_time):
            + Description: returns a list of values associated with the specified time
            + Inputs:
                - key_time: a time object of type datetime
            + Outputs:
                - List of values that correspond to that datetime in the ImportData instance
        
        2. roundTimeArray(self, res):
            + Description: returns a iterable zip object of data (time, value) pairs
            + Inputs:
                - res: integer value that will determine the rounding interval of times to create _roundtime
            + Outputs:
                - iterable zip object of data containing roundtime and corresponding values (roundtime, roundvalue)
            
    
### Usage

This will store the times and associated values in an instance of ImportData called imported_data
```
imported_data = d_i.ImportData('test_file.csv')
```

### Necessary Modules

```
import csv
import dateutil.parser
```

## roundTimeArray Function

### Description:

    - Inputs:
    - Outputs:

## printArray Function

### Description:

    - Inputs:
    - Outputs: