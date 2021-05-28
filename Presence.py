from flask import Flask, request
from KitchenLightsManager import kitchenLightOn, kitchenLightOff
app = Flask(__name__)
@app.route('/', methods=['POST'])

def receieveData():
    return (request.form('room'), request.form('powered')) # On the sending end you will send a json payload and foo (for example) would be the key to whatever data it is representing

#Room - entered,

# Room codes: 0 - Kitchen
# Room functions: 0 - light off, 1 - light on

def loop():
    kitchenFunctions = [kitchenLightOff, kitchenLightOn]
    roomFunctions = [kitchenFunctions]

    lightData = receieveData()
    room = lightData[0]
    powered = lightData[1]

    roomFunctions[room][powered]()

def main(looping):
    if looping:
        while True:
            loop()
    else:
        loop()

main()
