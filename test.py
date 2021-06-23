import bluetooth, time
import bluetooth._bluetooth as bluez
import struct
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

search_time = 10
# You can hardcode the desired device ID here as a string to skip the discovery stage
addr = "7C:9A:1D:34:89:4E"

def searchForDevices():
    print("Searching for devices...")

    nearby_devices = bluetooth.discover_devices(duration=search_time, flush_cache=True, lookup_names=True)

    if len(nearby_devices) > 0:
        print("Found %d devices!" % len(nearby_devices))
    else:
        print("No devices found! Please check your Bluetooth device and restart the demo!")
        exit(0)

    i = 0 # Just an incrementer for labeling the list entries
    # Print out a list of all the discovered Bluetooth Devices
    for addr, name in nearby_devices:
        print("%s. %s - %s" % (i, addr, name))
        i += 1

    str_device_num = input("Please specify the number of the device you want to track: ")
    device_num = int(str_device_num)
    # extract out the useful info on the desired device for use later
    addr, name = nearby_devices[device_num][0], nearby_devices[device_num][1]

    return addr, name

def get_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    duration = 4
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    results = []

    done = False
    while not done:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            nrsp = bluetooth.get_byte(pkt[0])
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                rssi = bluetooth.byte_to_signed_int(
                        bluetooth.get_byte(pkt[1+13*nrsp+i]))
                results.append( ( addr, rssi ) )
                print("[%s] RSSI: [%d]" % (addr, rssi))
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            print("get to done (TWO)")
            done = True
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            if status != 0:
                print("uh oh...")
                printpacket(pkt[3:7])
                done = True
        elif event == bluez.EVT_INQUIRY_RESULT:
            pkt = pkt[3:]
            nrsp = bluetooth.get_byte(pkt[0])
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                results.append( ( addr, -1 ) )
                print("[%s] (no RRSI)" % addr)
        else:
            print("unrecognized packet type 0x%02x" % ptype)
        print("event ", event)


    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

    return results

# def getDistance():

def main():
    dev_id = bluez.hci_get_route(addr)
    try:
        socket = bluez.hci_open_dev(dev_id)
        print(dev_id)
        print(socket)
    except:
        print("error accessing bluetooth device...")
        sys.exit(1)

    print("The script will now scan for the device %s." % (addr))

    test = True

    state = bluetooth.lookup_name(addr, timeout=20)
    services = bluetooth.find_service(address=addr)
    print(state)
    rssi = get_rssi(socket)
    print("rssi: ", rssi)


main()
