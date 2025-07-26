# Importation----------------------------------------------------------

from functions import addition,soustraction,multiplication,division,demmande_utilisateur

# Variable---------------------------------------------------------------

nombre_1=demmande_utilisateur("Choisir un nombre 1: ")
nombre_1=int(nombre_1)
nombre_2=demmande_utilisateur("Choisir un nombre 2: ")
nombre_2=int(nombre_2)
operation=demmande_utilisateur("Choisir l'operation: ")
resultat=0

# Programme principale---------------------------------------------------

print("Vous voulez faire:",nombre_1,operation,nombre_2)
print("Le resultat est:")

if operation=="+":
    resultat=addition(nombre_1,nombre_2)

elif operation=="-":
    resultat=soustraction(nombre_1,nombre_2)

elif operation=="*":
    resultat=multiplication(nombre_1,nombre_2)

elif operation=="/":
    resultat=division(nombre_1,nombre_2)
    
print(resultat)
