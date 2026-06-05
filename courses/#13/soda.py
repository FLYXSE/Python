class Soda:
    def __init__(self, dobavka=None):
        self.dobavka = dobavka

    def show_my_drink(self):
        if self.dobavka:
            print(f"Газировка и {self.dobavka}")
        else:
            print("Обычная газировка")

drink1 = Soda("Лимон")
drink1.show_my_drink()

drink2 = Soda()
drink2.show_my_drink()

drink3 = Soda("Вишня")
drink3.show_my_drink()
