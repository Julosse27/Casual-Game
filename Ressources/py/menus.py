"""
Représente toutes les actions et les affichages de base des menu aussi appelés fenètre.
"""
from typing import Literal, Callable
from Ressources.py.modeles import MODELES
from collections import defaultdict

class Fenetre:
    r"""
    Cette classe represente une fenetre dans son integralitée.
    Aussi appelé menu
    
    Parameters
    -------------
    nom: :class:`str`
        Le nom avec lequel cette fenetre est appelé et retrouvable.
    x: :class:`int`
        La coordonée x ou se trouve le début de ce menu.
    y: :class:`int`
        La coordonée y ou se trouve le début de ce menu.
    width: :class:`int`
        Le nombre de tuiles de largeurs que fera ce menu.

        /!\ Une tuile représente 8 pixels.
    height: :class:`int`
        Le nombre de tuiles de hauteur que fera ce menu.
    modele: optionel[`Literal`[`"simple"`, `"simple inversé"`, `"complet"`, `"complet inversé"`]]
        Le modèle avec lequel la fenètre doit etre dessinée.
    """
    def __init__(self, nom: str, x: int, y: int, width: int, height: int, modele_type: Literal["simple", "simple inversé", "complet", "complet inversé"] = "simple"):
        assert nom != "", "Le nom ne peut pas être vide."
        for noms in menus:
            assert nom != noms, f"Le menu {nom} existe déjà."
        assert width >= 2 and height >= 2, f"La taille du menu {nom} est trop petite."

        self.x = x
        self.y = y
        
        self.width = width
        self.height = height

        self.type = "menus"
        self.nom = nom    
        self.id = "0" + str(len(menus))

        self.change_modele: Callable

        modele = MODELES[modele_type].copy()
        self.color_map_1 = defaultdict[int, dict[int, tuple[int, str]]](lambda: {})
        for u in range(self.width):
            for v in range(self.height):
                modele_tile = modele[self.get_nom_cote(u, v)]
                for x, liste_y in modele_tile.items():
                    color_x = x + self.x + u * 8
                    liste_ex:dict[int, tuple[int, str]] = {}
                    for y, color in liste_y.items():
                        color_y = y + self.y + v * 8
                        liste_ex[color_y] = (color, self.id)
                    self.color_map_1[color_x].update(liste_ex)
        
        self.color_map_2 = defaultdict[int, dict[int, tuple[int, str]]](lambda: {})

        self.active_map = 1

        self.animation = False

        menus[nom] = self

    def get_nom_cote(self, u: int, v: int) -> Literal['h-g', 'b-g', 'g', 'h-d', 'b-d', 'd', 'h', 'b', 'm']:
        """
        Fonction qui donne la qualification d'un endroit du menu.
        
        Parameters
        ----------
        u: :class:`int`
            Dans quelle colone de tuile.
        v: :class:`int`
            Dans quelle ligne de tuile.
        """
        if u == 0:
            if v == 0:
                emp = "h-g"
            elif v == self.height - 1:
                emp = "b-g"
            else:
                emp = "g"
        elif u == self.width - 1:
            if v == 0:
                emp = "h-d"
            elif v == self.height - 1:
                emp = "b-d"
            else:
                emp = "d"
        elif v == 0:
            emp = "h"
        elif v == self.height - 1:
            emp = "b"
        else:
            emp = "m"

        return emp

    def draw(self):
        '''
        La fonction qui dessine le menu.
        '''
        pass

menus = dict[str | Literal["nom"], Fenetre](nom = "menus") # pyright: ignore[reportArgumentType]