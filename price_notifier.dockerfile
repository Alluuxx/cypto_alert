FROM python:3.9-slim

COPY price_notifier.py .
COPY requirements.txt .
COPY ./certs/ca.crt /certs/ca.crt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "price_notifier.py"]