"""
Représente toutes les actions de base et les affichages des menu.
"""
import pyxel as px
from typing import Literal

FICHIER_RESSOURCES = "Ressources/pyxres/menus.pyxres"

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
    modele: `Literal`[`"simple"`, `"simple inversé"`, `"complet"`, `"complet inversé"`]
        Le modèle avec lequel la fenètre doit etre dessinée.
    texte: optionel[`str`]
        Le texte qui est écrit dans la fenètre.
    colone_txt: optionel[`Literal`[`"gauche"`, `"droite"`, `"millieu"`] | :class:`int`]
        Soit une position prédéfinie sur l'axe x soit un nombre de pixels à se décaller mais
        positif exclusivement.
    ligne_txt: optionel[`Literal`[`"haut"`, `"bas"`, `"millieu"`] | :class:`int`]
        Soit une position prédéfinie sur l'axe y soit un nombre de pixels à se décaller mais
        positif exclusivement.
    """
    def __init__(self, nom: str, x: int, y: int, width: int, height: int, modele: Literal["simple", "simple inversé", "complet", "complet inversé"] = "simple", texte: str | None = None, colone_txt: Literal["gauche", "droite", "millieu"] | int = "millieu", ligne_txt: Literal["haut", "bas", "millieu"] | int = "millieu"):
        assert width >= 2 and height >= 2, f"La taille du menu {nom} est trop petite."
        _EMPLACEMENTS = {"x": {"gauche": 8, "millieu": width * 4, "droite": (width - 1) * 8}, "y": {"haut": 8, "bas": (height - 1) * 8, "millieu": height * 4}}
        _MODELES = {"simple": {"h-g": (0, 0), "h-d": (1, 0), "b-g": (0, 1), "b-d": (1, 1), "h": (2, 0), "b": (3, 0), "g": (2, 1), "d": (3, 1), "m": (4, 0), "cm": 10},
                    "simple inversé": {"h-g": (0, 2), "h-d": (1, 2), "b-g": (0, 3), "b-d": (1, 3), "h": (2, 2), "b": (3, 2), "g": (2, 3), "d": (3, 3), "m": (4, 0), "cm": 9},
                    "complet": {"h-g": (0, 4), "h-d": (1, 4), "b-g": (0, 5), "b-d": (1, 5), "h": (2, 4), "b": (3, 4), "g": (2, 5), "d": (3, 5), "m": (4, 0), "cm": 9},
                    "complet inversé": {"h-g": (0, 6), "h-d": (1, 6), "b-g": (0, 7), "b-d": (1, 7), "h": (2, 6), "b": (3, 6), "g": (2, 7), "d": (3, 7), "m": (4, 0), "cm": 10}
                    }
        
        if texte != None:
            self.emplacement = []

            if type(colone_txt) == int:
                assert colone_txt >= 0, f"L'emplacement du texte du menu {nom} sur l'axe x est invalide." #type: ignore
                self.emplacement.append(colone_txt)
            else:
                self.emplacement.append(_EMPLACEMENTS["x"][colone_txt]) # type:ignore
            
            if type(ligne_txt) == int:
                assert ligne_txt >= 0, f"L'emplacement du texte du menu {nom} sur l'axe y est invalide." #type: ignore
                self.emplacement.append(ligne_txt)
            else:
                self.emplacement.append(_EMPLACEMENTS["y"][ligne_txt]) # type:ignore
            self.texte = texte
            
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.modele = _MODELES[modele].copy()
        menus[nom] = self

    def draw(self):
        '''
        La fonction qui dessine le menu.
        '''
        px.load(FICHIER_RESSOURCES)

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
                
                px.tilemaps[0].pset(x, y, self.modele[emp])

        px.pal(0, self.modele["cm"])

        px.bltm(self.x, self.y, 0, 0, 0, self.width * 8, self.height * 8)

        px.pal()

menus = dict[str, Fenetre]()

def draw_menus(*noms):
    if len(noms) == 0:
        print("Vous n'avez pas indiqué quels menus vous voulez afficher.")
    else:
        for nom in noms:
            menus[nom].draw()