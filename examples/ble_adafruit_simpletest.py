# For use on a Circuit Playground Bluefruit.
# Easily tested withe the Bluefruit Playground app.

# Act as a BLE peripheral. Provide all possible adafruit_services services.

import board
import neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

class AdafruitService

def update():




def run():
    ble = BLERadio()
    advertisement = ProvideServicesAdvertisement(uart_server)

    while True:
        # Advertise when not connected.
        ble.start_advertising(advertisement)
        while not ble.connected:
            pass
        ble.stop_advertising()

        while ble.connected:
            update()
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, ColorPacket):
            print(packet.color)
            pixels.fill(packet.color)
