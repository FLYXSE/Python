class X:
    def info(self):
        print("X")


class Y(X):
    def info(self):
        print("Y")
        super().info()


class Z(X):
    def info(self):
        print("Z")
        super().info()


class W(Y, Z):
    def info(self):
        super().info()


W().info()