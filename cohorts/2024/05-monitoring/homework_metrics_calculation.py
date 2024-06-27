import datetime
import time
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

from pprint import pprint
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metrics import ColumnDriftMetric, ColumnSummaryMetric, ColumnQuantileMetric, ColumnCorrelationsMetric, DatasetDriftMetric, DatasetMissingValuesMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists hmwk5_metrics;
create table hmwk5_metrics(
	timestamp timestamp,
	prediction_drift float,
	mean_total_fare float,
	fare_amount_quantile float,
	num_drifted_columns integer,
	share_missing_values float
)
"""

reference_data = pd.read_parquet('data/reference.parquet')
with open('models/lin_reg.bin', 'rb') as f_in:
	model = joblib.load(f_in)

begin = datetime.datetime(2024, 3, 1, 0, 0)
# data labeling
target = "duration_min"
date_features = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]
num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
cat_features = ["PULocationID", "DOLocationID"]
column_mapping = ColumnMapping(
    prediction='prediction',
	datetime_features=date_features,
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)
raw_data = pd.read_parquet('data/green_tripdata_2024-03.parquet')
# take only these columns
raw_data = raw_data[date_features + num_features + cat_features]
# exclude outliers for dates not in Mar 2024
raw_data = raw_data.loc[(raw_data.lpep_pickup_datetime >= datetime.datetime(2024,3,1,0,0)) & 
                               (raw_data.lpep_pickup_datetime < datetime.datetime(2024,4,1,0,0))]

report = Report(metrics=[
	ColumnDriftMetric(column_name='prediction'),
	ColumnSummaryMetric(column_name='fare_amount'),
	ColumnQuantileMetric(column_name="fare_amount", quantile=0.5),
	DatasetDriftMetric(),
    DatasetMissingValuesMetric()
])

# @task - translates to mage's data block
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)

# @task - translates to mage's data block
def calculate_metrics_postgresql(curr, i):
	current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
		(raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

	#current_data.fillna(0, inplace=True)
	current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))

	report.run(reference_data = reference_data, current_data = current_data,
		column_mapping=column_mapping)

	result = report.as_dict()
	# pprint(f"ColumnDriftMetric ['metrics'][0]['result']['drift_score']: {result['metrics'][0]['result']['drift_score']}", indent=2)
	# pprint(f"ColumnSummaryMetric ['metrics'][1]['result']['current_characteristics']['mean']: {result['metrics'][1]['result']['current_characteristics']['mean']}", indent=2)
	# pprint(f"ColumnQuantileMetric ['metrics'][2]['result']['current']['value']: {result['metrics'][2]['result']['current']['value']}", indent=2)
	# pprint(f"DatasetDriftMetric['metrics'][3]['result']['number_of_drifted_columns']: {result['metrics'][3]['result']['number_of_drifted_columns']}", indent=2)
	# pprint(f"DatasetMissingValuesMetric ['metrics'][4]['result']['current']['share_of_missing_values']: {result['metrics'][4]['result']['current']['share_of_missing_values']}", indent=2)


	prediction_drift = result['metrics'][0]['result']['drift_score']
	mean_total_fare = result['metrics'][1]['result']['current_characteristics']['mean']
	fare_amount_quantile = result['metrics'][2]['result']['current']['value']
	num_drifted_columns = result['metrics'][3]['result']['number_of_drifted_columns']
	share_missing_values = result['metrics'][4]['result']['current']['share_of_missing_values']

	curr.execute(
		"insert into hmwk5_metrics(timestamp, prediction_drift, mean_total_fare, fare_amount_quantile, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s, %s, %s)",
		(begin + datetime.timedelta(i), prediction_drift, mean_total_fare, fare_amount_quantile, num_drifted_columns, share_missing_values)
	)

# @flow - translates to mage's pipeline
def batch_monitoring_backfill():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, 31):
			with conn.cursor() as curr:
				calculate_metrics_postgresql(curr, i)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info(f"data sent, {i}")

if __name__ == '__main__':
	batch_monitoring_backfill()
