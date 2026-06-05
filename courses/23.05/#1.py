class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year
        
    def info(self):
        print(f"Brand: {self.brand}\nYear: {self.year}")
        
        
class Car(Vehicle):
    def __init__(self, brand, year, fuel_type):
        super().__init__(brand, year)
        self.fuel_type = fuel_type
        
    def info(self):
        print(f"Brand: {self.brand}\nYear: {self.year}\nFuel Type: {self.fuel_type}")
        
        
vehicle = Vehicle("Toyota", 2020)
vehicle.info()
car = Car("BMW", 2022, "Бензин")
car.info()