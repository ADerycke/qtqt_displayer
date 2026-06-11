# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:13:11 2025

@author: Alexis
"""

# IMPORT LIBRARY

#dicuss with the machine
from pathlib import Path

#for the Qt window
as_Qt = True
try:
    from PySide6.QtWidgets import QApplication, QFileDialog
except:
    try:
        from PyQt5.QtWidgets import QApplication, QFileDialog
    except:
        as_Qt = False
        print("Warning : no python Qt installation available so don't use the interface")

        
def get_file(*, racine=''):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()

    filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)')

    return filepath

def get_path(*, name='', extension='txt'):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    default_name = name + "." + extension
    
    path, _ = QFileDialog.getSaveFileName(None, 'Save As', default_name, 'All Files (*)')

    return path

def get_directory(*, filepath=None):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    
    
    
    # Si un chemin racine est fourni, l'utiliser comme point de départ
    if filepath:
        filepath = Path(filepath)
        folder = filepath.parent
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder', str(folder))
    else:
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder')

    return directory

def get_output_filepath(filepath: str, *,
                            image_format: str = ".png",
                            table_format: str = '.xlsx',
                            groupe: bool = False,
                            autopath: bool = True,
                            folder: str = ''
                        )-> tuple[str, str, str, str]:
    """
    Génère les chemins de sortie pour les fichiers de sortie (images et tables).

    Args:
        filepath: Chemin du fichier d'entrée.
        image_format: Extension des images (par défaut ".png").
        table_format: Extension des tables (par défaut ".xlsx").
        groupe: Si True, crée un sous-dossier avec le nom du fichier.
        autopath: Si False, utilise un chemin personnalisé (non implémenté ici).
        folder: '', alow to pass already set folder for racine

    Returns:
        Tuple contenant les chemins des fichiers de sortie :
        (inverse_fig, resample_fig, ages_table, lengths_table)
    """

    filepath = Path(filepath)
    file_name = filepath.stem

    if not autopath :
        if as_Qt and folder == '' :
            folder = Path(get_directory(filepath=filepath))  # Conversion en str si nécessaire
        elif folder == '' :
            folder = filepath.parent
        else:
            folder = Path(folder)
    else :
        folder = filepath.parent

    
    if groupe:
        folder_grp = folder / file_name
        folder_grp.mkdir(exist_ok=True)  # Crée le dossier s'il n'existe pas

        inverse_fig = folder_grp / f"inversion{image_format}"
        resample_fig = folder_grp / f"resample{image_format}"
        ages_table = folder_grp / f"ages{table_format}"
        lengths_table = folder_grp / f"lengths{table_format}"
    else:
        inverse_fig = folder / f"{file_name}_inversion{image_format}"
        resample_fig = folder / f"{file_name}_resample{image_format}"
        ages_table = folder / f"{file_name}_ages{table_format}"
        lengths_table = folder / f"{file_name}_lengths{table_format}"

    return str(inverse_fig), str(resample_fig), str(ages_table), str(lengths_table)
    

