#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pandas.testing as pdt

from datetime import datetime
from batch import prepare_data

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    categorical = ['PULocationID', 'DOLocationID'] 

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]
    
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']

    input_df = pd.DataFrame(data, columns=columns)

    actual_features  = prepare_data(input_df, categorical)

    # print(actual_features)
    # print(actual_features.shape[0])

    # tests/test_batch.py in prepare_data()
    #   PULocationID DOLocationID tpep_pickup_datetime tpep_dropoff_datetime  duration
    # 0           -1           -1  2023-01-01 01:01:00   2023-01-01 01:10:00       9.0
    # 1            1            1  2023-01-01 01:02:00   2023-01-01 01:10:00       8.0

    expected_data = [
        ("-1", "-1", dt(1, 1), dt(1, 10), 9.0),
        ("1", "1", dt(1, 2), dt(1, 10), 8.0),
    ]
    expected_columns = [
        'PULocationID', 
        'DOLocationID', 
        'tpep_pickup_datetime', 
        'tpep_dropoff_datetime',
        'duration',
    ]
    expected_features = pd.DataFrame(expected_data, columns=expected_columns)

    # print(expected_features)
    # print(expected_features.shape[0])

    # compare DataFrames using dict, list, or pd.testing
    assert actual_features.to_dict() == expected_features.to_dict()
    # just actual_df == expected_df does not work
    assert expected_features.equals(actual_features)

    # https://pandas.pydata.org/docs/reference/api/pandas.testing.assert_frame_equal.html
    # check_dtype: bool, default True
    pdt.assert_frame_equal(actual_features, expected_features)

    # compare number of rows in DataFrames
    assert actual_features.shape[0] == expected_features.shape[0]
    # compare number of columns in DataFrames
    assert actual_features.shape[1] == expected_features.shape[1]

    # compare column names in DataFrames as lists
    assert actual_features.columns.to_list() == expected_features.columns.to_list()
