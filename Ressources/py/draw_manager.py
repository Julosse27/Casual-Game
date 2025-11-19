"""
Améliore le système de dessin pour améliorer les performances.
"""

import pyxel as px
from typing import Literal
from Ressources.py.menus import Fenetre, menus as _menus
from Ressources.py.boutons import Bouton, boutons as _boutons

pos_souris = (0, 0)

_file_loaded = None

liste_draw = list[Fenetre | Bouton]()

_liste_draw_chek = list[Literal["dessine", "non_dessine", "a_supp"]]()

_liste_draw_ressources = []

_list_ressources = (_menus, _boutons)

def ajout_draw(type_e: Literal["menus", "boutons"], *noms: str, calque: int | list[int] = -1):
    if type(calque) == list:
        assert len(noms) == len(calque)
    for ressources in _list_ressources:
        if ressources["nom"] == type_e:
            for nom in noms:
                try:
                    liste_draw.insert(calque if type(calque) == int else calque[noms.index(nom)], ressources[nom]) # type:ignore
                    _liste_draw_chek.insert(calque if type(calque) == int else calque[noms.index(nom)], "non_dessine") # type:ignore
                    _liste_draw_ressources.insert(calque if type(calque) == int else calque[noms.index(nom)], ressources["ressource"]) # type:ignore
                except KeyError:
                    print(f"Le {type_e[:-1]} appelé {nom} ne peut pas être affiché.")
            break

def stop_draw(type: Literal["menus", "boutons"], *noms):
    for ressources in _list_ressources:
        if ressources["nom"] == type:
            for nom in noms:
                try:
                    index = liste_draw.index(ressources[nom])
                    _liste_draw_chek[index] = "a_supp"
                except KeyError:
                    print(f"Le {type[:-1]} appelé {nom} n'est pas disponible.")
                except ValueError:
                    print(f"Le {type[:-1]} appelé {nom} n'est pas dans la liste a dessiner.")
            break

def draw():
    global pos_souris
    # Définit le font_d'écran
    if px.frame_count == 0:
        px.cls(12)
    else:
        px.rect(pos_souris[0], pos_souris[1], 8, 8, 12)

    global _file_loaded
    a_supp = []
    for i in range(len(_liste_draw_chek)):
        if _liste_draw_chek[i] == "a_supp":
            px.rect(liste_draw[i].x, liste_draw[i].y, liste_draw[i].width * 8, liste_draw[i].height * 8, 12)
            a_supp.append(i)
        elif (pos_souris[0] + 8 >= liste_draw[i].x and pos_souris[0] < (liste_draw[i].x + liste_draw[i].width * 8)) and (pos_souris[1] + 8 >= liste_draw[i].y and pos_souris[1] < (liste_draw[i].y + liste_draw[i].height * 8)):
            _liste_draw_chek[i] = "non_dessine"
        
        if _liste_draw_chek[i] == "non_dessine":
            if _file_loaded != _liste_draw_ressources[i]:
                px.load(_liste_draw_ressources[i])
                _file_loaded = _liste_draw_ressources[i]
            liste_draw[i].draw()
            _liste_draw_chek[i] = "dessine"

    for pop in a_supp:
        _liste_draw_chek.pop(pop)
        liste_draw.pop(pop)
        _liste_draw_ressources.pop(pop)

    # Enregistre la position de la souris pour la cacher
    # dans la prochaine frame
    pos_souris = (px.mouse_x, px.mouse_y)