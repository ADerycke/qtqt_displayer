# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:13:11 2025

@author: Alexis
"""

# importation lib general 
from PySide6.QtWidgets import QApplication

# importation internal logic
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from displayer.core.controller import Controller


# Start the program
if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    main_controller = Controller(app)
    main_controller.show_hide_wind("main",True)
    
    app.exec()