"""
Ce module représente tout les textes qui peuvent apparaitre dans ce jeu.
"""
import pyxel as px
from typing import Literal

class Texte:
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
    texte: :class:`str`
        Le texte qui doit être affiché avec cet objet
    couleur: optionel[:class:`int`]:
        Soit une couleur parmis celles dans la liste pyxel soit
        la valeur exadécimale sous la forme 0xFFFFFF d'une nouvelle couleur.
    """
    def __init__(self, nom: str, x: int, y: int, texte: str, couleur: int = 7) -> None:
        assert nom != "", "Le nom ne peut pas être vide."
        assert texte != "", "Veuilez spécifier le texte de cet objet."
        for noms in textes:
            assert nom != noms, f"Le bouton {nom} existe déjà."
        
        


textes = dict[str, list[Texte]](nom = "textes", ressources = "Ressources/pyxres/elements_b.pyxres") # pyright: ignore[reportArgumentType]