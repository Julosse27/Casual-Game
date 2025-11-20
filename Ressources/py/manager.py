"""
Améliore le système de dessin pour améliorer les performances.
"""

import pyxel as px
from typing import Literal
from Ressources.py.menus import Fenetre, menus as _menus
from Ressources.py.boutons import Bouton, boutons as _boutons

pos_souris = (0, 0)

tilemap: list[list[int]] = []

_file_loaded = None

liste_elements = list[Fenetre | Bouton]()

_liste_draw_chek = list[Literal["dessine", "non_dessine", "a_supp"]]()

_liste_draw_ressources = []

list_ressources = (_menus, _boutons)

def def_elements(ordre: Literal["inverse", "normal"] | list[tuple[str, str]] = "normal", **elements_noms: list[str]) -> None:
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
                    for ressource in list_ressources:
                        if ressource["nom"] == type_e:
                            ressource[nom]
                            break
                except ValueError:
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
            for ressource in list_ressources:
                if ressource["nom"] == type_e:
                    for nom in noms:
                        if ordre == "inverse":
                            liste_elements.insert(0, ressource[nom])
                        elif ordre == "normal":
                            liste_elements.append(ressource[nom])
                        _liste_draw_chek.append("non_dessine")
                        _liste_draw_ressources.append(ressource["ressource"])
                    continue
    else:
        for type_e, nom in ordre:
            for ressource in list_ressources:
                if ressource["nom"] == type_e:
                    liste_elements.append(ressource[nom])
                    _liste_draw_chek.append("non_dessine")
                    _liste_draw_ressources.append(ressource["ressource"])
                    continue

def elements_update():
    for element in liste_elements:
        if element.type == "bouton":
            element.update() # type:ignore

def stop_draw(type: Literal["menus", "boutons"], *noms):
    for ressources in list_ressources:
        if ressources["nom"] == type:
            for nom in noms:
                try:
                    index = liste_elements.index(ressources[nom])
                    _liste_draw_chek[index] = "a_supp"
                except KeyError:
                    print(f"Le {type[:-1]} appelé {nom} n'est pas disponible.")
                except ValueError:
                    print(f"Le {type[:-1]} appelé {nom} n'est pas dans la liste a dessiner.")
            break

def draw():
    global pos_souris, tilemap, _file_loaded
    # Définit le font_d'écran
    if px.frame_count == 0:
        px.cls(12)
    else:
        for x in range(pos_souris[0], pos_souris[0] + 8):
            for y in range(pos_souris[1], pos_souris[1] + 8):
                if not (x > px.width or y > px.height):
                    couleur = tilemap[x][y]
                    px.pset(x, y, couleur)

    a_supp = []
    for i in range(len(_liste_draw_chek)):
        if _liste_draw_chek[i] == "a_supp":
            px.rect(liste_elements[i].x, liste_elements[i].y, liste_elements[i].width * 8, liste_elements[i].height * 8, 12)
            a_supp.append(i)
        
        if _liste_draw_chek[i] == "non_dessine" or liste_elements[i].animation:
            if _file_loaded != _liste_draw_ressources[i]:
                px.load(_liste_draw_ressources[i])
                _file_loaded = _liste_draw_ressources[i]
            liste_elements[i].draw()
            tilemap = []
            for x in range(px.width + 1):
                tilemap.append([])
                for y in range(px.height + 1):
                    tilemap[x].append(px.pget(x, y))
                    
            _liste_draw_chek[i] = "dessine"

    for pop in a_supp:
        _liste_draw_chek.pop(pop)
        liste_elements.pop(pop)
        _liste_draw_ressources.pop(pop)

    # Enregistre la position de la souris pour la cacher
    # dans la prochaine frame
    pos_souris = (
                0 if px.mouse_x < 0 else px.width if px.mouse_x > px.width else px.mouse_x, 
                0 if px.mouse_y < 0 else px.height if px.mouse_y > px.height else px.mouse_y
                  )
