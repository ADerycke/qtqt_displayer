# displayer/__init__.py

"""
QTQt Displayer
==============

Application PyQt pour l’affichage et l’analyse des sorties QTQt.

Sous-modules :
- qtqt.ui       : Interface utilisateur (fenêtres, widgets)
- qtqt.data     : Parsing et gestion des données QTQt
- qtqt.plotting : Fonctions de tracés (matplotlib)
- qtqt.core     : Logique centrale (contrôleur, threads, settings)
"""

__version__ = "0.1.0"

# Import public API
from . import data
from . import plotting
from . import core

__all__ = [
    "data",
    "plotting",
    "core",
]
