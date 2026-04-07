# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:13:11 2025

@author: Alexis
"""

# IMPORT LIBRARY

#dicuss with the machine
import sys
import os

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

    #if "win" in sys.platform:
    filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)')
    # else:
    #     filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)',  options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)

    return filepath

def get_path(*, name='', extension='txt'):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    default_name = name + "." + extension
    
    #if "win" in sys.platform:
    path, _ = QFileDialog.getSaveFileName(None, 'Save As', default_name, 'All Files (*)')
    # else:
    #     path, _ = QFileDialog.getSaveFileName(None, 'Save As', default_name, 'All Files (*)', options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)

    return path

def get_directory(*, racine=''):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()

    # Si un chemin racine est fourni, l'utiliser comme point de départ
    if racine:
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder', racine)
    else:
        directory = QFileDialog.getExistingDirectory(None, 'Select a folder')

    return directory

def get_output_filepath(filepath, *, image_format = ".png", table_format = '.xlsx', groupe=False, autopath=True):
    
    folder = os.path.dirname(filepath)
    file_name = os.path.basename(filepath)
    
    file_name = filepath.replace(" ","_")
    file_name = file_name.replace(".txt",'')
    
    if not autopath and not as_Qt :
        folder = get_directory(racine=folder)
    
    if groupe :
        folder_grp = os.path.join(folder,file_name)
        if not os.path.exists(folder_grp): os.makedirs(folder_grp)
        inverse_fig = os.path.join(folder_grp, "inversion" + image_format)
        resample_fig = os.path.join(folder_grp, "resample" + image_format)
        
        ages_table = os.path.join(folder_grp, "ages" + table_format)
        lengths_table = os.path.join(folder_grp, "lengths" + table_format)
    
    else:
        inverse_fig = os.path.join(folder, file_name + "_inversion" + image_format)
        resample_fig = os.path.join(folder, file_name + "_resample" + image_format)
        
        ages_table = os.path.join(folder, file_name + "_ages" + table_format)
        lengths_table = os.path.join(folder, file_name + "_lengths" + table_format)

    return inverse_fig, resample_fig, ages_table, lengths_table
    

# def get_QTQt_files(file_path, file_name, file_type):
    
#     if file_type == "summary":
#         file_ext = ".txt"
        
#         test_path_percent_files = os.path.join(file_path, file_name + "_tto_fix" + file_ext) #predicted envelope
#         if path.exists(test_path_percent_files):
#             QTQt_tto_fix = read_csv(test_path_percent_files, sep='chaineimpossible', engine='python', header=None)
#         else:
#             QTQt_tto_fix = "vide"
#         test_resample_files =  os.path.join(file_path, file_name + "_Hierachical" + file_ext)#kinetic resample
#         if path.exists(test_resample_files):
#             QTQt_Hierachical = read_csv(test_resample_files, sep='chaineimpossible', engine='python', header=None)
#         else:
#             QTQt_Hierachical = "vide"
        
#         return QTQt_tto_fix, QTQt_Hierachical
         
#     elif file_type == "sample" :
        
#         if os.path.exists(file_name):
#              #connecter au parseur de fichier pour connaitre les paramètres de modélisation
#         else:
#             #retourner une valeur vide
        

# def save_QTQt_fig (self, filepath, , *,autopath=False):
#     if autopath == False:
#         file_name = filepath.replace(" ","_")
#         test = file_name.split('/')
#         file_name = test[len(test)-1]
#         file_name = file_name.replace(".txt",'')
#         complete_path = get_path(name= file_name, extension=file_format)
#         complete_path = str(complete_path)
#         complete_path = complete_path.replace("<_io.TextIOWrapper name='",'').replace("' mode='w' encoding='cp1252'>", '')
#     else:
#         filepath = filepath.replace(".txt","")
#         complete_path = str(filepath + file_format)
#     self.figure.savefig(complete_path, format=file_format, bbox_inches='tight')