# Pour remplacer tout un nom : selectionez le mot , ctrl + H, choisir le remplacant puis clicket sur replace all

# Changer la couleur du texte dans la console :
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

print(color.BOLD + 'Hello, World!' + color.END)

# Turtle
from turtle import * #initialiser
from math import *
from random import*

forward(100) #avancer

# tourner
left(90)
right(45)

# forme
for i in range(4):
    left(90)
    forward(50)
    right(90)              # Croix
    forward(50)
    left(90)
    forward(100)           

penup()
left(90)
forward(100)
pendown()
for i in range (100):
    
    forward(4.4)           # Rond
    left(5)


for i in range(50000000):
    forward(i)               # Spirale
    right(90)

for i in range(5000000):
    forward((i*i)/50)         # Tunel
    right(90)


for i in range(500000000):
    forward(i-500)               # Piramide
    right(90)


speed(10000000)
color('green','yellow')
begin_fill()
for i in range(4):
    left(90)
    forward(50)
    right(90)              
    forward(50)
    left(90)
    forward(100)            # Croix,rong collore
end_fill()

penup()
left(90)
forward(100)
pendown()
color('black','red')
begin_fill()
for i in range (75):
    
    forward(4.4)         
    left(5)
end_fill()




def forme(rayon,nombre_de_cote,position):
    penup()
    precision = 6.28/nombre_de_cote
    i = 0
    while i <=3.14*2:
        x = cos(i) *rayon + position[0]
        y = sin(i) *rayon + position[1]
        
        setpos((x,y))
        pendown()

        if (i+precision > 3.14*2 and i != 3.14*2):           # Fait des forme geometrique(specifiez le nombre de cote)
            i = 3.14*2
        else:
            i+= precision

for i in range(200):
    rayonRandom = randint(10, 50)
    xRandom = randint(-300, 300)
    yRandom = randint(-300, 300)
    forme(rayon=rayonRandom,nombre_de_cote=4,position=(xRandom,yRandom))
