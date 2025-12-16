# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 17:22:47 2025

@author: Alexis
"""
# importation lib general 
from PySide6.QtWidgets import QApplication

# importation internal logic
import sys
from displayer.core.controller import Controller


# Start the program
def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    main_controller = Controller(app)
    main_controller.show_hide_wind("main",True)
    
    app.exec()