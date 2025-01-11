import requests
import time
import paho.mqtt.client as mqtt
import json
import os

API_KEY = os.getenv("API_KEY")  
BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")  
WAIT_TIME = int(os.getenv("WAIT_TIME", 60))  # default 60 sec

# lsit of 5 used cryptos
CRYPTOCURRENCIES = ["XRP", "BTC", "QNT", "XLM", "HBAR"]

def fetch_price(symbol, currency="USD"):
    try:
        url = BASE_URL
        headers = {"X-CMC_PRO_API_KEY": API_KEY}
        params = {"symbol": symbol, "convert": currency}
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data['data'][symbol]['quote'][currency]['price']
        else:
            return None
    except Exception as e:
        return None

def publish_prices_to_mqtt(prices):
    client = mqtt.Client()
    client.tls_set("/certs/ca.crt")
    client.tls_insecure_set(True)
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
        json_prices = json.dumps(prices) # prices -> json
        client.publish(MQTT_TOPIC, json_prices)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    while True:
        prices = {}
        for crypto in CRYPTOCURRENCIES:
            price = fetch_price(crypto)
            if price is not None:
                prices[crypto] = price

        if prices:
            publish_prices_to_mqtt(prices)
        
        time.sleep(WAIT_TIME)  # get price every 60 sec