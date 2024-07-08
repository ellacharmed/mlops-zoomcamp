#!/usr/bin/env python
# coding: utf-8

import os
import sys
import pickle
import pandas as pd

from datetime import datetime

with open('model.bin', 'rb') as f_in:
    dv, lr = pickle.load(f_in)


def dt(hour, minute, second=0):
    
    return datetime(2023, 1, 1, hour, minute, second)
    

def read_data(filename, categorical):

    # print('in read_data()')

    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")

    if S3_ENDPOINT_URL is None:
        options = None
    else:
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

    df = pd.read_parquet(filename, storage_options=options)
    
    return prepare_data(df, categorical)

def prepare_data(df, cat_cols):
    # print('in prepare_data()')

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[cat_cols] = df[cat_cols].fillna(-1).astype('int').astype('str')

    return df


def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration/taxi_type=yellow/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)

def save_data(filename, df):
    # print('in save_data()')

    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")
    options = None

    if S3_ENDPOINT_URL is not None:
        # print(f'S3_ENDPOINT_URL : {S3_ENDPOINT_URL}')
        options = {"client_kwargs": {"endpoint_url": S3_ENDPOINT_URL}}

    df.to_parquet(filename, engine="pyarrow", index=False, storage_options=options)


def main(year, month):
    # print('in main()')

    # localstack s3 tests
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    # local tests
    # input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # output_file = f'./output/yellow_tripdata_{year:04d}-{month:02d}.parquet'

    categorical = ['PULocationID', 'DOLocationID'] 

    df = read_data(input_file, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    # print('in main() -- predicted mean duration:', y_pred.mean())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    save_data(output_file, df_result)
    # print('in main() -- ALL DONE')


if __name__ == "__main__":
    # print('in __main__')

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    main(year, month)
