# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 11:10:17 2025

@author: Alexis
"""

# import general lib
from xarray import DataArray
import numpy


# import internal logic
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from displayer.core import workers, savers
from displayer.data import utils
#from displayer.data.datatypes import RInversion


def extract_tT_pred(data, *, forward=False):
    max_point = 3
    
    #bloc 1
    Chemin_loc = data[data[data.columns[0]].str.contains('Max Like')]
    nb_point_like = data[Chemin_loc.index[0]+2 : Chemin_loc.index[0]+3].values
    Chemin_val = data[Chemin_loc.index[0]+1 : Chemin_loc.index[0] + 3]
    Chemin_val_like = Chemin_val.squeeze()
    Chemin_val_like = Chemin_val_like.str.split(n=-1, expand=True)
    Chemin_val_like.rename(columns={2:"Like",4:"Posterior"},inplace=True)
    Chemin_point = data[Chemin_loc.index[0]+3 : Chemin_loc.index[0] + 3 + int(nb_point_like)]
    Chemin_point_like = Chemin_point.squeeze()
    Chemin_point_like = Chemin_point_like.str.split(n=-1, expand=True)
    Chemin_point_like.rename(columns={0:"point",1:"Time",2:"Temp",3:"Z"},inplace=True)
    max_point = max(int(nb_point_like),max_point)
    
    if not forward:
        #bloc 2
        Chemin_loc = data[data[data.columns[0]].str.contains('Max Post')]
        nb_point_post = data[Chemin_loc.index[0]+2 : Chemin_loc.index[0]+3].values
        Chemin_val = data[Chemin_loc.index[0]+1 : Chemin_loc.index[0] + 3]
        Chemin_val_post = Chemin_val.squeeze()
        Chemin_val_post = Chemin_val_post.str.split(n=-1, expand=True)
        Chemin_val_post.rename(columns={2:"Like",4:"Posterior"},inplace=True)
        Chemin_point = data[Chemin_loc.index[0]+3 : Chemin_loc.index[0] + 3 + int(nb_point_post)]
        Chemin_point_post = Chemin_point.squeeze()
        Chemin_point_post = Chemin_point_post.str.split(n=-1, expand=True)
        Chemin_point_post.rename(columns={0:"point",1:"Time",2:"Temp",3:"Z"},inplace=True)
        max_point = max(int(nb_point_post),max_point)
        
        #bloc 3
        Chemin_loc = data[data[data.columns[0]].str.contains('EXPECTED')]
        nb_point_expect = data[Chemin_loc.index[0]+3 : Chemin_loc.index[0]+4].values
        nb_point_expect = nb_point_expect[0,0].split(' ')
        Chemin_point = data[Chemin_loc.index[0]+4 : Chemin_loc.index[0] + 4 + int(nb_point_expect[0])]
        Chemin_point_expect = Chemin_point.squeeze()
        Chemin_point_expect = Chemin_point_expect.str.split(n=-1, expand=True)
        Chemin_point_expect.rename(columns={0:"Time",1:"T_Expected",2:"T_Mode",3:"T_env_sup",4:"T_env_inf"},inplace=True)
        max_point = max(int(nb_point_expect[0]),max_point)
    
    
    #recup dans un xarray
    if not forward:
        X = range(3) #time, temperature, info
        Y = range(max_point)
        Chemin = range(6)
        #data_tT.clear()
        data_Chemin = DataArray(
            data=numpy.full((len(Chemin),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'Chemin': Chemin},
            dims=('Chemin','Y', 'X')
        )
        
        utils.get_chemin (0, data_Chemin, Chemin_point_like,Chemin_val_like, max_point, int(nb_point_like), 'Temp')
        data_Chemin[0,0,2]='Max likelihood'
        utils.get_chemin (1, data_Chemin, Chemin_point_post,Chemin_val_post, max_point, int(nb_point_post), 'Temp')
        data_Chemin[1,0,2]='Max posterior'
        utils.get_chemin (2, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_Expected')
        data_Chemin[2,0,2]='Expected model'
        utils.get_chemin (3, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_Mode')
        data_Chemin[3,0,2]='Max mode model'
        utils.get_chemin (4, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_env_sup')
        data_Chemin[4,0,2]='Envelope sup. (99%)'
        utils.get_chemin (5, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_env_inf')
        data_Chemin[5,0,2]='Envelope inf. (99%)'
    else:
        X = range(3) #time, temperature, info
        Y = range(max_point)
        data_Chemin = DataArray(
            data=numpy.full((len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y},
            dims=('Y', 'X')
        )
        data_Chemin[:,0]=Chemin_point_like.Time
        data_Chemin[:,1]=Chemin_point_like['Temp']
        
        data_Chemin[0,2]='Max likelihood'

    return data_Chemin

#data_inversion = RInversion()

filepath = savers.get_file()[0]
QTQt_summary, QTQt_tto_fix, QTQt_Hierachical = workers.read_QTQt_files(filepath)


tabl_tT = extract_tT_pred(QTQt_summary, forward=True)

# %%



print(tabl_tT)