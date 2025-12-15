"""
Ce module gères les couleurs utilisées par le jeu.
"""
from pyxel import colors

def index_couleur(valeur_exa: str):
    """
    Cette fonction va ajouter la couleur demandée au module pyxel 
    et retourner son index. Ou retourner l'index de la couleur demandée si elle existe
    déjà

    Parameter
    ----------
    valeur_exa: :class:`str`
        Vous devez donner la valeur exadécimale en str sous la forme
        #FFFFFF (l'éditeur VScode pourra vous permettre de choisir directement
        les couleurs si vous ecrivez cela).
    """
    assert valeur_exa[0] == "#", "La déclaration d'une couleur doit démarer par #."
    assert len(valeur_exa) == 7, """La déclaration d'une couleur doit contenir # 
                                    plus 2 infos exadécimales pour chaque couleur primaire."""
    
    valeur_exa.replace("#", "0x")
    valeur_int_exa = int(valeur_exa, base= 0)
    color_palette = colors.to_list()

    for color in color_palette:
        if color == valeur_int_exa:
            return color_palette.index(valeur_int_exa)
     
    res = len(color_palette)
    color_palette.append(valeur_int_exa)
    return res