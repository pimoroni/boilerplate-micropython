class FakeI2C:
    """Stand in for the device on the far end of the bus.

    Model enough of the real register file that the driver can be exercised
    without hardware, then assert against it.

    """

    def __init__(self):
        self.registers = bytearray(256)
        self.writes = []

    def readfrom_mem(self, address, register, length):
        return bytes(self.registers[register:register + length])

    def writeto_mem(self, address, register, buf):
        self.writes.append((register, bytes(buf)))
        for offset, value in enumerate(buf):
            self.registers[register + offset] = value


def test_setup():
    from boilerplate import Boilerplate

    device = Boilerplate(FakeI2C())

    assert device.address == 0x77


def test_version():
    import boilerplate

    assert boilerplate.__version__ == "0.0.1"
