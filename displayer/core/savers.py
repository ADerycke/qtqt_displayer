# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:13:11 2025

@author: Alexis
"""

# IMPORT LIBRARY

#dicuss with the machine
import sys

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

    if "win" in sys.platform:
        filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)')
    else:
        filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)',  options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)

    return filepath

def get_path(*, name='', extension='txt', racine=''):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    default_name = name + "." + extension
    
    if "win" in sys.platform:
        path, _ = QFileDialog.getSaveFileName(None, 'Save As', default_name, 'All Files (*)')
    else:
        path, _ = QFileDialog.getSaveFileName(None, 'Save As', default_name, 'All Files (*)', options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)

    return path

def save_QTQt_fig (self, filepath, file_format, *,autopath=False):
    if autopath == False:
        file_name = filepath.replace(" ","_")
        test = file_name.split('/')
        file_name = test[len(test)-1]
        file_name = file_name.replace(".txt",'')
        complete_path = get_path(name= file_name, extension=file_format)
        complete_path = str(complete_path)
        complete_path = complete_path.replace("<_io.TextIOWrapper name='",'').replace("' mode='w' encoding='cp1252'>", '')
    else:
        filepath = filepath.replace(".txt","")
        complete_path = str(filepath + "." + file_format)
    self.figure.savefig(complete_path, format=file_format, bbox_inches='tight')