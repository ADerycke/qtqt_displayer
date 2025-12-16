# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 10:46:15 2025

@author: Alexis
"""

#basic librairy
from xarray import DataArray

class RInversion():
    
    def __init__(self, *,data=None):
        
        self.info_list = {}
        self.sample_list = {}
        self.color_list = []
        
        self.tabl_constrain = DataArray()
        self.tabl_tT_history = DataArray()
        self.tabl_tT_pred = DataArray()
        self.tabl_tT_pred_vertical = DataArray()
        
        self.tabl_He_like = DataArray()
        self.tabl_He_post = DataArray()
        self.tabl_He_expect = DataArray()
        
        self.tabl_FT_like = DataArray()
        self.tabl_FT_post = DataArray()
        self.tabl_FT_expect = DataArray()
        
        self.tabl_LFT = DataArray()
        
        #optionnal data
        self.tabl_grid_history = DataArray()
        self.distrib_envelopp = DataArray()
        self.grid_info = []
        
        self.tab_init_resample = DataArray()
        self.tab_resample = DataArray()
        
        if data is not None: self.set_data(data)
        
    
    def set_data(self, data):
        
        self.info_list = data['info_list']
        self.sample_list = data['sample_list']
        self.color_list = data['color_list']
        
        self.tabl_constrain = data['tabl_constrain']
        self.tabl_tT_history = data['tabl_tT_history']
        self.tabl_tT_pred = data['tabl_tT_pred']
        self.tabl_tT_pred_vertical = data['tabl_tT_pred_vertical']
        
        self.tabl_He_like = data['tabl_He_like']
        self.tabl_He_post = data['tabl_He_post']
        self.tabl_He_expect = data['tabl_He_expect']
        
        self.tabl_FT_like = data['tabl_FT_like']
        self.tabl_FT_post = data['tabl_FT_post']
        self.tabl_FT_expect = data['tabl_FT_expect']
        
        self.tabl_LFT = data['tabl_LFT']
        
        #optionnal data
        if "tabl_grid_history" in data:
            self.tabl_grid_history = data['tabl_grid_history']
            self.distrib_envelopp = data['distrib_envelopp']
            self.grid_info = data['grid_info']
        
        if "tab_init_resample" in data:
            self.tab_init_resample = data['tab_init_resample']
            self.tab_resample = data['tab_resample']
        
class RForward():
    
    def __init__(self, *,data=None):
        
        self.info_list = {}
        self.sample_list = {}
        self.color_list = []
        
        self.tabl_tT = DataArray()
        self.tabl_tT_vertical = DataArray()
        
        self.tabl_He = DataArray()
        
        self.tabl_FT = DataArray()
        
        self.tabl_LFT = DataArray()

        
        if data is not None: self.set_data(data)
        
    
    def set_data(self, data):
        
        self.info_list = data['info_list']
        