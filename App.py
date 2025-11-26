import pyxel as px
from Ressources.py.manager import *

class Jeu:
    """
    Represente le jeu en général

    Parameters
    -----------
    width: :class:`int`
        La largeur de la fenètre de jeu.
    height: :class:`int`
        La hauteur de la fenètre de jeu.
    titre: :class:`str`
        Le titre du jeu et donc de la fenètre qd on lance le jeu.
    fps: :class:`int`
        Le nombre de frames par secondes c'est à dire le nombre de fois ou toutes
        les actions du jeu sont répétées chaque seconde.
    """
    def __init__(self, width: int, height: int, titre: str, fps = 30) -> None:
        
        # initialise la fenetre de jeu
        px.init(width, height, title= titre, fps= fps)

        init_ressources()

        Fenetre("test", 0, 0, 2, 2)
        Bouton("test", 0, 0, 3, 3, "complet", test)

        px.mouse(True)

        px.cls(background_color)

        elements_def(menus = ["test", "test1", "test2", "test3"], boutons = ["test", "test1", "test2"])

        # lance la fenetre de jeu
        px.run(self.update, draw)

    def update(self):
        """
        La fonction qui est répétée chaque frame du jeu pour mettre à jour les variables
        et gérer les différentes actions dans le jeu.
        """
        if px.btn(px.KEY_A):
            px.quit()

        elements_update()

def test():
    print("test")
    print()

def test2(mot:str):
    print(mot)
    print()

def test3(mot, repetitions):
    for _ in range(repetitions):
        print(mot)
    print()

Jeu(1024, 512, "test")