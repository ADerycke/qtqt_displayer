# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 15:32:20 2025

@author: Alexis
"""

# importation lib general
from PySide6.QtWidgets import QApplication

# import internal logic
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#from displayer.ui.main_window import ResampleWindow
from displayer.ui import dialogs


if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    #resample_wind = ResampleWindow()
    #resample_wind.show()
    test_window = dialogs.HelpWindow('ages')
    test_window.show()
    
    app.exec()

