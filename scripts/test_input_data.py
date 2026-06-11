# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 21:39:33 2026

@author: Alexis
"""

import pandas


#for the Qt window
try:
    from PySide6.QtWidgets import QApplication, QFileDialog
except:
    from PyQt5.QtWidgets import QApplication, QFileDialog

        
def get_file(*, racine=''):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()


    filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine)

    return filepath


def build_data_dict(excel_file_path):
    """
    Lit un fichier Excel et construit un dictionnaire structuré par page,
    où chaque page est associée à un dictionnaire de données filtrées par la colonne "QTQt value".
    """
    xls = pandas.ExcelFile(excel_file_path)
    sheet_names = xls.sheet_names
    data_dict = {}

    for sheet_name in sheet_names:
        df = pandas.read_excel(excel_file_path, sheet_name=sheet_name)

        # Solution 1: Supprimer les doublons
        filtered_data = df.drop_duplicates(subset=["QTQt value"]).set_index("QTQt value").to_dict(orient="index")

        data_dict[sheet_name] = filtered_data

    return data_dict

# Exemple d'utilisation
if __name__ == "__main__":
    excel_file_path = get_file()[0]
    data_dict = build_data_dict(excel_file_path)
    test = data_dict["Radiation models"][-2]









