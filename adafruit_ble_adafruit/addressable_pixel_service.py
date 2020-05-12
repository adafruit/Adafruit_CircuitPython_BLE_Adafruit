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

from collections import namedtuple
import struct

import _bleio

from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic, ComplexCharacteristic
from adafruit_ble.characteristics.int import Uint8Characteristic
from adafruit_ble_adafruit.adafruit_service import AdafruitService

PixelValues = namedtuple("PixelValues", ("start", "write_now", "data"),)
"""Namedtuple for pixel data and instructions.

* start

    start writing data into buffer at this byte number (byte, not pixel)

* write_now

    ``True`` if data should be written to pixels now.
    ``False`` if write should not happen immediately.

* data

    sequence of bytes of data for all pixels, in proper color order for type of pixel
"""


class _PixelPacket(ComplexCharacteristic):
    """
    start: uint16: start writing data into buffer at this byte number (byte, not pixel)
    flags: uint8: bit 0: 0 = don't write to pixels yet
                         1 = write entire buffer to pixels now
    data: raw array of data for all pixels, in proper color order for type of pixel
    """

    uuid = AdafruitService.adafruit_service_uuid(0x903)

    def __init__(self):
        super().__init__(
            properties=Characteristic.WRITE,
            read_perm=Attribute.NO_ACCESS,
            max_length=512,
        )

    def bind(self, service):
        """Binds the characteristic to the given Service."""
        # Set Characteristic's max length, based on value from AddressablePixelService.
        # + 3 is for size of start and flags
        bound_characteristic = super().bind(service)
        return _bleio.PacketBuffer(bound_characteristic, buffer_size=1)


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
    """
    0 = WS2812 (NeoPixel), 800kHz
    1 = SPI (APA102: DotStar)
    """
    _pixel_packet = _PixelPacket()
    """Pixel-setting data. max_length is supplied on binding."""

    def __init__(self, service=None):
        self._pixel_packet_buf = None
        super().__init__(service=service)

    @property
    def values(self):
        """Return a tuple (start, write_now, data) corresponding to the
        different parts of ``_pixel_packet``.
        """
        if self._pixel_packet_buf is None:
            self._pixel_packet_buf = bytearray(
                self._pixel_packet.packet_size  # pylint: disable=no-member
            )
        buf = self._pixel_packet_buf
        if self._pixel_packet.readinto(buf) == 0:  # pylint: disable=no-member
            # No new values available
            return None

        return PixelValues(
            struct.unpack_from("<H", buf)[0], bool(buf[2] & 0x1), buf[3:],
        )
