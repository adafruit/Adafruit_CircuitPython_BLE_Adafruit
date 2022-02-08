# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_ble_adafruit.adafruit_service`
================================================================================

Access to sensors and hardware on or connected to BLE-capable boards.

* Author(s): Dan Halbert

Implementation Notes
--------------------

**Hardware:**

* `Adafruit CircuitPlayground Bluefruit <https://www.adafruit.com/product/4333>`_
* `Adafruit CLUE nRF52840 Express <https://www.adafruit.com/product/4500>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Adafruit.git"

import struct

from micropython import const

from adafruit_ble.advertising import Advertisement, LazyObjectField
from adafruit_ble.advertising.standard import ManufacturerData, ManufacturerDataField
from adafruit_ble.advertising.adafruit import (
    MANUFACTURING_DATA_ADT,
    ADAFRUIT_COMPANY_ID,
)
from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.characteristics.int import Int32Characteristic, Uint32Characteristic
from adafruit_ble.uuid import VendorUUID
from adafruit_ble.services import Service

try:
    from typing import Optional
    from _bleio import ScanEntry
except ImportError:
    pass


_PID_DATA_ID = const(0x0001)  # This is the same as the Radio data id, unfortunately.


class AdafruitServerAdvertisement(
    Advertisement
):  # pylint: disable=too-few-public-methods
    """Advertise the Adafruit company ID and the board USB PID."""

    match_prefixes = (
        struct.pack(
            "<BHBH",
            MANUFACTURING_DATA_ADT,
            ADAFRUIT_COMPANY_ID,
            struct.calcsize("<HH"),
            _PID_DATA_ID,
        ),
    )
    manufacturer_data = LazyObjectField(
        ManufacturerData,
        "manufacturer_data",
        advertising_data_type=MANUFACTURING_DATA_ADT,
        company_id=ADAFRUIT_COMPANY_ID,
        key_encoding="<H",
    )
    pid = ManufacturerDataField(_PID_DATA_ID, "<H")
    """The USB PID (product id) for this board."""

    def __init__(self, *, entry: Optional[ScanEntry] = None) -> None:
        super().__init__(entry=entry)
        # Return early if things have been set by an existing ScanEntry.
        if entry:
            return
        # Creating an advertisement to send.
        self.connectable = True
        self.flags.general_discovery = True
        self.flags.le_only = True


class AdafruitService(Service):
    """Common superclass for all Adafruit board services."""

    @staticmethod
    def adafruit_service_uuid(n: int) -> VendorUUID:
        """Generate a VendorUUID which fills in a 16-bit value in the standard
        Adafruit Service UUID: ADAFnnnn-C332-42A8-93BD-25E905756CB8.
        """
        return VendorUUID("ADAF{:04x}-C332-42A8-93BD-25E905756CB8".format(n))

    @classmethod
    def measurement_period_charac(cls, msecs: int = 1000) -> Int32Characteristic:
        """Create a measurement_period Characteristic for use by a subclass."""
        return Int32Characteristic(
            uuid=cls.adafruit_service_uuid(0x0001),
            properties=(Characteristic.READ | Characteristic.WRITE),
            initial_value=msecs,
        )

    @classmethod
    def service_version_charac(cls, version: int = 1) -> Uint32Characteristic:
        """Create a service_version Characteristic for use by a subclass."""
        return Uint32Characteristic(
            uuid=cls.adafruit_service_uuid(0x0002),
            properties=Characteristic.READ,
            write_perm=Attribute.NO_ACCESS,
            initial_value=version,
        )
