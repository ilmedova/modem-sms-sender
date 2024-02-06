import asyncio
import websockets
import json
import subprocess
import logging
import requests
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import GsmModemException

#replace with your websocket server url and port
WEBSOCKET_URL = "ws://WEBSOCKET_URL:WEBSOCKET_PORT/app/websocketkey?protocol=7&client=js&version=4.3.1&flash=false"

#you need to subscribe to one of the websocket channels that you already have on your backend, replace the channel name with the channel name you have
CHANNEL_NAME = "your_channel_name_for_subscribing"

#everytime the event is triggered, your websocket should send the event data in this format: {"phone": "1234567890","message": "Hello, this is a test message!"}
def establish_modem_connection():
    try:
        modem = GsmModem("/dev/ttyUSB0", 115200)
        modem.connect()
        modem.waitForNetworkCoverage(10)
        print("Connection with modem established")
        return modem
    except GsmModemException as e:
        print("Couldn't connect")
        return None

async def websocket_client():
    while True:
        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                await websocket.send(json.dumps({
                    "event": "pusher:subscribe",
                    "data": {
                        "channel": CHANNEL_NAME
                    }
                }))
                modem = establish_modem_connection()
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if "data" in data:
                        data = json.loads(data['data'])
                    print(data)
                    if data.get("phone") is not None:
                        try:
                            response = modem.sendSms(data.get("phone"), data.get("message"))
                        except GsmModemException as e:
                            modem.close()
        except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError):
            print("WebSocket connection closed or refused. Retrying...")
            await asyncio.sleep(5)  # Wait for 5 seconds before attempting to reconnect

def main():
    while True:
        try:
            asyncio.run(websocket_client())
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
