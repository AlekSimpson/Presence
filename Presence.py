from KitchenLightsManager import kitchenLightOn, kitchenLightOff

#Room - entered,

# Room codes: 0 - Kitchen
# Room functions: 0 - light off, 1 - light on

def lightMan(room, powered):
    kitchenFunctions = [kitchenLightOff, kitchenLightOn]
    roomFunctions = [kitchenFunctions]

    print("got to light man")
    roomFunctions[0][1]()

# def main(looping):
#     if looping:
#         while True:
#             loop()
#     else:
#         loop()
#
# main()
