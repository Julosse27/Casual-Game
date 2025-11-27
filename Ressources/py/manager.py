"""
Améliore le système de dessin pour améliorer les performances.
"""

import pyxel as px
from typing import Literal
from Ressources.py.menus import Fenetre, menus as _menus
from Ressources.py.boutons import Bouton, boutons as _boutons
from Ressources.py.modeles import init_ressources

pos_souris = (0, 0)

liste_elements = list[Fenetre | Bouton]()

draw_statut = False

background_color = 12

list_ressources: dict[str, dict[str, Bouton | Fenetre]] = {_menus["nom"]: _menus, _boutons["nom"]: _boutons}  # pyright: ignore[reportAssignmentType]

def change_modele(element: Fenetre | Bouton, nb_color_map: Literal[1, 2]):
    global color_map, draw_statut
    change = False
    for x, _ in color_map.items():
        color_map_el = element.color_map_1.copy() if nb_color_map == 1 else element.color_map_2.copy()
        try:
            for y_el, color in color_map_el[x].items():
                if color[1] == element.id:
                    color_map[x][y_el] = color
                    change = True
        except KeyError:
            pass
    if change:
        draw_statut = True
        element.active_map = nb_color_map
    else:
        print("Il n'y à aucun changement.")

def colormap_reset():
    global color_map, draw_statut
    color_map = dict[int, dict[int, tuple[int, str]]]()
    for element in liste_elements:
        for x in range(element.x, element.x + element.width * 8):
            try:
                color_map[x]
            except KeyError:
                color_map[x] = {}
            color_map_ex = {}
            for y, color in element.color_map_1[x].items():
                color_map_ex[y] = color
            color_map[x].update(color_map_ex)
    draw_statut = True

def get_element_colors(type_e: Literal["boutons", "menus"], nom: str):
    try:
        first_x = list_ressources[type_e][nom].x
        first_y = list_ressources[type_e][nom].y
        for x, liste_y in color_map.items():
            if x >= first_x and x < first_x + list_ressources[type_e][nom].width * 8:
                for y, color in liste_y.items():
                    if y >= first_y and y < first_y + list_ressources[type_e][nom].height * 8:  # pyright: ignore[reportOperatorIssue]
                        pass
    except KeyError:
        print(f"Le {type_e} de nom {nom} n'existe pas.")
         
def get_colormap(x: int, y: int) -> int:
    """
    Retourne la couleur du pixel demandé.

    Parameters
    -----------
    x: :class:`int`:
        La coordonnée x du pixel.
    y: :class:`int`:
        La coordonnée y du pixel.

    Return
    -------
    color: :class:`int`:
        La couleur de ce pixel selon l'actulle colormap.
    """
    try:
        res = color_map[x][y][0]
        return res
    except KeyError:
        return background_color

def elements_def(ordre: Literal["inverse", "normal"] | list[tuple[str, str]] = "normal", **elements_noms: list[str]) -> None:
    r"""
    Fonction qui va permettre de définir les element à prendre en compte au
    moment actuel du jeu.

    Parameters
    -----------
    ordre: optionel[ :class:`Literal`[`"inverse"`, `"normal"`] | :class:`tuple`[`tuple`[`str`, `str`]]]
        Ce paramètre assigne un ordre au éléments que l'on ajoute:
            - Soit l'on choisit entre le mode `"normal"` et `"inverse"` qui soit va prendre tout les éléments dans l'ordre ou ils
            ont été nommées soit dans l'ordre inverse.
            - Ou on définit un tuple de 2 informations capitales pour définir 1 a 1 l'ordre dans lequel ils vont étre ajoutés.   
            /!\ typographie spéciale dans les infos à spécifier !!
                - D'abord le type de l'élément (soit `boutons` ou `menus`).
                - Ensuite le nom de l'élément.
    **elements_noms: :class:`list[str]`
        /!\ Ce paramètre nécécite une typographie exacte: 
            - Premièrement le nom représente le type d'élément que l'on veut ajouter parmis eux: `boutons`, `menus`
            - Ce paramètre devra contenir une :class:`list[str]` puisque celle-ci contiendra les noms des éléments que tu veut ajouter.
    """
    print("-" * 20)
    print("Ajout des éléments")
    print("Si il y a des problèmes ils seront affichés avec des messages.")
    print("-" * 20)
    if len(elements_noms) == 0:
        print("Spécifiez quels éléments vous voulez ajouter.")
        return
    type_supp = []
    nom_supp = []
    for type_e, noms in elements_noms.items():
        if type_e not in ("boutons", "menus"):
            print(f"Le type {type_e} n'existe apparement pas, les éléments spécifiés ne seront pas ajoutés.")
            type_supp.append(type_e)
            print("---")
        else:
            if len(nom_supp) != 0:
                print("---")
            for nom in noms:
                try:
                    list_ressources[type_e][nom]
                except KeyError:
                    print(f"Le {type_e} {nom} n'existe pas il ne sera donc pas ajouté.")
                    nom_supp.append((type_e, nom))
                
    if ordre not in ("normal", "inverse"):
        test_len = 0
        for _, z in elements_noms.items():
            test_len += len(z)
        if len(ordre) == test_len:
            print("L'ordre et les noms spécifiées doivent correspondre.")
            return
        
    global liste_elements
    liste_elements = list[Fenetre | Bouton]()
        
    for supp in type_supp:
        if ordre not in ("inverse", "normal"):
            for nom_type, x in ordre:
                if nom_type == supp:
                    ordre.remove((nom_type, x))  # pyright: ignore[reportAttributeAccessIssue]
        elements_noms.pop(supp)

    for type_s, nom in nom_supp:
        if ordre not in ("inverse", "normal"):
            ordre.remove((type_s, nom))  # pyright: ignore[reportAttributeAccessIssue]
        elements_noms[type_s].remove(nom)


    if ordre in ("inverse", "normal"):
        for type_e, noms in elements_noms.items():
            ressource = list_ressources[type_e]
            for nom in noms:
                ressource[nom].change_modele = change_modele
                if ordre == "inverse":
                    liste_elements.insert(0, ressource[nom])
                elif ordre == "normal":
                    liste_elements.append(ressource[nom])
            continue
    else:
        for type_e, nom in ordre:
            ressource = list_ressources[type_e]
            liste_elements.append(ressource[nom])
            continue
    
    colormap_reset()

def elements_update():
    for element in liste_elements:
        if type(element) == Bouton:
            element.update()

def draw():
    global pos_souris, draw_statut
    # Définit le font_d'écran
    for x in range(pos_souris[0], pos_souris[0] + 8):
        for y in range(pos_souris[1], pos_souris[1] + 8):
            if x >= 0 and x <= px.width and y >= 0 and y <= px.height:
                couleur = get_colormap(x, y)
                px.pset(x, y, couleur)

    if draw_statut:
        px.cls(background_color)
        for x, liste_y in color_map.items():
            for y, color in liste_y.items():
                if type(y) == int:
                    px.pset(x, y, color[0])
        draw_statut = False

    pos_souris = (
                px.mouse_x,
                px.mouse_y
                  )
