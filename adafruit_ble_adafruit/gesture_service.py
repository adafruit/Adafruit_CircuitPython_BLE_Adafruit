# The MIT License (MIT)
#
# Copyright (c) 2020 Dan Halbert for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ble_adafruit.gesture_service`
================================================================================

BLE access to gesture detector.

* Author(s): Dan Halbert
"""
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Adafruit.git"

from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Uint8Characteristic
from adafruit_ble_adafruit.adafruit_service import AdafruitService


class GestureService(AdafruitService):  # pylint: disable=too-few-public-methods
    """Gesture sensor."""

    UP = 1  # pylint: disable=invalid-name
    """swipe up"""
    DOWN = 2
    """swipe down"""
    LEFT = 3
    """swipe left"""
    RIGHT = 4
    """swipe right"""

    uuid = AdafruitService.adafruit_service_uuid(0xF00)
    gesture = Uint8Characteristic(
        uuid=AdafruitService.adafruit_service_uuid(0xF01),
        properties=(Characteristic.READ | Characteristic.NOTIFY),
        read_perm=Attribute.OPEN,
        write_perm=Attribute.NO_ACCESS,
    )
    """
    0: no gesture
    1: swipe up (`UP`)
    2: swipe down (`DOWN`)
    3: swipe left (`LEFT`)
    4: swipe right (`RIGHT`)
    """
    measurement_period = AdafruitService.measurement_period_charac(0)
    """Initially 0: send notification only on changes. -1 means stop reading."""
