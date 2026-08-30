from micropython import const

__version__ = "0.0.1"

DEFAULT_ADDRESS = const(0x77)


# Rename me!
class Boilerplate:
    def __init__(self, i2c, address=DEFAULT_ADDRESS):
        """Initialise the device.

        :param i2c: an initialised machine.I2C instance
        :param address: i2c address of the device

        """
        self.i2c = i2c
        self.address = address

    def _read(self, register, length=1):
        return self.i2c.readfrom_mem(self.address, register, length)

    def _write_u8(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes([value & 0xFF]))
