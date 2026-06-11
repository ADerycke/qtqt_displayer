# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 10:46:15 2025

@author: Alexis
"""

#basic librairy
from xarray import DataArray
from pathlib import Path

#internal lib
from . import utils


class RInversion:
    
    def __init__(self, *,data=None):
        
        self.info_list = {}
        self.sample_list = {}
        self.color_list = []
        
        self.tabl_constrain = DataArray()
        self.tabl_tT_history = DataArray()
        self.tabl_tT_pred = DataArray()
        
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
        
class RForward:
    
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
        
        
class Sample:
    
    def __init__(self, summary_name, filepath, ID, color):
        
        path_obj = Path(filepath)
        self.filepath_ = filepath
        self.folder_ = str(path_obj.parent)
        
        self.name_ = str(path_obj.name).replace('.txt','')
        self.clean_name_ = utils.clean_name(self.name_)
        self.id_ = ID
        
        self.parent_ = summary_name
        
        self.color_ = color
        
        #additionnal data
        self.FT_kin_ = None
        self.eU_tab_ = None
        self.max_time_ = None
    
    def __repr__(self):
        return 'sample = ' + self.name_ + '\n - clean_name : ' + self.clean_name_ + '\n - summary : ' + self.parent_ + '\n - id : ' + self.id_
    
    
class SampleList:

    def __init__(self, summary_name):
        self.summary_name_ = summary_name
        self.samples_: list[Sample] = []

    def add_sample(self, filepath, ID, tab_color):
        # vérifie si un sample avec le même nom existe déjà
        for sample in self.samples_:
            if sample.filepath_ == filepath:
                sample.parent_ = self.summary_name_
                return
        # sinon ajout
        self.samples_.append(Sample(self.summary_name_, filepath, ID, tab_color[0]))
        #remove the color as is use
        tab_color.pop(0)

    def get_sample_by_name(self, name):
        for sample in self.samples_:
            if sample.name_ == name and sample.parent_ == self.summary_name_ :
                return sample
            
        return None
    
    def get_sample_by_clean_name(self, clean_name):
        
        for sample in self.samples_:
            print(clean_name + ' vs ' + sample.clean_name_)
            if sample.clean_name_ == clean_name and sample.parent_ == self.summary_name_ :
                return sample
            
        return None

    def get_sample_by_id(self, ID):
        for sample in self.samples_:
            if sample.id_ == ID and sample.parent_ == self.summary_name_ :
                return sample
            
        return None
        
    def get_name_by_id(self, ID):
        for sample in self.samples_:
            if sample.id_ == ID and sample.parent_ == self.summary_name_ :
                return sample.clean_name_
            
        return None
    
    def get_color_by_name(self, clean_name):
        for sample in self.samples_:
            if sample.clean_name_ == clean_name and sample.parent_ == self.summary_name_ :
                return sample.color_
            
        return None
    
    def get_color_by_id(self, ID):
        for sample in self.samples_:
            if sample.id_ == ID and sample.parent_ == self.summary_name_ :
                return sample.color_
            
        return None
    
    def get_tabeU_by_id(self, ID):
        for sample in self.samples_:
            if sample.id_ == ID and sample.parent_ == self.summary_name_ :
                return sample.eU_tab_
            
        return None
    
    def get_summary_len(self):
        n = 0
        for sample in self.samples_:
            if sample.parent_ == self.summary_name_ :
                n += 1
                
        return n
    
    def get_max_time_summary(self):
        n = -1
        for sample in self.samples_:
            if sample.parent_ == self.summary_name_ and sample.max_time_ > n :
                n = sample.max_time_
        return n
    
    def list_summary_samples(self):
        summary_samples : list[Sample] = []
        for sample in self.samples_:
            if sample.parent_ == self.summary_name_ :
                summary_samples.append(sample)
        
        return summary_samples
  
    def __repr__(self):
        return 'actual summary = ' + self.summary_name_ + '\n - nb of sample : ' + str(len(self.samples_))
  
    
if __name__ == "__main__" :
    
    
    # parent = "test.txt"
    
    # file_path = "D:/QTQt/Modelisation - QTQt/McClure - publication/Data - AHe ZHe AFT - rmr0 a 0/Anderson (Gerin).txt"
    # ID = 0 
    
    # test = Sample(parent,file_path,ID)
    
    test = RInversion()