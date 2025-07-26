#  Operation---------------------------------------------------------

def addition(nombre_1=0,nombre_2=0):
    resultat=nombre_1+nombre_2
    return resultat

def soustraction(nombre_1=0,nombre_2=0):
    resultat=nombre_1-nombre_2
    return resultat

def division(nombre_1=0,nombre_2=0):
    resultat=nombre_1/nombre_2
    return resultat

def multiplication(nombre_1=0,nombre_2=0):
    resultat=nombre_1*nombre_2
    return resultat

#  Autres--------------------------------------------------------------------

def demmande_utilisateur(message="Entrez une valeur"):
    user_input=input(message)
    print("Vous avez entrer: ", user_input)
    return user_input
