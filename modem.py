import asyncio
import websockets
import json
import subprocess
import logging
import requests
from gsmmodem.modem import GsmModem, SentSms
from gsmmodem.exceptions import GsmModemException

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
    response = requests.post("http://localhost:8000/api/sms/sms-update", json=data, headers=headers)
    response.raise_for_status()

async def websocket_client():
    async with websockets.connect("ws://localhost:6001/app/websocketkey?protocol=7&client=js&version=4.3.1&flash=false") as websocket:
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

def main():
    asyncio.run(websocket_client())

if __name__ == "__main__":
    main()