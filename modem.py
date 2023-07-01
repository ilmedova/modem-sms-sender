import asyncio
import websockets
import json
import subprocess
import logging
import requests
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import GsmModemException

WEBSOCKET_URL = "ws://216.250.8.91:6001/app/websocketkey?protocol=7&client=js&version=4.3.1&flash=false"
API_ENDPOINT = "http://216.250.8.91:8000/api/sms/sms-update"

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

async def send_to_api_endpoint(phone, message, status):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "phone": phone,
        "message": message,
        "status": status
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    response.raise_for_status()

async def websocket_client():
    while True:
        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                await websocket.send(json.dumps({
                    "event": "pusher:subscribe",
                    "data": {
                        "channel": "verifications"
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
                            if isinstance(response, SentSms):
                                await send_to_api_endpoint(data.get("phone"), data.get("message"), True)
                            else:
                                await send_to_api_endpoint(data.get("phone"), data.get("message"), False)
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
