#!/usr/bin/env bash

docker-compose up -d

sleep 5

BUCKET_NAME="nyc-duration"
REGION="us-east-1"
ENDPOINT_URL="http://localhost:4566"

# Check if the bucket exists
if aws --endpoint-url=$ENDPOINT_URL s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
  echo "Bucket does not exist. Creating bucket..."
  aws --endpoint-url=$ENDPOINT_URL s3 mb "s3://$BUCKET_NAME"
  echo "Bucket $BUCKET_NAME created."
else
  echo "Bucket $BUCKET_NAME already exists."
fi


ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi


pipenv run python integration_test.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi


docker-compose down
