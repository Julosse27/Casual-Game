import pyxel as px
from Ressources.py.draw_manager import *
import Ressources.py.passerelle as passerelle

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

        Fenetre("test", 0, 0, 2, 2, "simple")
        Fenetre("test1", 16, 0, 2, 2, "simple inversé")
        Fenetre("test2", 0, 16, 2, 2, "complet")
        Fenetre("test3", 16, 16, 2, 2, "complet inversé")
        Bouton("test", 32, 0, 2, 2, "simple", test)
        Bouton("test1", 32, 16, 2, 2, "complet", test2, "test2")
        Bouton("test2", 48, 0, 2, 2, "complet", test3, "mot", 2, animation= "inversé")

        px.mouse(True)

        # lance la fenetre de jeu
        px.run(self.update, draw)

    def update(self):
        """
        La fonction qui est répétée chaque frame du jeu pour mettre à jour les variables
        et gérer les différentes actions dans le jeu.
        """
        passerelle.update("boutons", "test", "test1", "test2")
        if px.btn(px.KEY_A):
            px.quit()
        if px.frame_count == 0:
            ajout_draw("boutons", "test", "test1", "test2")
            ajout_draw("menus", "test", "test1", "test2", "test3")

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

Jeu(100, 100, "test")