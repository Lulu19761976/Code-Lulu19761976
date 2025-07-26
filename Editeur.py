import pygame

class Button:
    def __init__(self, rect, color, text, font):
        # Initialise le bouton avec sa position, couleur, texte et police
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.font = font

    def draw(self, screen):
        # Dessine le bouton sur l'écran
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (255,255,255))
        screen.blit(text_surf, (self.rect.x+10, self.rect.y+5))

    def is_clicked(self, pos):
        # Retourne True si le bouton a été cliqué (collision avec la souris)
        return self.rect.collidepoint(pos)
    
import os

# Taille de la grille (nombre de cases par côté)
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Taille d'une case en pixels
CELL_SIZE = 40

# Marge entre les cases
MARGIN = 2

# Dimensions de la fenêtre
WIDTH = GRID_WIDTH * CELL_SIZE + 60
HEIGHT = GRID_HEIGHT * CELL_SIZE + 60  # espace pour les boutons

# Chemin du fichier de sauvegarde (dans le même dossier que ce script)
dossier_courant = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(dossier_courant, "level.json")

COLORS = {
  0: (30, 30, 30),  # Couleur par défaut (case éteinte)
  1: (255, 255, 0),  # Couleur jaune
  2: (0, 255, 0),    # Couleur verte
  3: (255, 0, 0),    # Couleur rouge
  4: (0, 0, 255),    # Couleur bleue
  5: (255, 165, 0),  # Couleur orange
  6: (128, 0, 128),  # Couleur violette
  7: (0, 255, 255),  # Couleur cyan
  8: (192, 192, 192)   # Couleur grise
}

import pygame
import json

class Grid:
    def __init__(self):
        # Initialise la grille avec des cases éteintes (0)
        line = [0 for x in range(GRID_WIDTH)]
        self.grid = [line.copy() for y in range(GRID_HEIGHT)]

    def draw(self, screen):
        # Dessine la grille sur l'écran
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE-MARGIN, CELL_SIZE-MARGIN)
                color = COLORS[self.grid[y][x]]
                pygame.draw.rect(screen, color, rect)

    def set_tile(self, x, y, tile):
        self.grid[y][x] = tile

    def save(self, path):
        # Sauvegarde la grille dans un fichier JSON, une ligne par ligne
        with open(path, "w") as f:
            f.write("[\n")
            for i, row in enumerate(self.grid):
                line = json.dumps(row)
                if i < len(self.grid) - 1:
                    f.write(f"  {line},\n")
                else:
                    f.write(f"  {line}\n")
            f.write("]\n")

    def load(self, path):
        # Charge la grille depuis un fichier JSON
        with open(path, "r") as f:
            data = json.load(f)
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    self.grid[y][x] = data[y][x]


class LevelEditor:
    def __init__(self):
        pygame.init()
        # Création de la fenêtre principale
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Éditeur de niveau simple")
        self.font = pygame.font.SysFont(None, 32)
        # Création de la grille
        self.grid = Grid()
        # Création des boutons Enregistrer et Charger
        self.save_btn = Button((10, HEIGHT - 50, 140, 40), (70, 200, 70), "Enregistrer", self.font)
        self.load_btn = Button((WIDTH-130, HEIGHT - 50, 120, 40), (70, 70, 200), "Charger", self.font)
        
        # Création des boutons de couleur
        self.color_btns = [
            Button((WIDTH - 50, i * 50, 40, 40), COLORS[i], str(i), self.font)
            for i in range(len(COLORS))
        ]
        
        self.selected_tile = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quitter l'application
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Clic normal (bouton gauche)
                    if event.button == 1:
                        mx, my = event.pos
                        # Si clic dans la grille
                        if my < GRID_HEIGHT * CELL_SIZE:
                            x = mx // CELL_SIZE
                            y = my // CELL_SIZE
                            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                                self.grid.set_tile(x, y, self.selected_tile)
                        # Si clic sur le bouton Enregistrer
                        elif self.save_btn.is_clicked((mx, my)):
                            self.grid.save(SAVE_FILE)
                            print("Niveau enregistré.")
                        # Si clic sur le bouton Charger
                        elif self.load_btn.is_clicked((mx, my)):
                            if os.path.exists(SAVE_FILE):
                                self.grid.load(SAVE_FILE)
                                print("Niveau chargé.")
                        
                        # Vérifier les clics sur les boutons de couleur
                        for index, btn in enumerate(self.color_btns):
                            # Mettre à jour la position Y du bouton avec l'offset
                            btn_rect = btn.rect.copy()
                            if btn_rect.collidepoint(pygame.mouse.get_pos()):
                                self.selected_tile = index
                                print(f"Couleur sélectionnée : {index}")

            # Affichage de l'interface
            self.screen.fill((50, 50, 50))
            self.grid.draw(self.screen)
            self.save_btn.draw(self.screen)
            self.load_btn.draw(self.screen)
            
            # Zone de défilement pour les boutons de couleur
            color_area = pygame.Rect(WIDTH - 60, 0, 60, HEIGHT - 60)
            pygame.draw.rect(self.screen, (40, 40, 40), color_area)
            
            # Afficher les boutons de couleur avec l'offset
            for index, btn in enumerate(self.color_btns):
                btn.draw(self.screen)
            
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    # Lancement de l'éditeur de niveau
    LevelEditor().run()