from flask import Flask, request
from KitchenLightsManager import kitchenLightOn, kitchenLightOff
app = Flask(__name__)
@app.route('/', methods=['POST'])

def receieveData():
    return request.form('room') # On the sending end you will send a json payload and foo (for example) would be the key to whatever data it is representing

#Room - entered,

# Room codes: 0 - Kitchen
# Room functions: 0 - light off, 1 - light on 

def main():
    kitchenFunctions = [kitchenLightOff, kitchenLightOn]
    roomFunctions = [kitchenFunctions]
    # room = receieveData()
    roomFunctions[0][1]()


main()
