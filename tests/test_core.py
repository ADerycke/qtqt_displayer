# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 14:58:00 2025

@author: Alexis
"""

# import general lib


# import internal logic
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from displayer.core import saver, workers


# %%
filepaths = saver.get_file()
filepath = filepaths[0]
QTQt_summary, QTQt_tto_fix, QTQt_Hierachical = workers.read_QTQt_files(filepath)