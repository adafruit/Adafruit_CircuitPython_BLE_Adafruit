# Bluefruit Playground server program, to run on CLUE

from adafruit_service import AdafruitServerAdvertisement

from adafruit_service.accelerometer_service import AccelerometerService
from adafruit_service.addressable_pixel_service import AddressablePixelService
from adafruit_service.barometric_pressure_service import BarometricPressureService
from adafruit_service.button_service import ButtonService
from adafruit_service.gyroscope_service import GyroscopeService
from adafruit_service.humidity_service import HumidityService
from adafruit_service.light_sensor_service import LightSensorService
from adafruit_service.magnetometer_service import MagnetometerService
from adafruit_service.temperature_service import TemperatureService

adv = BluefruitPlaygroundAdvertisement()
# Adafruit Circuit Playground Bluefruit USB PID:
adv.pid = 0x8046  *********** CHANGE

while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    ble.stop_advertising()


    while ble.connected:
