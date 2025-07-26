import time
import os
import random

clear = lambda: os.system('cls')

#---------------------------------------------------------------------------------

def afficher(grid):
    for i in range(3):
        ligne = grid[i]
        print(ligne[0], "\033[0m|",ligne[1],"\033[0m|",ligne[2])
        if i != 2:
            print("\033[0m----------")
        time.sleep(0.3)

#---------------------------------------------------------------------------------

def jouer(grid,signe):
    phraseInput = "\033[0mVous voulez joue a quelles case "+signe+" ? "
    inputJoueur = input(phraseInput)
    inputJoueur = int(inputJoueur)
    if inputJoueur <10 and inputJoueur >0:
        if inputJoueur==1:
            if (grid[2][0])==" ":
                grid[2][0]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==2:
            if (grid[2][1])==" ":
                grid[2][1]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==3:
            if (grid[2][2])==" ":
                grid[2][2]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==4:
            if (grid[1][0])==" ":
                grid[1][0]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==5:
            if (grid[1][1])==" ":
                grid[1][1]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==6:
            if (grid[1][2])==" ":
                grid[1][2]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==7:
            if (grid[0][0])==" ":
                grid[0][0]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==8:
            if (grid[0][1])==" ":
                grid[0][1]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
        elif inputJoueur==9:
            if (grid[0][2])==" ":
                grid[0][2]=signe
            else:
                print ("Cette case est deja prise choisissez en une autre. ")
                jouer(grid,signe)
    else:
        print ("La case n'est pas valide veuillez en choisir une autre")
        jouer(grid,signe)
    

#---------------------------------------------------------------------------------

def verifNul (grid):
    verifFull=True
    for y in range(3):
        for x in range(3):
            if grid[y][x]==" ":
                verifFull= False

    return verifFull

#---------------------------------------------------------------------------------

def gagne(grid):
    # Verif ligne
    for y in range(3):
        ligne = grid[y]
        if ligne[0] == ligne[1] == ligne[2] != " ":
            return ligne[0]
        
    # Colonne
    for x in range(3):
        if  grid[0][x] == grid[1][x] == grid[2][x] != " ":
            return grid[0][x]
        
    # Diagonale négative
    if grid[0][0] == grid[1][1] == grid[2][2] != " ":
        return grid[0][0]
    
    # Diagonale positive
    if grid[0][2] == grid[1][1] == grid[2][0] != " ":
        return grid[0][2]
            
    return " "

#---------------------------------------------------------------------------------

signeJ1 = "\033[91mX\033[0m"
signeJ2 = "\033[92m0\033[0m"

compteurJ1 = 0
compteurJ2 = 0

while True:
    valeurRandom = random.randint(0, 100)
    
    if valeurRandom % 2 == 0:
        signe = signeJ1
    else :
        signe = signeJ2


    game = True
    grid= [[" "," "," "],
           [" "," "," "],
           [" "," "," "]]

    while game == True:
        clear()
        print("Joueur",signeJ1,":",compteurJ1, "Joueur",signeJ2,":",compteurJ2)
        afficher(grid)
        jouer(grid, signe)

        if signe == signeJ1:
            signe = signeJ2
        else:
            signe = signeJ1

        joueurGagnant = gagne(grid)

        if joueurGagnant != " ":
            afficher(grid)
            print ("\033[0m\033[1mJoueur ", joueurGagnant, "\033[1m à gagné !\033[0m")

            if joueurGagnant == signeJ1:
                compteurJ1 += 1
            elif joueurGagnant == signeJ2:
                compteurJ2 += 1

            game=False
            time.sleep(1)
            break

        if verifNul(grid)==False:
            continue
        else:
            afficher(grid)
            game=False
            print ("\033[0m\033[1mPartie nul \033[0m")
            time.sleep(1)
            break
    