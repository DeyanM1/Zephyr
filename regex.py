class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def printType(self):
        print(type(self))
        
        
p = Person("John", 11)

p.printType()