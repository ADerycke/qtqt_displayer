# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 16:52:19 2025

@author: Alexis
"""

def get_scale(total):
    total=int(total)
    if total >= 1000:
        max_scale = 250
        min_scale = 50
    elif 1000 > total >= 400 :
        max_scale = 100
        min_scale = 25
    elif 400 > total >= 150 :
        max_scale = 50
        min_scale = 10
    elif 150 > total >= 35 :
        max_scale = 25
        min_scale = 5
    elif 35 > total >= 15 :
        max_scale = 5
        min_scale = 1
    elif 15 > total >= 2 :
        max_scale = 2
        min_scale = 0.25
    else:
        max_scale = 0.5
        min_scale = 0.05
    
    return max_scale, min_scale