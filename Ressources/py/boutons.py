"""
Représente tout les boutons pour des interactions de base.
"""
import pyxel as px
from typing import Literal, Callable
from Ressources.py.modeles import MODELES
from Ressources.py.couleurs import index_couleur
from collections import defaultdict

class Bouton:
    r"""
    Représente un bouton dans son integralitée de son animation à son action.
    
    Parameters
    ------------
    nom: :class:`str`
        Le nom avec lequel ce bouton est appelé et retrouvable.
    x: :class:`int`
        La coordonée x ou se trouve le début de ce bonton.
    y: :class:`int`
        La coordonée y ou se trouve le début de ce bouton.
    width: :class:`int`
        Le nombre de tuiles de largeurs que fera ce bouton.
        /!\ Une tuile représente 8 pixels.
    height: :class:`int`
        Le nombre de tuiles de hauteur que fera ce bouton.
    action: `fonction retourne none`
        L'action que ce bouton déclenche.
    parametres_action: nb_variable_args[`tout type`]
        Paramètres de l'action si il y en a.
    animation_inversee: optionel[:class:`bool`]
        Si l'animation doit être inversée, par défaut `False`.
    modele: optionel[`Literal`[`"simple"`, `"complet"`]]
        Le modèle avec lequel le bouton doit etre dessinée.
    couleurs_spé: nb_variable_d'arguments[:class:`str`]
        Ce paramètre permet de changer les couleurs du bouton:
            - background = La couleur du fond
            - side = la couleur du coté du bouton
            - option_side = la couleur secondaire du coté du bouton
    """
    def __init__(self, nom: str, x: int, y: int, width: int, height: int, action: Callable, *parametres_action, animation_inversee: bool = False, modele_type: Literal["simple", "complet"] = "simple", **couleur_spé: str) -> None:
        assert nom != "", "Le nom ne peut pas être vide."
        for noms in boutons:
            assert nom != noms, f"Le bouton {nom} existe déjà."        
        assert width >= 2 and height >= 2, f"La taille du bouton {nom} est trop petite."
        
        self._MODELES = {
            "simple": "simple inversé",
            "complet": "complet inversé"
            }
        
        self.action = action
        self.parametres = parametres_action

        self.type = "bouton"
        self.nom = nom
        self.id = "1" + str(len(boutons))

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        modele = MODELES[self._MODELES[modele_type] if animation_inversee else modele_type]
        modele_anim = MODELES[self._MODELES[modele_type] if not animation_inversee else modele_type]

        self.color_map_1 = self.setup_colormaps(modele)
        
        self.color_map_2 = self.setup_colormaps(modele_anim)

        self.active_map = 1
        
        self.change_modele: Callable[[Bouton, Literal[1, 2]], None]
        self.animation = False
        self.focus_timer = -1
        boutons[nom] = self

    def setup_colormaps(self, modele: dict[str, dict[int, dict[int, int]]]) -> defaultdict[int, dict[int, tuple[int, str]]]:
        r"""
        Retourne la colormap en fonction du modèle donné.

        Parameters
        -----------
        modele: :class:`dict`[:class:`str`, :class:`dict`[:class:`int`, :class:`dict`[:class:`int`, :class:`int`]]]:
            Le modèle des couleurs.
        """
        variable = defaultdict[int, dict[int, tuple[int, str]]](lambda: {})

        for u in range(self.width):
            for v in range(self.height):
                modele_tile = modele[self.get_nom_cote(u, v)]
                for x, liste_y in modele_tile.items():
                    color_x = x + self.x + u * 8
                    liste_ex: dict[int, tuple[int, str]] = {}
                    for y, color in liste_y.items():
                        color_y = y + self.y + v * 8
                        liste_ex[color_y] = (color, self.id)
                    variable[color_x].update(liste_ex)
        
        return variable

    def get_nom_cote(self, x: int, y: int):
        """
        Fonction qui donne la qualification d'un endroit du bouton.
        
        Parameters
        ----------
        x: :class:`int`
            Dans quelle colone de tuile.
        y: :class:`int`
            Dans quelle ligne de tuile.
        """
        if x == 0:
            if y == 0:
                emp = "h-g"
            elif y == self.height - 1:
                emp = "b-g"
            else:
                emp = "g"
        elif x == self.width - 1:
            if y == 0:
                emp = "h-d"
            elif y == self.height - 1:
                emp = "b-d"
            else:
                emp = "d"
        elif y == 0:
            emp = "h"
        elif y == self.height - 1:
            emp = "b"
        else:
            emp = "m"

        return emp

    def update(self):
        """
        La fonction qui met à jour les action et les variables du bouton.
        """
        # vérifie si la souris est sur le même axe x et y que le bouton.
        self.animation = False
        if (px.mouse_x >= self.x and px.mouse_x < self.x + self.width * 8) and (px.mouse_y >= self.y and px.mouse_y < self.y + self.height * 8):
            self.focus_timer += 1
            if self.focus_timer % 15 == 0:
                self.change_modele(self, 2 if self.active_map == 1 else 1)
            if px.btnp(px.MOUSE_BUTTON_LEFT):
                self.action(*self.parametres)
        else:
            if self.focus_timer != -1:
                self.change_modele(self, 1)
                self.focus_timer = -1
        
boutons = dict[str | Literal["nom"], Bouton](nom = "boutons")  # pyright: ignore[reportArgumentType]