from KitchenLightsManager import kitchenLightOn, kitchenLightOff

#Room - entered,

# Room codes: 0 - Kitchen
# Room functions: 0 - light off, 1 - light on

def lightMan(room, powered):
	kitchenFunctions = [kitchenLightOff, kitchenLightOn]
	roomFunctions = [kitchenFunctions]

	roomFunctions[room][powered]()
