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

__version__ = "1.0.0"
__author__ = "Alexis Derycke"
__email__ = "alexis.derycke@hotmail.com"
__description__ = "package python pour traiter et afficher les résutats du logiciel QTQt"
__url__ = "https://https://github.com/ADerycke/qtqt_displayer"
__license__ = "CC0 1.0"
__copyright__ = "Copyright 2025, Alexis Derycke"


# Import internal API
from . import data
from . import plotting
from . import core

__all__ = [
    "data",
    "plotting",
    "core",
]
