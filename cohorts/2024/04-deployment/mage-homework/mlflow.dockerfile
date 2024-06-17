FROM python:3.10-slim

RUN pip install mlflow==2.13.2

EXPOSE 5000

CMD [ \
    "mlflow", "server", \
    "--backend-store-uri", "sqlite:///home/mlflow.db", \
    "--host", "0.0.0.0", \
    "--port", "5000" \
]