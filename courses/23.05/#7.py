class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        print(f"{self.name} издаёт звук")
        print(f"Этому животному {self.age}\n")


class Mammal(Animal):
    def feed_milk(self):
        print(f"{self.name} кормит молоком")
        print(f"Этому животному {self.age}\n")


class Bird(Animal):
    def lay_eggs(self):
        print(f"{self.name} откладывает яйца")
        print(f"Этому животному {self.age}\n")
        

class Bat(Mammal, Bird):
    def make_sound(self):
        print(f"{self.name} издаёт другой звук.")
        print(f"Этому животному {self.age}\n")

Animal("Рысь", "3 года").make_sound()
Mammal("Корова", "2 года").feed_milk()
Bird("Голубь", "2.5 года").lay_eggs()
Bat("Летучая мышь", "1 год").make_sound()