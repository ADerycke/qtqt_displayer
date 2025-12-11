# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 11:30:48 2025

@author: Alexis
"""


#import basic lib
#for plotting 
from matplotlib.gridspec import GridSpec
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

#import internal logic
from . import plotter


class InverseFig(Figure):
    
    def __init__(self, *args, **kwargs):
        super().__init__(figsize=(17, 6))
        
        self.tight_layout()
        self.subplots_adjust(left=0.04, right=0.96, bottom=0.1, top=0.9)
        
        #figure generale
        structure = GridSpec(
            ncols=8,
            width_ratios=[1, 0.2, 1, 0.6, 1, 1, 1, 0.05],
            nrows=6,
            height_ratios=[0.2, 1, 1, 1, 1, 1],
        )
        
        #add chart sub plot
        self.subplot_FT = self.add_subplot(structure[1:3, 0])
        self.subplot_FT_bis =self.subplot_FT.twinx()
         
        self.subplot_like = self.add_subplot(structure[1, 2])
        self.subplot_post = self.add_subplot(structure[2, 2])
        self.subplot_age = self.add_subplot(structure[3:5, 2])
         
        self.subplot_history = self.add_subplot(structure[1:5, 4:7])
        self.subplot_history_bis =self.subplot_history.twinx()
        self.subplot_timescale = self.add_subplot(structure[0, 4:7], sharex=self.subplot_history)
         
        self.subplot_hist_legen = self.add_subplot(structure[1:5, 7])
         
         #add info sub plot
        self.subplot_samples = self.add_subplot(structure[3:, 0])
        self.subplot_hist_parameters = self.add_subplot(structure[5, 3:7])
        
        #update layout
        self.init_layout()
    
    def init_layout(self):
        # chart layout
        plotter.layout_iteration([self.subplot_like, self.subplot_post])
        plotter.layout_pred_ages(self.subplot_age)
        plotter.layout_LFT([self.subplot_FT, self.subplot_FT_bis])
        plotter.layout_history([self, self.subplot_history, self.subplot_history_bis, self.subplot_hist_legen])
        plotter.layout_time_scale(self.subplot_timescale)
        
        plotter.layout_informations(self.subplot_samples)
        plotter.layout_informations(self.subplot_hist_parameters)
        
    def plot_iteration(self, *args, **kwargs):
        plotter.plot_iteration([self.subplot_like, self.subplot_post], *args, **kwargs)
        
    def plot_pred_ages(self, *args, **kwargs):
        plotter.plot_pred_ages(self.subplot_age, *args, **kwargs)
    
    def plot_LFT(self, *args, **kwargs):
        plotter.plot_LFT([self.subplot_FT, self.subplot_FT_bis], *args, **kwargs)
        
    def plot_histoire(self, *args, **kwargs):
        plotter.plot_histoire([self, self.subplot_history, self.subplot_history_bis, self.subplot_hist_legen], *args, **kwargs)
    
    def plot_time_scale(self, *args, **kwargs):
        plotter.plot_time_scale(self.subplot_timescale, *args, **kwargs)

    def add_information(self, *args, **kwargs):
        plotter.add_information(self.subplot_hist_parameters, *args, **kwargs)
    
    def add_samples(self, *args, **kwargs):
        plotter.add_samples(self.subplot_samples, *args, **kwargs)


class ResampleFig(Figure):
    
    def __init__(self, *args, num_graphs=2, **kwargs):
        super().__init__(figsize=(10, num_graphs * 3))
        
        self.num_graphs = num_graphs
        self.axs = self.subplots(self.num_graphs, 1, sharex=True)
        self.linestyles = ['-', '--', '-.', ':',
                      (0, (5, 1)),
                      (0, (3, 5, 1, 5)),
                      (0, (5, 5)),
                      (0, (3, 1, 1, 1)), 
                      (0, (1, 1)),
                      (0, (5, 10))
                      ]
    
    def update_size(self, num_graphs):
        self.num_graphs = num_graphs
        self.clf()
        self.set_size_inches(10, self.num_graphs * 3, forward=True)
        self.axs = self.subplots(self.num_graphs, 1, sharex=True)

    def plot_resample(self, data_init, data_resample, sample_list, color_list):
        num_sample = data_init.shape[0] 

        #premier graph likelihood
        graph_pos = 0
        x = data_resample[0, 0, :].astype(int)
        y = data_resample[0, 1, :].astype(float)
        self.axs[graph_pos].plot(x, y, linestyle='-', color='red', linewidth = 0.5)
        self.axs[graph_pos].set_ylabel('likelihood')

        #deuxieme graph FT kin
        graph_pos = 1
        for i in range(num_sample):
            x = data_resample[i, 0, :].astype(int)
            y = data_resample[i, 2, :].astype(float)
            self.axs[graph_pos].plot(x, y, linestyle="-", color=color_list[sample_list[i]['name']])
        self.axs[graph_pos].set_ylabel('FT kinetic\nparameters')
        
        # Boucle sur chaque ligne de data_init
        graph_pos = 1
        for i in range(num_sample):
            tempo_nb_he = int(data_init[i, 5])
            
            if tempo_nb_he > 0 :
                graph_pos = 1 + graph_pos
                # Boucle sur le nombre de courbes à tracer pour ce subplot
                for j in range(tempo_nb_he):
                    x = data_resample[i, 0, :].astype(int)
                    y = data_resample[i, 3 + j, :].astype(float)
                    y_bis = sample_list[i]['eU_' + str(j)] * (1+(y/100))

                    # Tracer la courbe dans le subplot correspondant à l'index i
                    self.axs[graph_pos].plot(x, y_bis, linestyle=self.linestyles[j % len(self.linestyles)], color=color_list[sample_list[i]['name']])

                # Ajouter des labels et une légende à chaque subplot
                self.axs[graph_pos].set_ylabel(sample_list[i]['name'] + '\neU [ppm]')
        
        num_graphs = graph_pos + 1
        
        if num_graphs != self.num_graphs :
            self.update_size(num_graphs)
        
        for i in range(num_graphs):
            # Masquer les axes x de tous les subplots sauf le premier et le dernier
            self.axs[i].spines['bottom'].set_visible(False)
            self.axs[i].spines['top'].set_visible(False)
            self.axs[i].xaxis.set_tick_params(which='major', direction='inout', length=5, width=1, 
                                     color='black', labelcolor='black', top=True, bottom=True)
            self.axs[i].xaxis.set_tick_params(which='minor', direction='in', length=2, width=0.5, 
                                     color='black', labelcolor='black', top=True, bottom=True)
            self.axs[i].yaxis.set_tick_params(which='major', direction='inout', length=5, width=1, 
                                     color='black', labelcolor='black', left=True, right=True)
            self.axs[i].yaxis.set_tick_params(which='minor', direction='in', length=2, width=0.5, 
                                     color='black', labelcolor='black', left=True, right=True)
            
            if i == 0 : 
                self.axs[i].spines['bottom'].set_visible(True)
                self.axs[i].spines['top'].set_visible(True) 
                self.axs[i].set_xlabel('iteration')
                self.axs[i].xaxis.set_label_position('top')
            elif i == 1:
                self.axs[i].get_xaxis().set_visible(True)
                self.axs[i].xaxis.set_label_position('top')
                self.axs[i].spines['top'].set_visible(True)
                self.axs[i].tick_params(axis='x', labeltop=True, labelbottom=False)
                self.axs[i].xaxis.set_major_formatter(FuncFormatter(lambda x, p: '{:,}'.format(int(x)).replace(",", " ")))
            elif i == num_graphs - 1:  # Le dernier subplot
                self.axs[i].get_xaxis().set_visible(True)
                self.axs[i].xaxis.set_label_position('bottom')
                self.axs[i].spines['bottom'].set_visible(True)
                self.axs[i].set_xlabel('iteration')
                self.axs[i].tick_params(axis='x', labeltop=False, labelbottom=True)
                self.axs[i].xaxis.set_major_formatter(FuncFormatter(lambda x, p: '{:,}'.format(int(x)).replace(",", " ")))
