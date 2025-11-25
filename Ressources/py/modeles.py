"""
Gère les fichiers ressources
"""
import pyxel as px

MODELES: dict[str, dict[str, dict[int, dict[int, int]]]] = {"simple": {"cm": 10, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 0), "h-d": (8, 0), "b-g": (0, 8), "b-d": (8, 8), "h": (16, 0), "b": (24, 0), "g": (16, 8), "d": (24, 8), "m": (32, 0)},
           "simple inversé": {"cm": 9, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 16), "h-d": (8, 16), "b-g": (0, 24), "b-d": (8, 24), "h": (16, 16), "b": (24, 16), "g": (16, 24), "d": (24, 24), "m": (32, 0)},
           "complet": {"cm": 10, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 32), "h-d": (8, 32), "b-g": (0, 40), "b-d": (8, 40), "h": (16, 32), "b": (24, 32), "g": (16, 40), "d": (24, 40), "m": (32, 0)},
           "complet inversé": {"cm": 9, "res": r"Ressources\pyxres\elements_b.pyxres", "tc": 8, "h-g": (0, 48), "h-d": (8, 48), "b-g": (0, 56), "b-d": (8, 56), "h": (16, 48), "b": (24, 48), "g": (16, 56), "d": (24, 56), "m": (32, 0)}
           }  # pyright: ignore[reportAssignmentType]

def init_ressources():
    global MODELES
    file_loaded = None
    for nom, elements in MODELES.items():
        element = {}
        for nom_cote, position in elements.items():

            if nom_cote not in ("cm", "tc", "res"):
                if file_loaded != elements["res"]:
                    px.load(elements["res"]) # pyright: ignore[reportArgumentType]
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
        MODELES[nom] = element.copy()