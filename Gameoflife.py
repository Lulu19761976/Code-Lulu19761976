import pygame

import pygame
from camera import Camera

class Button:
    """
    Classe représentant un bouton graphique dans Pygame.
    Permet d'afficher un bouton et de détecter les clics dessus.
    """

    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font, bg_color=(100,100,100), text_color=(255,255,255)):
        """
        Initialise le bouton.
        - rect : zone du bouton (position et taille)
        - text : texte affiché sur le bouton
        - font : police utilisée pour le texte
        - bg_color : couleur de fond du bouton (optionnel)
        - text_color : couleur du texte (optionnel)
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        # Prépare le texte à afficher (surface Pygame)
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def draw(self, surface):
        """
        Dessine le bouton sur la surface donnée (l'écran ou une image).
        """
        pygame.draw.rect(surface, self.bg_color, self.rect)  # Dessine le rectangle du bouton
        txt_rect = self.text_surface.get_rect(center=self.rect.center)  # Centre le texte dans le bouton
        surface.blit(self.text_surface, txt_rect)  # Affiche le texte

    def is_hover(self, pos):
        """
        Vérifie si la position (pos) de la souris est sur le bouton.
        Utile pour détecter les clics.
        """
        return self.rect.collidepoint(pos)
    
class Grid:
    """
    Classe qui gère la grille du Jeu de la vie de Conway.
    Chaque cellule peut être vivante (1) ou morte (0).
    """

    def __init__(self, rows, cols):
        """
        Initialise la grille avec le nombre de lignes et de colonnes donné.
        Toutes les cellules sont mortes au départ.
        """
        self.rows = rows
        self.cols = cols
        self.reset()  # Crée la grille vide

    def reset(self):
        """
        Remet toutes les cellules à zéro (mortes).
        """
        self.cells = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def randomize(self, prob=0.2):
        """
        Remplit la grille avec des cellules vivantes aléatoirement.
        prob : probabilité qu'une cellule soit vivante (entre 0 et 1).
        """
        from random import random
        self.cells = [[1 if random() < prob else 0 for _ in range(self.cols)] for _ in range(self.rows)]

    def count_neighbors(self, r, c):
        """
        Compte le nombre de cellules vivantes autour de la cellule (r, c).
        Les voisins sont les 8 cellules autour (haut, bas, gauche, droite, diagonales).
        """
        count = 0
        for i in range(r-1, r+2):      # Parcourt les lignes voisines
            for j in range(c-1, c+2):  # Parcourt les colonnes voisines
                # Ignore la cellule centrale et les indices hors grille
                if (i == r and j == c) or i < 0 or j < 0 or i >= self.rows or j >= self.cols:
                    continue
                count += self.cells[i][j]  # Ajoute 1 si la cellule est vivante
        return count

    def next_generation(self):
        """
        Calcule la prochaine génération selon les règles du Jeu de la vie :
        - Une cellule vivante avec 2 ou 3 voisins survit.
        - Une cellule morte avec exactement 3 voisins devient vivante.
        - Sinon, la cellule meurt ou reste morte.
        """
        new = [[0] * self.cols for _ in range(self.rows)]  # Nouvelle grille
        for r in range(self.rows):
            for c in range(self.cols):
                n = self.count_neighbors(r, c)
                if self.cells[r][c] == 1 and n in (2, 3):
                    new[r][c] = 1  # Survie
                elif self.cells[r][c] == 0 and n == 3:
                    new[r][c] = 1  # Naissance
                # Sinon, reste morte (0)
        self.cells = new  # Met à jour la grille

    def toggle(self, r, c, value=None):
        """
        Change l'état d'une cellule (vivante/morte).
        - Si value est None : inverse l'état (vivant <-> mort).
        - Si value vaut 0 ou 1 : force la cellule à cette valeur.
        """
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if value is None:
                self.cells[r][c] = 1 - self.cells[r][c]
            else:
                self.cells[r][c] = value

class Camera:
    """
    La classe Camera permet de "déplacer" la vue sur une grande grille.
    Elle gère le zoom (taille des cellules) et le déplacement (x, y) de la fenêtre d'affichage.
    """
    def __init__(self, world_width, world_height, view_width, view_height, cell_size):
        """
        Initialise la caméra.
        - world_width, world_height : dimensions de la grille (en nombre de cellules)
        - view_width, view_height : dimensions de la fenêtre d'affichage (en pixels)
        - cell_size : taille d'une cellule (en pixels)
        """
        self.world_width = world_width
        self.world_height = world_height
        self.view_width = view_width
        self.view_height = view_height
        self.cell_size = cell_size
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        """
        Déplace la caméra de dx pixels horizontalement et dy pixels verticalement.
        Empêche la caméra de sortir des limites de la grille.
        """
        self.x = min(max(self.x + dx, 0), self.world_width * self.cell_size - self.view_width)
        self.y = min(max(self.y + dy, 0), self.world_height * self.cell_size - self.view_height)

    def apply(self, col, row):
        """
        Convertit les coordonnées (colonne, ligne) d'une cellule en coordonnées (x, y) à l'écran,
        en tenant compte du zoom et du déplacement de la caméra.
        Retourne les coordonnées en pixels pour dessiner la cellule.
        """
        px = col * self.cell_size - self.x
        py = row * self.cell_size - self.y
        return px, py
    


# --- Paramètres de la fenêtre et de la grille ---
CELL_SIZE = 20      # Taille d'une cellule en pixels
COLS = 100          # Nombre de colonnes dans la grille
ROWS = 100          # Nombre de lignes dans la grille
WIDTH = 800         # Largeur de la fenêtre d'affichage
HEIGHT = 600        # Hauteur de la fenêtre d'affichage
BUTTON_PANEL_HEIGHT = 50  # Hauteur de la zone des boutons
SCREEN_HEIGHT = HEIGHT + BUTTON_PANEL_HEIGHT  # Hauteur totale

# --- Variables globales de simulation ---
running = False     # Indique si la simulation est en cours
step_flag = False   # Indique si on doit avancer d'une génération
grid_obj = Grid(ROWS, COLS)  # La grille du jeu

def bresenham_line(x0, y0, x1, y1):
    """
    Algorithme de Bresenham pour dessiner une ligne entre deux points sur une grille.
    Retourne la liste des coordonnées (row, col) de toutes les cellules traversées.
    Utile pour dessiner en glissant la souris rapidement.
    """
    points = []
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    error = delta_x - delta_y
    while True:
        points.append((y0, x0))
        if x0 == x1 and y0 == y1:
            break
        error2 = 2 * error
        if error2 > -delta_y:
            error -= delta_y
            x0 += step_x
        if error2 < delta_x:
            error += delta_x
            y0 += step_y
    return points

def game_loop():
    """
    Fonction principale qui gère la boucle du jeu :
    - Affichage
    - Gestion des événements (souris, clavier)
    - Simulation du jeu de la vie
    """
    global running, step_flag, grid_obj
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jeu de la vie")
    clock = pygame.time.Clock()

    # Caméra pour déplacer et zoomer sur la grille
    cam = Camera(COLS, ROWS, WIDTH, HEIGHT, CELL_SIZE)
    cell_size = CELL_SIZE

    # Variables pour le dessin en glissé
    drawing = False      # True si on est en train de dessiner avec la souris
    draw_value = None    # Valeur à dessiner (1 = vivant, 0 = mort)
    last_cell = None     # Dernière cellule modifiée (pour tracer une ligne)

    # Préparer la police et les boutons
    font = pygame.font.SysFont(None, 24)
    btn_w, btn_h, spacing = 80, 30, 10
    names = ['Start', 'Stop', 'Step', 'Randomize', 'Clear', 'Quit']
    buttons = {}
    for i, name in enumerate(names):
        x = spacing + i * (btn_w + spacing)
        y = HEIGHT + 10
        rect = pygame.Rect(x, y, btn_w, btn_h)
        buttons[name] = Button(rect, name, font)

    while True:
        # --- Gestion des événements clavier/souris ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Relâchement du bouton souris : on arrête de dessiner
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                last_cell = None

            # Gestion des touches clavier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key == pygame.K_SPACE:
                    running = not running  # Pause ou reprise
                elif event.key == pygame.K_RETURN:
                    step_flag = True       # Avancer d'une génération
                elif event.key == pygame.K_r:
                    grid_obj.randomize()   # Remplir la grille aléatoirement
                elif event.key == pygame.K_c:
                    grid_obj.reset()       # Vider la grille

            # Zoom avec la molette de la souris
            elif event.type == pygame.MOUSEWHEEL:
                # On veut zoomer autour du centre de l'écran
                old_size = cell_size
                
                center_x = WIDTH / 2
                center_y = HEIGHT / 2
                
                # Coordonnées du centre dans le "monde" (grille)
                
                world_cx = (cam.x + center_x) / old_size
                world_cy = (cam.y + center_y) / old_size
                
                # Ajuster la taille des cellules
                if event.y > 0:
                    cell_size = min(cell_size + 2, 200)
                elif event.y < 0:
                    min_size = max(WIDTH // COLS, HEIGHT // ROWS)
                    cell_size = max(cell_size - 2, min_size)
                    
                cam.cell_size = cell_size  # Mettre à jour la caméra
                # Recentrer la caméra pour garder le même centre
                cam.x = world_cx * cell_size - center_x
                cam.y = world_cy * cell_size - center_y
                # Empêcher la caméra de sortir des limites
                cam.x = min(max(cam.x, 0), COLS * cell_size - WIDTH)
                cam.y = min(max(cam.y, 0), ROWS * cell_size - HEIGHT)

            # Clic souris : soit dessiner une cellule, soit cliquer un bouton
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < HEIGHT:
                    # Clic sur la grille : début du dessin
                    col = int((x + cam.x) // cell_size)
                    row = int((y + cam.y) // cell_size)
                    
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        drawing = True
                        
                        # On choisit la couleur selon la cellule cliquée
                        draw_value = 1 if grid_obj.cells[row][col] == 0 else 0
                        grid_obj.toggle(row, col, draw_value)
                        last_cell = (row, col)
                else:
                    # Clic sur un bouton
                    for name, btn in buttons.items():
                        if btn.is_hover((x, y)):
                            if name == 'Start': running = True
                            elif name == 'Stop': running = False
                            elif name == 'Step': step_flag = True
                            elif name == 'Randomize': grid_obj.randomize()
                            elif name == 'Clear': grid_obj.reset()
                            elif name == 'Quit': pygame.quit(); return

        # --- Dessin en glissé (maintenir le bouton souris) ---
        if drawing:
            mx, my = pygame.mouse.get_pos()
            if my < HEIGHT:
                c = int((mx + cam.x) // cell_size)
                r = int((my + cam.y) // cell_size)
                
                if 0 <= r < ROWS and 0 <= c < COLS:
                    # Tracer une ligne entre la dernière cellule et la nouvelle
                    if last_cell is not None:
                        r0, c0 = last_cell
                        for rr, cc in bresenham_line(c0, r0, c, r):
                            grid_obj.toggle(rr, cc, draw_value)
                            last_cell = (rr, cc)
                    
                    # Mettre à jour la dernière cellule
                    last_cell = (r, c)

        # --- Simulation du jeu de la vie ---
        if step_flag:
            grid_obj.next_generation()  # Avancer d'une génération
            step_flag = False
        if running:
            grid_obj.next_generation()  # Avancer automatiquement

        # --- Affichage ---
        screen.fill((0, 0, 0))  # Fond noir

        # Dessiner la grille (uniquement les cellules vivantes)
        for r in range(ROWS):
            for c in range(COLS):
                if grid_obj.cells[r][c] == 1:
                    px, py = cam.apply(c, r)
                    # On ne dessine que si la cellule est visible à l'écran
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        pygame.draw.rect(screen, (0,255,0),(px,py,cell_size-1,cell_size-1))

        # Dessiner les boutons
        for btn in buttons.values():
            btn.draw(screen)

        # Déplacement continu de la caméra avec les flèches du clavier
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: cam.move(-cell_size,0)
        if keys[pygame.K_RIGHT]: cam.move(cell_size,0)
        if keys[pygame.K_UP]: cam.move(0,-cell_size)
        if keys[pygame.K_DOWN]: cam.move(0,cell_size)

        pygame.display.flip()  # Mettre à jour l'affichage

if __name__ == "__main__":
    game_loop()