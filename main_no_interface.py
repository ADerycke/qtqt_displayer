# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 17:09:44 2025

@author: Alexis
"""

# general lib
from pandas import read_csv
from os import path

# figure lib
from matplotlib.colors import TABLEAU_COLORS, hex2color
from matplotlib.pyplot import rcParams

# internal lib
import sys, os
sys.path.append(os.path.dirname(__file__))
from displayer.data import parser
from displayer.data.datatypes import RInversion
from displayer.plotting import plotter
from displayer.core import savers, workers

# %%  GENERAL FUNCTION

def define_parameters(): #recup info de la main window
    inversion_param = {
        'save_format': '', # "png", "pdf", "svg",
        'auto_save_path' : True, # False
        'time_min':-1,
        'time_max':0,
        'temp_min':-1,
        'temp_max':0,
            
        'chemin' : 'all', #'heatmap', 'simple'
        'colormap' : 'viridis_r', #'cividis_r', 'jet', 'QTQt_old',...
        'classement':'Likelihood', #"Posterior", "Iteration"
        'hist_color' : "Likelihood", # "Posterior"
        'model' : "Max Likelihood", #"Max Posterior", "Expected"
        'gradiant' : 30,
        'niveau' :"Epoch", # "Eon", "Era", "Period", "Superepoch", "Age"
        'vertical_profile' : "no", # "Max Likelihood", "Max Posterior", "Expected"
        }
        
    return inversion_param



# %% INITIALIZE GLOBAL VARIABLE (as minimum as possible...)

# load an initial color liste for sample
global font_size
tab_color = {}

# generer un table de couleurs / noms d'échantillons de base de 50 (limite maximum)
n=1
for i in range(50):
    for item, value in TABLEAU_COLORS.items():
        tab_color["sample " + str(n)] = hex2color(value)
        n = n + 1
del n

#font size and figure parameters :
font_size = 11
params = {
         'legend.title_fontsize': font_size + 2,
         'legend.fontsize': font_size,
         'axes.labelsize': font_size,
         'axes.titlesize':font_size + 2,
         'xtick.labelsize':font_size - 2,
         'ytick.labelsize':font_size - 2,
         'font.size':font_size - 2,
         "axes.titlecolor": "black",
         "axes.labelcolor": "black",
         "xtick.color": "black",
         "ytick.color": "black",
         }
rcParams.update(params)

# %% CONTRUIRE LA FIGURE
displayer_figure = plotter.built_fig()

# %% OUVRIR LE FICHIER    
filepath = savers.get_file()[0]
QTQt_summary = read_csv(filepath, sep='chaineimpossible', engine='python', encoding='latin1')

# test to see if their is additionnal informationnal files
file_name, file_ext = path.splitext(filepath)
test_path_percent_files = file_name + "_tto_fix" + file_ext #predicted envelope
if path.exists(test_path_percent_files):
    QTQt_tto_fix = read_csv(test_path_percent_files, sep='chaineimpossible', engine='python', header=None)
else:
    QTQt_tto_fix = "vide"
test_resample_files = file_name + "_Hierachical" + file_ext #kinetic resample
if path.exists(test_resample_files):
    QTQt_Hierachical = read_csv(test_resample_files, sep='chaineimpossible', engine='python', header=None)
else:
    QTQt_Hierachical = "vide"


# %% PROCESS LE FICHIER
data_inversion = RInversion()

#get/load color dictionnary
if 'color_list' in globals() :
    data_inversion.color_list, data_inversion.sample_list = parser.get_colorlist(QTQt_summary, tab_color)
else:
    data_inversion.color_list, data_inversion.sample_list = parser.get_colorlist(QTQt_summary, tab_color)
data_inversion.info_list = parser.get_inversion_info(QTQt_summary)


# get data from the file
data_inversion.tabl_tT_history = parser.extract_tT_history(QTQt_summary)
#optional files
if not isinstance(QTQt_tto_fix, str):
    data_inversion.tabl_grid_history, data_inversion.distrib_envelopp, data_inversion.grid_info = parser.extract_grid_history(QTQt_tto_fix)
if not isinstance(QTQt_Hierachical, str):
    data_inversion.tab_init_resample, data_inversion.tab_resample = parser.extract_resample(QTQt_Hierachical)

#results
data_inversion.tabl_constrain = parser.extract_constrain(QTQt_summary)
data_inversion.tabl_tT_pred = parser.extract_tT_pred(QTQt_summary)
data_inversion.tabl_tT_pred_vertical = parser.extract_tT_pred_vertical(QTQt_summary, data_inversion.sample_list)
data_inversion.tabl_He_like, data_inversion.tabl_He_post, data_inversion.tabl_He_expect = parser.extract_He_Ages(QTQt_summary)
data_inversion.tabl_FT_like, data_inversion.tabl_FT_post, data_inversion.tabl_FT_expect = parser.extract_FT_Ages(QTQt_summary)
data_inversion.tabl_LFT = parser.extract_FT_Length(QTQt_summary)


# update list info
k = -1
if not isinstance(QTQt_Hierachical, str):
    for i in data_inversion.sample_list:
        it_maxlike = data_inversion.tab_resample[i,1,:].argmax().item()
        data_inversion.sample_list[i]['FT_kin'] = float(data_inversion.tab_resample[i,2,it_maxlike])
        tab_eU_percent = data_inversion.tab_resample[i,3:,it_maxlike]

        #test if there is He data
        if not tab_eU_percent.isnull().values[0] :
            k = k + 1
            for j in range(len(tab_eU_percent)):
                if not tab_eU_percent.isnull().values[j] :
                    tab_eU_mod = data_inversion.tabl_He_like[k,:,6]
                    data_inversion.sample_list[i]['eU_' + str(j)] = float(tab_eU_mod[j].values) / (1+(float(tab_eU_percent[j].values)/100))

# %% AFFICHER LA FIGURE PRINCIPAL
inversion_param = define_parameters()

plotter.plot_iteration(displayer_figure, data_inversion.tabl_tT_history, data_inversion.info_list)
plotter.plot_pred_ages(displayer_figure, data_inversion.tabl_He_like, data_inversion.tabl_He_post, data_inversion.tabl_He_expect,
               data_inversion.tabl_FT_like, data_inversion.tabl_FT_post, data_inversion.tabl_FT_expect,
               data_inversion.color_list, model=inversion_param['model'])
plotter.plot_LFT(displayer_figure, data_inversion.tabl_LFT, data_inversion.color_list, model=inversion_param['model'])
if not isinstance(QTQt_tto_fix, str):
    plotter.plot_histoire(displayer_figure, data_inversion.tabl_tT_history, data_inversion.tabl_tT_pred, data_inversion.tabl_tT_pred_vertical, data_inversion.tabl_constrain, classement=inversion_param['classement'], color=inversion_param['hist_color'],
                  history=inversion_param['chemin'], gradiant=inversion_param['gradiant'], time_min=inversion_param['time_min'], time_max=inversion_param['time_max'], temp_min=inversion_param['temp_min'], temp_max=inversion_param['temp_max'],
                  colormap=inversion_param['colormap'], vertical_profile=inversion_param['vertical_profile'], data_stat=data_inversion.tabl_grid_history, enveloppe=data_inversion.distrib_envelopp, grid_info = data_inversion.grid_info)
else:
    plotter.plot_histoire(displayer_figure, data_inversion.tabl_tT_history, data_inversion.tabl_tT_pred, data_inversion.tabl_tT_pred_vertical, data_inversion.tabl_constrain, classement=inversion_param['classement'], color=inversion_param['hist_color'],
                  history=inversion_param['chemin'], gradiant=inversion_param['gradiant'], time_min=inversion_param['time_min'], time_max=inversion_param['time_max'], temp_min=inversion_param['temp_min'], temp_max=inversion_param['temp_max'],
                  colormap=inversion_param['colormap'], vertical_profile=inversion_param['vertical_profile'])
plotter.plot_time_scale(displayer_figure, data_inversion.tabl_tT_history, niveau=inversion_param['niveau'], time_min=inversion_param['time_min'], time_max=inversion_param['time_max'], temp_min=inversion_param['temp_min'], temp_max=inversion_param['temp_max'])
plotter.plot_info(displayer_figure, data_inversion.info_list)
plotter.add_legende(displayer_figure, data_inversion.sample_list, data_inversion.color_list)
displayer_figure.canvas.draw()


# %% AFFICHER LA FIGURE SECONDAIRE
if not isinstance(QTQt_Hierachical, str):
    num_sample = data_inversion.tab_init_resample.shape[0] 
    num_graphs = 2
    # compter le nombre d'echantillon avec des data He
    for i in range(num_sample):
        if int(data_inversion.tab_init_resample[i, 5]) > 0 : num_graphs = num_graphs + 1    
    resample_figure = plotter.built_resample_fig(num_graphs=num_graphs)
    plotter.plot_resample(resample_figure, data_inversion.tab_init_resample, data_inversion.tab_resample, data_inversion.sample_list, data_inversion.color_list) 

# %% EXPORT FIGURE
if inversion_param['save_format'] != '':
    displayer_figure.canvas.setFixedWidth(1680)
    displayer_figure.canvas.setFixedHeight(500)
    savers.save_QTQt_fig(displayer_figure, filepath, inversion_param['save_format'], autopath=inversion_param['auto_save_path'])
    
# %% EXPORT DATA
export_data = "no"
export_age = savers.get_path(extension='xlsx')
export_length = savers.get_path(extension='xlsx')

if export_data != 'no':
    workers.export_age(data_inversion,filepath= export_age)
    workers.export_length(data_inversion,filepath= export_length)
