# Bluefruit Playground server program, to run on Circuit Playground Bluefruit

import time

from adafruit_ble import BLERadio

from adafruit_ble_adafruit.adafruit_service import AdafruitServerAdvertisement

from adafruit_ble_adafruit.accelerometer_service import AccelerometerService
from adafruit_ble_adafruit.addressable_pixel_service import AddressablePixelService
from adafruit_ble_adafruit.button_service import ButtonService
from adafruit_ble_adafruit.light_sensor_service import LightSensorService
from adafruit_ble_adafruit.temperature_service import TemperatureService
from adafruit_ble_adafruit.tone_service import ToneService

from adafruit_circuitplayground import cp

accel_svc = AccelerometerService()
accel_svc.measurement_period = 100
accel_last_update = 0

neopixel_svc = AddressablePixelService()


button_svc = ButtonService()
button_svc.set_pressed(cp.switch, cp.button_a, cp.button_b)

light_svc = LightSensorService()
light_svc.measurement_period = 100
light_last_update = 0

temp_svc = TemperatureService()
temp_svc.measurement_period = 100
temp_last_update = 0

tone_svc = ToneService()
# Nothing playing now.
last_tone = (0, 0)
tone_last_freq = 0
tone_playing = False

ble = BLERadio()

# Adafruit Circuit Playground Bluefruit USB PID:
# Arduino: 0x8045,  CircuitPython: 0x8046, app supports either
adv = AdafruitServerAdvertisement(0x8046)

while True:
    # Advertise when not connected.
    ble.start_advertising(adv)
    while not ble.connected:
        pass
    ble.stop_advertising()

    while ble.connected:
        now_msecs = time.monotonic_ns() // 10000000

        if now_msecs - accel_last_update > accel_svc.measurement_period:
            accel_svc.acceleration = cp.acceleration
            accel_last_update = now_msecs

        if now_msecs - light_last_update > light_svc.measurement_period:
            light_svc.light_level = cp.light
            light_last_update = now_msecs

        if now_msecs - temp_last_update > temp_svc.measurement_period:
            temp_svc.temperature = cp.temperature
            temp_last_update = now_msecs

        button_svc.set_pressed(cp.switch, cp.button_a, cp.button_b)

        tone = tone_svc.tone
        if tone != last_tone:
            print(tone)
            freq, duration = tone
            if freq != 0:
                if duration != 0:
                    # Note that this blocks. Alternatively we could
                    # use now_msecs to time a tone in a non-blocking
                    # way, but then the other updates might make the
                    # tone interval less consistent.
                    cp.play_tone(freq, duration)
                else:
                    cp.stop_tone()
                    cp.start_tone(freq)
            else:
                cp.stop_tone()
        last_tone = tone
