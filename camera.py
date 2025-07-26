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