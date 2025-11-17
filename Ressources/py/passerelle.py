"""
Ce module fait la passerelle entre les fichiers pythons des ressources et
le jeu en général.
"""
import pyxel as px
from typing import Callable, Literal
from Ressources.py.boutons import boutons, Bouton
from Ressources.py.menus import menus, Fenetre

_REFERENCE = {"boutons": (boutons, "Ressources/pyxres/elements_b.pyxres"),
              "menus": (menus, "Ressources/pyxres/elements_b.pyxres")
              }

element_a_draw = {
                "Ressources/pyxres/elements_b.pyxres": list[Callable[[], None]]()
                
                }

_file_loaded = None

def load_draw(type: Literal["boutons", "menus"], *noms):
    if len(noms) == 0:
        print(f"Vous n'avez pas spécifié quels {type} vous voulez afficher.")
    else:
        for nom in noms:
            try:
                element_a_draw[_REFERENCE[type][1]].append(_REFERENCE[type][0][nom].draw)
            except KeyError as e:
                print(f"Le {type} {nom} n'est pas accessible pour son affichage.")
    
def update(type: Literal["boutons"], *noms):
    if len(noms) == 0:
        print(f"Vous n'avez pas spécifié quels {type} vous voulez mettre à jour.")
    else:
        for nom in noms:
            try:
                _REFERENCE[type][0][nom].update()
            except KeyError as e:
                print(f"Le {type} {nom} n'est pas accessible pour sa mise à jour.")

def draw():
    global element_a_draw
    for file, fonctions in element_a_draw.items():
        global _file_loaded
        if _file_loaded != file:
            px.load(file)
            _file_loaded = file
        for element in fonctions:
            element()
        element_a_draw[file] = list[Callable[[], None]]()