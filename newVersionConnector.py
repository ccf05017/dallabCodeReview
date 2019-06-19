from websockets import connect
import asyncio
import json
import time
import pprint


class EthClient:

    def __init__(self, host):
        self._websocket = None
        self._connected = False
        self._host = host

    async def receive_message(self, timeout):
        message_response = await asyncio.wait_for(self._websocket.recv(), timeout=timeout)
        return message_response

    async def send_message(self, message):
        try:
            await self._websocket.send(json.dumps(message))

        except Exception as e2:
            self._connected = False
            print("Websocket Message Process Error Occured")
            print(e2)

        finally:
            if self._websocket != None:
                self._websocket.close()
            print("Connection End")

    async def connect(self, message):
        print("Connecting to " + self._host)
        try:
            # Connect to ETH node
            self._websocket = await connect("ws://" + self._host)
            self._connected = True
            print("Success Connect to " + self._host)

            # Request websocket event
            await self.send_message(message)
            # Receive websocket event
            while True:
                eth_response = await self.receive_message(60)
                pprint.pprint(eth_response)

        except Exception as e1:
            # For reconnect
            self._connected = False
            print("Websocket Connection Error Occured")
            print(e1)

        finally:
            if self._websocket != None:
                self._websocket.close()
            print(self._host + " Connection End")

    async def open(self, message):
        # First connection open
        print("Try Open")
        await self.connect(message)

        # To reconnect
        while True:
            time.sleep(2)
            if not self._connected:
                print("Reconnecting...")
                await self.connect(message)
