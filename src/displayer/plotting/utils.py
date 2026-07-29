# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 16:52:19 2025

@author: Alexis
"""

from lttb import downsample
import numpy as np

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

def val_to_str(valeur, prefixe = '', remplacement = '', sufixe = '', test = 0): # change valeur to display for exploration parameters
    if float(valeur) != valeur :
        text = remplacement
    elif valeur == test:
        text = remplacement
    else:
        valeur = float(valeur)
        if "%" in sufixe : valeur = valeur * 100
        text = prefixe + str(round(valeur)) + sufixe
        
    return text

def val_to_time_str(valeur):
    if round(valeur,0)/60/60 >= 1:
        text = str(round(valeur/60/60,1)) + ' h.'
    else:
        text = str(round(valeur/60)) + ' min.'
    
    return text


def tT_downscale(data_tT, dim="iteration", n_out=10000, y_index=1, x_index=3):
    """
    Réduit un DataArray xarray suivant une dimension en utilisant
    les indices LTTB calculés sur une série de référence.
    """

    # Série de référence
    ref = data_tT.isel(Y=y_index, X=x_index).values

    x = np.arange(len(ref))
    reduced = downsample(np.column_stack((x, ref)), n_out=n_out)

    indices = reduced[:, 0].astype(int)

    return data_tT.isel({dim: indices})