#!/bin/bash

PROJECT_NAME=hmwk4 \
  MAGE_CODE_PATH=/home/src \
  SMTP_EMAIL=$SMTP_EMAIL \
  SMTP_PASSWORD=$SMTP_PASSWORD \
  docker compose up -d
