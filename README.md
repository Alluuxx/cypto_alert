This project is a Dockerized application designed to monitor cryptocurrency prices and notify users of significant price changes. The application consists of two main components that communicate via an MQTT broker.

1. **Price Fetcher**  
   - Fetches real-time cryptocurrency prices using the Coinmarketcap API.  
   - Monitors changes in cryptocurrency prices (XRP, BTC, QNT, XLM, HBAR).  
   - Publishes price data to an MQTT broker.

2. **Price Notifier**  
   - Subscribes to the MQTT broker to receive price data.  
   - Checks if price changes exceed a predefined percentage threshold in a predefined timeframe.  
   - Sends alerts via a Discord bot when significant price changes occur.

  The system runs in Rahti 2 cloud environment 24/7.
