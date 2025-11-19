"""
Améliore le système de dessin pour améliorer les performances.
"""

import pyxel as px
from typing import Literal
from Ressources.py.menus import Fenetre, menus as _menus
from Ressources.py.boutons import Bouton, boutons as _boutons

pos_souris = (0, 0)

liste_draw = list[Fenetre | Bouton]()

_liste_draw_chek = list[Literal["dessine", "non_dessine", "a_supp"]]()

_list_ressources = (_menus, _boutons)

def ajout_draw(type: Literal["menus", "boutons"], *noms):
    for ressources in _list_ressources:
        if ressources["nom"] == type:
            for nom in noms:
                try:
                    liste_draw.append(ressources[nom])
                    _liste_draw_chek.append("non_dessine")
                except KeyError:
                    print(f"Le {type[:-1]} appelé {nom} ne peut pas être affiché.")
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

    global _liste_draw_chek, liste_draw
    a_supp = []
    for i in range(len(_liste_draw_chek)):
        if _liste_draw_chek[i] == "a_supp":
            px.rect(liste_draw[i].x, liste_draw[i].y, liste_draw[i].width * 8, liste_draw[i].height * 8, 12)
            a_supp.append(i)
        elif _liste_draw_chek[i] == "non_dessine":
            liste_draw[i].draw()
            _liste_draw_chek[i] = "dessine"

    # Enregistre la position de la souris pour la cacher
    # dans la prochaine frame
    pos_souris = (px.mouse_x, px.mouse_y)