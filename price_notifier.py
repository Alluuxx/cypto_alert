import paho.mqtt.client as mqtt
import json
import discord
import asyncio
from datetime import datetime
import os

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
PRICE_TOPIC = os.getenv("PRICE_TOPIC") 
ALERT_TOPIC = os.getenv("ALERT_TOPIC")
THRESHOLD = float(os.getenv("THRESHOLD", 0.3)) 

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID")) 

# discord-library settings
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

previous_prices = {}

def on_connect(client, userdata, flags, rc):
    client.subscribe(PRICE_TOPIC)

def on_message(client, userdata, msg):
    global previous_prices
    try:
        prices = json.loads(msg.payload.decode("utf-8"))
        for crypto, current_price in prices.items():
            previous_price = previous_prices.get(crypto)
            
            if previous_price is not None:
                change = ((current_price - previous_price) / previous_price) * 100
                print(f"{crypto}: Price change: {change:.2f}%")

                if abs(change) >= THRESHOLD:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    alert_message = (f"ALERT! {crypto}: Price change: {change:.2f}% at {current_time}. "
                                    f"Current price: {current_price:.6f} EUR")
                    client.publish(ALERT_TOPIC, alert_message)
                    asyncio.run_coroutine_threadsafe(
                        send_alert_to_discord(alert_message), discord_client.loop
                    )
            previous_prices[crypto] = current_price
    except Exception as e:
        print(f"Error processing message: {e}")

async def send_alert_to_discord(alert_message):
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(alert_message)
    else:
        print("Failed to find the specified Discord channel.")

@discord_client.event
async def on_ready():
    print(f"Discord bot logged in as {discord_client.user}")

def main():
    client = mqtt.Client()
    client.tls_set("/certs/ca.crt")
    client.tls_insecure_set(True)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")

if __name__ == "__main__":
    main()
    discord_client.run(DISCORD_TOKEN)