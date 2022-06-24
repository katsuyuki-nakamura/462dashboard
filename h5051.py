from struct import unpack_from
from bluepy.btle import Scanner


def twos_complement(n: int, w: int = 16) -> int:
    """Two's complement integer conversion."""
    # Adapted from: https://stackoverflow.com/a/33716541.
    if n & (1 << (w - 1)):
        n = n - (1 << w)
    return n


class H5051:
    def __init__(self):
        self._temperature = 0.0
        self._humidity = 0.0
        self._battery = 0
        self.scanner = Scanner()

    def update(self):
        devices = self.scanner.scan(2.0)
        for dev in devices:
            is_govee = False
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Complete Local Name" and \
                   value == "Govee_H5051_385C":
                    is_govee = True
            if is_govee:
                for (adtype, desc, value) in dev.getScanData():
                    if desc == "Manufacturer":
                        binary = bytes.fromhex(value)
                        a, b, c = unpack_from("<HHB", binary, 3)
                        self._temperature = twos_complement(a, 16)/100
                        self._humidity = b/100
                        self._battery = c

    @property
    def temperature(self):
        return self._temperature

    @property
    def humidity(self):
        return self._humidity

    @property
    def battery(self):
        return self._battery


if __name__ == "__main__":
    h5051 = H5051()
    h5051.update()

    print(h5051.temperature, '℃', h5051.humidity, '%', h5051.battery, '%')
