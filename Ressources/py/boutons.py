"""
Représente tout les boutons pour des interactions de base.
"""
import pyxel as px
from typing import Literal, Callable

FICHIER_RESSOURCES = "Ressources/pyxres/elements_b.pyxres"

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
    modele: `Literal`[`"simple"`, `"complet"`]
        Le modèle avec lequel le bouton doit etre dessinée.
    action: `fonction retourne none`
        L'action que ce bouton déclenche.
    parametres_action: nb_variable_args[`tout type`]
        Paramètres de l'action si il y en a.
    animation: optionel[`Literal`[`"simple"`, `"inversé"`]]
        Le type d'animation lorsque la souris passe sur le bouton.
    """
    def __init__(self, nom: str, x: int, y: int, width: int, height: int, modele: Literal["simple", "complet"], action: Callable, *parametres_action, animation: Literal["inversé", "simple"] = "simple") -> None:
        for noms in boutons:
            assert nom != noms, f"Le bouton {nom} existe déjà."        
        assert width >= 2 and height >= 2, f"La taille du bouton {nom} est trop petite."
        
        self.MODELES = {
            "simple": ( {"h-g": (0, 0), "h-d": (1, 0), "b-g": (0, 1), "b-d": (1, 1), "h": (2, 0), "b": (3, 0), "g": (2, 1), "d": (3, 1), "m": (4, 0), "cm": 10}, 
                        {"h-g": (0, 2), "h-d": (1, 2), "b-g": (0, 3), "b-d": (1, 3), "h": (2, 2), "b": (3, 2), "g": (2, 3), "d": (3, 3), "m": (4, 0), "cm": 9}),
            "complet": ({"h-g": (0, 4), "h-d": (1, 4), "b-g": (0, 5), "b-d": (1, 5), "h": (2, 4), "b": (3, 4), "g": (2, 5), "d": (3, 5), "m": (4, 0), "cm": 9},
                        {"h-g": (0, 6), "h-d": (1, 6), "b-g": (0, 7), "b-d": (1, 7), "h": (2, 6), "b": (3, 6), "g": (2, 7), "d": (3, 7), "m": (4, 0), "cm": 10})
            }
        
        self.action = action
        self.parametres = parametres_action

        self.nom = nom

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self._TYPES_ANIMS = (0, 1)
        self.type_animation = 0 if animation == "simple" else 1
        self.change_modele(modele)
        self.animation = False
        boutons[nom] = self
        print(boutons)

    def change_modele(self, nouveau_modele: Literal["simple", "complet"]):
        self.modele_actif = nouveau_modele

    def draw(self):
        """
        La fonction qui dessine le bouton.
        """

        if not (self.animation and px.frame_count % 30 < 15):
            anim = self.type_animation
        else:
            anim = self._TYPES_ANIMS[self._TYPES_ANIMS.index(self.type_animation) - 1]
        
        for x in range(self.width):
            for y in range(self.height):
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
                
                px.tilemaps[0].pset(x, y, self.MODELES[self.modele_actif][anim][emp])    
        
        px.pal(0, self.MODELES[self.modele_actif][anim]["cm"])

        px.bltm(self.x, self.y, 0, 0, 0, self.width * 8, self.height * 8)

        px.pal()

    def update(self):
        """
        La fonction qui met à jour les action et les variables du bouton.
        """
        # vérifie si la souris est sur le même axe x et y que le bouton.
        if (px.mouse_x >= self.x and px.mouse_x < self.x + self.width * 8) and (px.mouse_y >= self.y and px.mouse_y < self.y + self.height * 8):
            self.animation = True
            if px.btnp(px.MOUSE_BUTTON_LEFT):
                self.action(*self.parametres)
        else:
            self.animation = False
        
boutons = dict[str, Bouton]()
            