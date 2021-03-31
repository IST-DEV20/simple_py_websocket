#!/usr/bin/env python3

# WS client example
import asyncio
import json
import logging
import websockets
import time

async def hello():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        #name = input("What's your name? ")
        name = "web_user"
        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


        message = json.dumps({"action":"firmware","name": "2021-03-31.zip"})
        await websocket.send(message)

        # async for message in websocket:
        #     print(f"> {message}")

        # greeting = await websocket.recv()
        # print(f"< {greeting}")




asyncio.get_event_loop().run_until_complete(hello())
#asyncio.get_event_loop().run_forever()