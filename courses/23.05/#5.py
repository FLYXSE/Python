class Cook:
    def cook(self):
        return "Готовит еду"
        
class Driver:
    def drive(self):
        return "Водит машину."
        
class FoodCourier(Cook, Driver):
    def deliver(self):
        return "Доставляет еду."


c = Cook()
d = Driver()
fc = FoodCourier()
cc = c.cook()
dd = d.drive()
fcfc = fc.deliver()
print(f"Повар: {cc}\nВодитель: {dd}\nКурьер: {fcfc}")