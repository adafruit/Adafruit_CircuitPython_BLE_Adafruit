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
`adafruit_ble_adafruit.addressable_pixel_service`
================================================================================

BLE control of addressable pixels, such as NeoPixels or DotStars.

* Author(s): Dan Halbert
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Adafruit.git"

import struct

from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Uint8Characteristic

from .adafruit_service import AdafruitService


class AddressablePixelService(AdafruitService):
    """Control of NeoPixels, DotStars, etc."""

    uuid = AdafruitService.adafruit_service_uuid(0x900)
    pixel_pin = Uint8Characteristic(
        uuid=AdafruitService.adafruit_service_uuid(0x901),
        properties=(Characteristic.READ | Characteristic.WRITE),
    )
    """Send data out on this pin."""

    pixel_pin_type = Uint8Characteristic(
        uuid=AdafruitService.adafruit_service_uuid(0x902),
        properties=(Characteristic.READ | Characteristic.WRITE),
    )
    """0 = WS2812 (NeoPixel), 800kHz
    1 = SPI (APA102: DotStar)
    """
    pixel_data = Characteristic(
        uuid=AdafruitService.adafruit_service_uuid(0x903),
        properties=Characteristic.WRITE,
        write_perm=Attribute.NO_ACCESS,
    )
    """\
    start: uint16: start writing data into buffer at this byte number (byte, not pixel)
    flags: uint8: bit 0: 0 = don't write to pixels yet
                         1 = write entire buffer to pixels now
    data: raw array of data for all pixels, in proper color order for type of pixel
    """

    @property
    def parsed_pixel_data(self):
        """Return a tuple (start, write_now, data) corresponding to the
        different parts of ``pixel_data``.
        """
        pixel_data = self.pixel_data
        start = struct.unpack_from("<H", pixel_data)
        write_now = bool(pixel_data[2] & 0x1)
        data = memoryview(pixel_data)[3:]
        return (start, write_now, data)
