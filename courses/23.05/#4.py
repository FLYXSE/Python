class ElectricDevice:
    def __init__(self, voltage):
        self.voltage = voltage

    def plug_in(self):
        print(f"Вольтаж: {self.voltage}")


class WirelessDevice:
    def __init__(self, battery_life):
        self.battery_life = battery_life

    def connect_bluetooth(self):
        return


class Laptop(ElectricDevice, WirelessDevice):
    def __init__(self, voltage, battery_life, ram):
        super().__init__(battery_life)
        self.ram = ram



l = Laptop(1, 220, 16)
l.plug_in()