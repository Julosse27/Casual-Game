"""
Ce fichier est fait pour économiser des ressources lors de l'affichage des textures.
"""
import pyxel as px
from typing import Callable

element_a_d = {
                "Ressources/pyxres/elements_b.pyxres": list[Callable[[], None]]()
                
                }

_file_loaded = None

def load_draw(name:str, *functions):
    if name in ("Ressources.py.boutons", "Ressources.py.menus"):
        for function in functions:
            element_a_d["Ressources/pyxres/elements_b.pyxres"].append(function)
    
def draw():
    for file, fonctions in element_a_d.items():
        global _file_loaded
        if _file_loaded != file:
            px.load(file)
            _file_loaded = file
        for element in fonctions:
            element()