"""
Gère les fichiers ressources
"""
import pyxel as px
from typing import Literal

MODELES: dict[str, dict[Literal["option_side", "side", "background", "res", "tc", "h-g", "h-d", "b-g", "b-d", "h", "b", "g", "d", "m"], Literal[8, 9, 10, 11, r"Ressources\pyxres\elements_b.pyxres"] | tuple[int, int]]] = {
           "simple": {"side": 10,"background": 9, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 0), "h-d": (8, 0), "b-g": (0, 8), "b-d": (8, 8), "h": (16, 0), "b": (24, 0), "g": (16, 8), "d": (24, 8), "m": (32, 0)},
           "simple inversé": {"side": 9,"background": 10, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 16), "h-d": (8, 16), "b-g": (0, 24), "b-d": (8, 24), "h": (16, 16), "b": (24, 16), "g": (16, 24), "d": (24, 24), "m": (32, 0)},
           "complet": {"option_side": 8, "side": 10,"background": 9, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 32), "h-d": (8, 32), "b-g": (0, 40), "b-d": (8, 40), "h": (16, 32), "b": (24, 32), "g": (16, 40), "d": (24, 40), "m": (32, 0)},
           "complet inversé": {"option_side": 8, "side": 10,"background": 9, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 48), "h-d": (8, 48), "b-g": (0, 56), "b-d": (8, 56), "h": (16, 48), "b": (24, 48), "g": (16, 56), "d": (24, 56), "m": (32, 0)}
           }

def init_ressources():
    global MODELES
    file_loaded = None
    for nom, elements in MODELES.items():
        element = {}
        for nom_cote, position in elements.items():

            if nom_cote not in ("cm", "tc", "res"):
                if file_loaded != elements["res"]:
                    px.load(elements["res"])
                    file_loaded = elements["res"]

                px.blt(0, 0, 0, position[0], position[1], elements["tc"], elements["tc"]) # pyright: ignore[reportArgumentType]

                liste_pos = dict[int, dict[int, int]]()
                for x in range(8):
                    liste_pos[x] = {}
                    for y in range(8):
                        if nom_cote != "m":
                            liste_pos[x][y] = px.pget(x, y)
                        else:
                            liste_pos[x][y] = elements["cm"] # pyright: ignore[reportArgumentType]
                element[nom_cote] = liste_pos.copy()

        element["couleurs"] = {"background": elements["cm"], "side": , "option_side"}
        MODELES[nom] = element.copy()