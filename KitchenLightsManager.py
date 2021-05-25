import argparse
import asyncio
from typing import Dict
import apikeys

from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo

async def turnOnKitchenLight(api_key, my_learning_storage):
    async with Govee(api_key, learning_storage=my_learning_storage) as govee:
            online = await govee.check_connection()
            devices, err = await govee.get_devices()
            devices = (
                await govee.get_states()
            )
            cache_devices = govee.devices
            device = govee.device(devices[0].device)

            success, err = await govee.turn_on(device)

async def turnOffKitchenLight(api_key, my_learning_storage):
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
your_learning_storage = YourLearningStorage()

def main():
    parser = argparse.ArgumentParser(description="govee_api_laggat examples")
    parser.add_argument("--api-key", dest="api_key", type=str, required=True)
    args = parser.parse_args(['--api-key', apikeys.apikey])

    # going async ...
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(turnOffKitchenLight(args.api_key, your_learning_storage))
    finally:
        loop.close()

main()
