#!/usr/bin/env python
# coding: utf-8

import sys
import pickle
import pandas as pd

categorical = ['PULocationID', 'DOLocationID']

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


def read_data(filename):
    df = pd.read_parquet(filename)
    print('read_parquet() done')
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def run():
    service_type = sys.argv[1] # 'green' / 'yellow' 
    year = int(sys.argv[2]) #2023
    month = int(sys.argv[3]) #3
    
    # print('in run(): ARGS set')

    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{service_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'{service_type}_{year:04d}-{month:02d}.parquet'

    df = read_data(input_file)
    # print('df read')
    # print(df.head(2))

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    print('y_pred done')

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predictions'] = y_pred.tolist()
    # print(f'df_result done')
    preds_std = df_result['predictions'].std()
    preds_mean = df_result['predictions'].mean()
    print(f"std: {preds_std}")
    print(f"mean: {preds_mean}")

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

    print(f'output file saved')


if __name__ == "__main__":
    print('in main()')
    run()
