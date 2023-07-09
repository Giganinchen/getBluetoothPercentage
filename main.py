import bluetooth

def find_bluetooth_devices():
    nearby_devices = bluetooth.discover_devices()
    return nearby_devices

def get_device_battery(device_address):
    service_matches = bluetooth.find_service(address=device_address)
    for service in service_matches:
        if service["name"] == "Battery":
            return service["host"]
    return None

def get_battery_level(device_address):
    port = get_device_battery(device_address)
    if port:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((device_address, port))
        sock.send(b"\x01\x00\x00")
        data = sock.recv(1024)
        sock.close()
        return ord(data[-1])
    return None

if __name__ == "__main__":
    devices = find_bluetooth_devices()
    for device in devices:
        battery_level = get_battery_level(device)
        if battery_level is not None:
            print("Device:", device)
            print("Battery Level:", battery_level)
            print()
