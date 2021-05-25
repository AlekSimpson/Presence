import argparse
import asyncio
from typing import Dict
import apikeys
import time

from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo

async def kitchenOn(api_key, my_learning_storage):
    async with Govee(api_key, learning_storage=my_learning_storage) as govee:
            online = await govee.check_connection()
            devices, err = await govee.get_devices()
            devices = (
                await govee.get_states()
            )
            cache_devices = govee.devices
            device = govee.device(devices[0].device)

            success, err = await govee.turn_on(device)

async def kitchenOff(api_key, my_learning_storage):
    async with Govee(api_key, learning_storage=my_learning_storage) as govee:
            online = await govee.check_connection()
            devices, err = await govee.get_devices()
            devices = (
                await govee.get_states()
            )
            cache_devices = govee.devices
            device = govee.device(devices[0].device)

            success, err = await govee.turn_off(device)

class YourLearningStorage(GoveeAbstractLearningStorage):
    async def read(self) -> Dict[str, GoveeLearnedInfo]:
        return (
            {}
        )  # get the last saved learning information from disk, database, ... and return it.

    async def write(self, learned_info: Dict[str, GoveeLearnedInfo]):
        persist_this_somewhere = learned_info  # save this dictionary to disk


# then
learning_storage = YourLearningStorage()

def checkTime():
    now = time.localtime()
    current_time = time.strftime('%H:%M:%S', now)
    hour = int(current_time[0] + current_time[1])
    print("time is above 20 hundred ", hour >= 20)
    return hour >= 20

async def kitchenOn(args):
    if checkTime():
        # going async ...
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(kitchenOff(args.api_key, learning_storage))
        finally:
            loop.close()

async def kitchenOff(args):
    if checkTime():
        # going async ...
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(kitchenOff(args.api_key, learning_storage))
        finally:
            loop.close()

def main():
    parser = argparse.ArgumentParser(description="govee_api_laggat examples")
    parser.add_argument("--api-key", dest="api_key", type=str, required=True)
    args = parser.parse_args(['--api-key', apikeys.apikey])

    # kitchenOn(args)
    time = checkTime()

main()
