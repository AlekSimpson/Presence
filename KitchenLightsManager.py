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
		if devices[0].power_state != True:
			for device in cache_devices:
				success, eff = await govee.turn_on(device)
		else:
			print("already on")

async def kitchenOff(api_key, my_learning_storage):
	async with Govee(api_key, learning_storage=my_learning_storage) as govee:
		online = await govee.check_connection()
		devices, err = await govee.get_devices()
		devices = (
			await govee.get_states()
		)
		cache_devices = govee.devices
		if devices[0].power_state != False:
			for device in cache_devices:
				success, err = await govee.turn_off(device)
		else:
			print("already off")

class YourLearningStorage(GoveeAbstractLearningStorage):
    async def read(self) -> Dict[str, GoveeLearnedInfo]:
        return (
            {}
        )  # get the last saved learning information from disk, database, ... and return it.

    async def write(self, learned_info: Dict[str, GoveeLearnedInfo]):
        persist_this_somewhere = learned_info  # save this dictionary to disk

learning_storage = YourLearningStorage()

def checkTime():
    now = time.localtime()
    current_time = time.strftime('%H:%M:%S', now)
    hour = int(current_time[0] + current_time[1])
    print("time is above 20 hundred ", hour >= 20)
    return hour >= 20

def kitchenLightOn():
	parser = argparse.ArgumentParser(description="govee_api_laggat examples")
	parser.add_argument("--api-key", dest="api_key", type=str, required=True)
	args = parser.parse_args(['--api-key', apikeys.apikey])
	# going async ...
	# if checkTime():
	asyncio.run(kitchenOn(args.api_key, learning_storage))

def kitchenLightOff():
	parser = argparse.ArgumentParser(description="govee_api_laggat examples")
	parser.add_argument("--api-key", dest="api_key", type=str, required=True)
	args = parser.parse_args(['--api-key', apikeys.apikey])

	# going async ...
	# if checkTime():
	asyncio.run(kitchenOff(args.api_key, learning_storage))

