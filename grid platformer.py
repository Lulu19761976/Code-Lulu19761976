WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 0.5
PLAYER_MAX_SPEED = 10

TILE_SIZE = 40  # Taille d'une case en pixels

BLOCK_MAP = {
    0: None,             # Vide
    1: "herbe",         # Normal (vert)
    2: "glace",         # Normal (vert)
    3: "lave",          # Glace (bleu clair)
    7: "rebond",          # Rebond (à implémenter)
}

BLOCK_TYPES = {
  'herbe': {
    'slowing_speed': 0.5,
    'color': (0, 255, 0),
    'jump_multiplier': 1,
    'speed_multiplier': 1,
  },
  "rebond":{
    'slowing_speed': 0.5,
    'color': (255, 165, 0),
    'jump_multiplier': 1.5,
    'speed_multiplier': 1,
  },
  "glace":{
    'slowing_speed': 0.2,
    'color': (0, 165, 255),
    'jump_multiplier': 1,
    'speed_multiplier': 2,
  },
  "lave":{
    'slowing_speed': 1,
    'color': (255, 0, 0),
    'jump_multiplier': 0,
    'speed_multiplier': 0.2,
  }
}

import pygame
import sys
import json
class Game:
    def __init__(self):
        # Initialise Pygame et crée la fenêtre du jeu
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Fenêtre principale
        pygame.display.set_caption("Grid Platformer")
        self.clock = pygame.time.Clock()                        # Pour gérer le temps et le FPS

        # Attributs de la caméra
        self.camera_offset = [0, 0]
        self.camera_smooth = 1  # Facteur de lissage (0-1), plus bas = plus lent

        # Chargement du niveau depuis le fichier JSON
        self.load_level("C:\Projets\Tutorat\LearnPygame\Partie 10 Grid Platformer\level.json")
        
        # Création du joueur (objet Player)
        self.player = Player(100, 100, 30, 50)
        self.running = True  # Contrôle la boucle principale du jeu

    def load_level(self, filename):
        # Charge le niveau depuis un fichier JSON
        try:
            print(f"Chargement du niveau depuis {filename}...")
            with open(filename, 'r') as file:
                self.grid = json.load(file)
            print("Niveau chargé avec succès.")
            # Création des plateformes à partir de la grille
            self.platforms = []
            
            # Parcourt chaque cellule de la grille
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    print(f"Cellule ({x}, {y}): {cell}")  # Affiche la valeur de la cellule
                    # Si la cellule n'est pas vide (différente de 0)
                    if cell != 0 and cell in BLOCK_MAP and BLOCK_MAP[cell] is not None:
                        # Crée une plateforme de la taille d'une case
                    
                        block_type = BLOCK_MAP[cell]
                        
                        block_object = BLOCK_TYPES.get(block_type)
                        
                        if(block_object is None):
                            print(f"Type de bloc inconnu: {block_type}")
                            continue
                        
                        print(f"Type de bloc: {block_type}, Propriétés: {block_object}")  # Affiche le type de bloc et ses propriétés
                        platform = Platform(
                            x * TILE_SIZE,           # Position X
                            y * TILE_SIZE,           # Position Y
                            TILE_SIZE,               # Largeur
                            TILE_SIZE,               # Hauteur
                            block_object          # Type de bloc
                        )
                        self.platforms.append(platform)
                        
        except FileNotFoundError:
            print(f"Erreur: Le fichier {filename} n'a pas été trouvé.")
            # Niveau par défaut si le fichier n'est pas trouvé
            self.platforms = [
                Platform(0, HEIGHT - 40, WIDTH, 40)  # Sol par défaut
            ]
            
    def update_camera(self):
        # Calcule le centre du joueur
        target_x = self.player.rect.centerx - WIDTH // 2
        target_y = self.player.rect.centery - HEIGHT // 2
        
        # Applique un lissage à la caméra pour des mouvements plus fluides
        self.camera_offset[0] += (target_x - self.camera_offset[0]) * self.camera_smooth
        self.camera_offset[1] += (target_y - self.camera_offset[1]) * self.camera_smooth
        
        # Convertit les offsets en entiers pour éviter des problèmes d'affichage
        self.camera_offset[0] = int(self.camera_offset[0])
        self.camera_offset[1] = int(self.camera_offset[1])

    def apply_camera(self, rect):
        # Retourne un nouveau rectangle avec l'offset de la caméra appliqué
        return pygame.Rect(
            rect.x - self.camera_offset[0],
            rect.y - self.camera_offset[1],
            rect.width,
            rect.height
        )
    
    def run(self):
        # Boucle principale du jeu
        while self.running:
            self.handle_events()  # Gère les entrées clavier et la fermeture de la fenêtre
            keys = pygame.key.get_pressed()  # Récupère l'état de toutes les touches du clavier
            self.player.update(self.platforms, keys)  # Met à jour le joueur
            self.update_camera()  # Met à jour la position de la caméra
            self.draw()  # Affiche tous les éléments à l'écran
            self.clock.tick(FPS)  # Limite la vitesse du jeu à FPS images/seconde

    def handle_events(self):
        # Gère tous les événements (clavier, souris, fermeture, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Si l'utilisateur ferme la fenêtre, on arrête le jeu proprement
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Si une touche est pressée
                if event.key == pygame.K_ESCAPE:
                    # Si la touche Échap est pressée, on quitte le jeu
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    self.player.jump()  # Le joueur tente de sauter

    def draw(self):
        # Dessine le fond, les plateformes et le joueur
        self.screen.fill((135, 206, 235))  # Remplit l'écran avec une couleur bleu ciel
        
        for plat in self.platforms:
            # Dessine chaque plateforme avec l'offset de la caméra
            camera_rect = self.apply_camera(plat.rect)
            # Vérifie si la plateforme est visible à l'écran avant de la dessiner
            if (camera_rect.right > 0 and camera_rect.left < WIDTH and 
                camera_rect.bottom > 0 and camera_rect.top < HEIGHT):
                pygame.draw.rect(self.screen, plat.properties.get('color'), camera_rect)
        
        # Dessine le joueur avec l'offset de la caméra
        player_camera_rect = self.apply_camera(self.player.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), player_camera_rect)
        
        pygame.display.flip()  # Met à jour l'affichage à l'écran

[
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [2, 2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]
]
import pygame

class Platform:
    def __init__(self, x, y, w, h, properties):
        # On crée un rectangle Pygame pour représenter la plateforme
        self.rect = pygame.Rect(x, y, w, h)
        self.type = type
        
        # Différentes propriétés selon le type
        self.properties = properties
        print(self.properties)


class Player:
    def __init__(self, x, y, w, h):
        # Création du rectangle qui représente le joueur (position et taille)
        self.rect = pygame.Rect(x, y, w, h)
        self.vel_y = 0           # Vitesse verticale du joueur (pour la gravité et le saut)
        self.vel_x = 0           # Vitesse horizontale du joueur (pour les déplacements)
        self.on_ground = False   # Indique si le joueur touche une plateforme ou le sol
        self.slowing_speed = 2
        self.jump_multiplier = 1  # Multiplieur de saut, utilisé pour les plateformes spéciales
        self.speed_multiplier = 1  # Multiplieur de vitesse, utilisé pour les plateformes spéciales

    def handle_input(self, keys):
        # Gestion des déplacements horizontaux avec les touches fléchées
        if keys[pygame.K_LEFT]:
            if(self.vel_x > 0):
                self.vel_x = 0
            
            self.vel_x -= PLAYER_SPEED  # Déplacement vers la gauche
        elif keys[pygame.K_RIGHT]:
            if(self.vel_x < 0):
                self.vel_x = 0
            
            self.vel_x += PLAYER_SPEED  # Déplacement vers la droite
        elif(self.vel_x != 0):
          if(self.vel_x > 0):
            self.vel_x -= self.slowing_speed  # Ralentit le joueur s'il ne bouge pas
            if(self.vel_x < 0):
                self.vel_x = 0
          elif(self.vel_x < 0):
            self.vel_x += self.slowing_speed
            if(self.vel_x > 0):
                self.vel_x = 0
            
        # Limite la vitesse horizontale pour éviter de dépasser une certaine valeur
        if self.vel_x > PLAYER_MAX_SPEED * self.speed_multiplier:
            self.vel_x = PLAYER_MAX_SPEED * self.speed_multiplier  # Applique le multiplicateur de vitesse
        elif self.vel_x < -PLAYER_MAX_SPEED * self.speed_multiplier:
            self.vel_x = -PLAYER_MAX_SPEED * self.speed_multiplier  # Applique le multiplicateur de vitesse
            
        self.rect.x += int(self.vel_x)  # Applique le déplacement horizontal au rectangle du joueur

    def jump(self):
        # Permet au joueur de sauter uniquement s'il est sur le sol
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH * self.jump_multiplier  # Applique une vitesse verticale négative (vers le haut)

    def apply_gravity(self):
        # Applique la gravité à la vitesse verticale du joueur
        self.vel_y += GRAVITY
        # Déplace le joueur verticalement selon sa vitesse
        self.rect.y += int(self.vel_y)

    def check_collision(self, platforms):
        # Crée un petit rectangle sous le joueur pour détecter s'il touche une plateforme
        foot_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, 5)
        self.on_ground = False  # On suppose d'abord que le joueur n'est pas sur le sol

        # On vérifie si le "pied" du joueur touche une des plateformes
        for plat in platforms:
            # Collision seulement si le joueur tombe (vel_y >= 0)
            if foot_rect.colliderect(plat.rect) and self.vel_y >= 0:
                self.rect.bottom = plat.rect.top  # Place le joueur juste au-dessus de la plateforme
                self.vel_y = 0                   # Annule la vitesse verticale (arrête la chute)
                self.on_ground = True            # Le joueur est maintenant sur le sol
                
                # Si c'est un bloc rebond, le joueur rebondit automatiquement
                self.jump_multiplier = plat.properties.get('jump_multiplier', 1)
                self.slowing_speed = plat.properties.get('slowing_speed', 1)
                self.speed_multiplier = plat.properties.get('speed_multiplier', 1)
                print(f"Collision avec la plateforme: {plat.properties}")
                
        if(not self.on_ground):
            self.slowing_speed = 0.3

    def update(self, platforms, keys):
        # Met à jour l'état du joueur à chaque frame
        self.handle_input(keys)           # Déplacement gauche/droite
        self.apply_gravity()              # Applique la gravité
        self.check_collision(platforms)   # Vérifie les collisions avec les plateformes

    def draw(self, surface, camera_offset=None):
        if camera_offset:
            # Dessine le joueur avec l'offset de la caméra
            rect = pygame.Rect(
                self.rect.x - camera_offset[0],
                self.rect.y - camera_offset[1],
                self.rect.width,
                self.rect.height
            )
            pygame.draw.rect(surface, (255, 0, 0), rect)
        else:
            # Dessine normalement si pas d'offset de caméra
            pygame.draw.rect(surface, (255, 0, 0), self.rect)

if __name__ == "__main__":
    game = Game()
    game.run()