class Bird:
    def fly():
        print("Птица летит")
        
class Penguin(Bird):
    def fly():
        print("Пингвины не летают")
        

b = Bird
p = Penguin
b.fly()
p.fly()