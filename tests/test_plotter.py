# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 17:19:24 2025

@author: Alexis
"""

# import external logic
from matplotlib.pyplot import figure

# import internal logic
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from displayer.plotting.figures import InverseFig

displayer_fig = figure(FigureClass=InverseFig)
displayer_fig.show()



