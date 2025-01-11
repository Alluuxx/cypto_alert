FROM python:3.9-slim

COPY price_fetcher.py .
COPY requirements.txt .
COPY ./certs/ca.crt /certs/ca.crt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "price_fetcher.py"]

