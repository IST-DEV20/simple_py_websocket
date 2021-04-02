#!/usr/bin/env python3

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import time

logging.basicConfig()

STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps({"type": "state", **STATE})


def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


async def notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_firmware_state(filename):
    if USERS:  # asyncio.wait doesn't accept an empty list
        i=0
        while (i <= 100):
            message = json.dumps({"action":"firmware","progress": i,"message":"un zip ..."})
            await asyncio.wait([user.send(message) for user in USERS])
            i=i+1
            time.sleep(1)
        print("Update firmware completed.")
        await asyncio.wait([user.close() for user in USERS])
        

async def notify_web_state(filename):
    if USERS:  # asyncio.wait doesn't accept an empty list
        i=0
        while (i <= 100):
            message = json.dumps({"action":"web","progress": i,"message":"update ...."})
            await asyncio.wait([user.send(message) for user in USERS])
            i=i+1
            time.sleep(1)
        print("Update web GUI completed.")
        await asyncio.wait([user.close() for user in USERS])

async def notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def notify_version():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = json.dumps({"action":"firmware","version": "202104565656"})
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "firmware":
                print("update firmware..:" + data["filename"])
                await notify_firmware_state(data["filename"])
            elif data["action"] == "version":
                print("get firmware version")
                await notify_version()
            else:
                logging.error("unsupported event: {}", data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
