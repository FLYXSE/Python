class Device:
    def __init__(self, brand):
        self.brand = brand
        
    def turn_on():
        print("ERROR. ОС отсутствует!")
        
class Smartphone(Device):
    def __init__(self, brand, os):
        super().__init__(brand)
        self.os = os
    
    def turn_on():
        print("ОС Загружается.")
        
d = Device
s = Smartphone
d.turn_on()
s.turn_on()