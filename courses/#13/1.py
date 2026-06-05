class Phone:
    default_color = "Gray"
    default_model = "C385"
    
    def __init__(self, color, model):
        self.color = color
        self.model = model
        
print(Phone.default_color)
print(Phone.default_model)

phone1 = Phone("black", "C67")
print("=" * 50)
print(phone1.color)
print(phone1.model)

iPhone = Phone("Blue", "13 Pro")
print("=" * 50)
print(iPhone.color)
print(iPhone.model)