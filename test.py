from math import *
def carre(nombre):
    res=nombre*nombre
    return res

def delta(nombre1,nombre2):
    return nombre1-nombre2
nb=delta(4,2)
print(nb)

x1=0
y1=4
x2=1
y2=3

dx=delta(x2,x1)
dy=delta(y2,y1)

res=sqrt(carre(dx)+carre(dy))
print(res)
  