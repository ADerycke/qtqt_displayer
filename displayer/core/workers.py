# IMPORT LIBRARY

#basic librairy
from pandas import read_csv
from pandas import DataFrame, concat, NaT

#dicuss with the machine
from os import path

# internal lib
from displayer.data import parser
from displayer.data.datatypes import RInversion
from displayer.plotting import plotter

from . import savers


def read_QTQt_files(filepath):
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
    
    return QTQt_summary, QTQt_tto_fix, QTQt_Hierachical

def samples_info(QTQt_summary, tab_color, *, color_list=''):
    color_list, sample_list = parser.get_colorlist(QTQt_summary, tab_color, color_list=color_list)
    info_list = parser.get_inversion_info(QTQt_summary)
    tabl_constrain = parser.extract_constrain(QTQt_summary)
    
    return info_list, sample_list, color_list, tabl_constrain

def paths_info(QTQt_summary, sample_list, *, QTQt_tto_fix = ''):
    tabl_tT_history = parser.extract_tT_history(QTQt_summary)
    if isinstance(QTQt_tto_fix, str):
        tabl_grid_history = "vide"
        distrib_envelopp = "vide"
        grid_info = []
    else:
        tabl_grid_history, distrib_envelopp, grid_info = parser.extract_grid_history(QTQt_tto_fix)
    tabl_tT_pred = parser.extract_tT_pred(QTQt_summary)
    tabl_tT_pred_vertical = parser.extract_tT_pred_vertical(QTQt_summary, sample_list)
    
    return tabl_tT_history, tabl_grid_history, distrib_envelopp, grid_info, tabl_tT_pred, tabl_tT_pred_vertical
    
def prediction_info(QTQt_summary):
    tabl_He_like, tabl_He_post, tabl_He_expect = parser.extract_He_Ages(QTQt_summary)
    tabl_FT_like, tabl_FT_post, tabl_FT_expect = parser.extract_FT_Ages(QTQt_summary)
    tabl_LFT = parser.extract_FT_Length(QTQt_summary)
    
    return tabl_He_like, tabl_He_post, tabl_He_expect, tabl_FT_like, tabl_FT_post, tabl_FT_expect, tabl_LFT

def sampling_info(QTQt_Hierachical, sample_list, tabl_He_like):
    tab_init_resample, tab_resample = parser.extract_resample(QTQt_Hierachical)
    
    # update list info
    k = -1
    for i in sample_list:
        it_maxlike = tab_resample[i,1,:].argmax().item()
        sample_list[i]['FT_kin'] = float(tab_resample[i,2,it_maxlike])
        tab_eU_percent = tab_resample[i,3:,it_maxlike]

        #test if there is He data
        if not tab_eU_percent.isnull().values[0] :
            k = k + 1
            for j in range(len(tab_eU_percent)):
                if not tab_eU_percent.isnull().values[j] :
                    tab_eU_mod = tabl_He_like[k,:,6]
                    sample_list[i]['eU_' + str(j)] = float(tab_eU_mod[j].values) / (1+(float(tab_eU_percent[j].values)/100))
    #else:
    #    for i in sample_list:
    #        sample_list[i]['FT_kin'] = float(tabl_FT_like[i,0,8])
    #        tab_eU_percent = tabl_He_like[i,:,6]
    #        for j in range(len(tab_eU_percent)):
    #            if not tab_eU_percent.isnull().values[j] :
    #                sample_list[i]['eU_' + str(j)] = float(tab_eU_percent[j].values)

    
    return tab_init_resample, tab_resample, sample_list

def draw_main_figure(displayer_figure, 
                sample_list, color_list, info_list,
                tabl_tT_history, tabl_grid_history, distrib_envelopp, grid_info,
                tabl_He_like, tabl_He_post, tabl_He_expect,
                tabl_FT_like, tabl_FT_post, tabl_FT_expect,
                tabl_LFT,
                tabl_tT_pred, tabl_tT_pred_vertical, tabl_constrain,
                *,
                save_format= '', auto_save_path = True, time_min=-1, time_max=0, temp_min=-1, temp_max=0,
                chemin = 'all', colormap = 'viridis_r', classement='Likelihood', hist_color = "Likelihood",
                model = "Max Likelihood", gradiant = 30, niveau ="Epoch", vertical_profile = "no"):

    plotter.plot_iteration(displayer_figure, tabl_tT_history, info_list)
    plotter.plot_pred_ages(displayer_figure, tabl_He_like, tabl_He_post, tabl_He_expect,
                   tabl_FT_like, tabl_FT_post, tabl_FT_expect,
                   color_list, model=model)
    plotter.plot_LFT(displayer_figure, tabl_LFT, color_list, model=model)
    plotter.plot_histoire(displayer_figure, tabl_tT_history, tabl_tT_pred, tabl_tT_pred_vertical, tabl_constrain, classement=classement, color=hist_color,
                  history=chemin, gradiant=gradiant, time_min=time_min, time_max=time_max, temp_min=temp_min, temp_max=temp_max,
                  colormap=colormap, vertical_profile=vertical_profile, data_stat=tabl_grid_history, enveloppe=distrib_envelopp, grid_info = grid_info)
    plotter.plot_time_scale(displayer_figure, tabl_tT_history, niveau=niveau, time_min=time_min, time_max=time_max, temp_min=temp_min, temp_max=temp_max)
    plotter.plot_info(displayer_figure, info_list)
    plotter.add_legende(displayer_figure, sample_list, color_list)
    displayer_figure.canvas.draw()

def draw_resample_figure(resample_figure,
                         tab_init_resample, tab_resample, sample_list, color_list):
    plotter.plot_resample(resample_figure, tab_init_resample, tab_resample, sample_list, color_list)
    
def export_figures(main_canvas, displayer_figure, filepath, save_format, auto_save_path, *,
                   resample_figure=''):
    main_canvas.setFixedWidth(1680)
    main_canvas.setFixedHeight(500)
    savers.save_QTQt_fig(displayer_figure, filepath, save_format, autopath=auto_save_path)
    if not isinstance(resample_figure, str):
        savers.save_QTQt_fig(resample_figure, filepath + "_resample", save_format, autopath=auto_save_path)

def export_age(data:RInversion(), *, filepath=None):
    # Initialisation de tableaux vides en cas de données manquantes
    export_tab_He = DataFrame()
    export_tab_FT = DataFrame()
    if not filepath : filepath = savers.get_path(extension='xlsx')

    # Vérification de tabl_He_like
    if data.tabl_He_like.ndim > 0:
        n_elements_He = data.tabl_He_like[:, :, 2].stack(stacked_dim=('echantillon', 'Y')).size
        export_tab_He = {
            "sample": data.tabl_He_like[:, :, 8].stack(stacked_dim=('echantillon', 'Y')),
            "type": ["He"] * n_elements_He,
            "crystal": data.tabl_He_like[:, :, 9].stack(stacked_dim=('echantillon', 'Y')),
            "Rs [µm]": data.tabl_He_like[:, :, 4].stack(stacked_dim=('echantillon', 'Y')),
            "obs. ages [Ma]": data.tabl_He_like[:, :, 2].stack(stacked_dim=('echantillon', 'Y')),
            "obs. error [Ma]": data.tabl_He_like[:, :, 3].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - ages [Ma]": data.tabl_He_like[:, :, 0].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - error [Ma]": data.tabl_He_like[:, :, 1].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - ages [Ma]": data.tabl_He_post[:, :, 0].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - error [Ma]": data.tabl_He_post[:, :, 1].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - ages [Ma]": data.tabl_He_expect[:, :, 0].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - error [Ma]": data.tabl_He_expect[:, :, 1].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - Tc cross [Ma]": data.tabl_He_like[:, :, 5].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - Tc cross [Ma]": data.tabl_He_post[:, :, 5].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - Tc cross [Ma]": data.tabl_He_expect[:, :, 5].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - eU [ppm]": data.tabl_He_like[:, :, 6].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - eU [ppm]": data.tabl_He_post[:, :, 6].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - eU [ppm]": data.tabl_He_expect[:, :, 6].stack(stacked_dim=('echantillon', 'Y')),
        }
        export_tab_He = DataFrame(export_tab_He)

    # Vérification de tabl_FT_like
    if data.tabl_FT_like.ndim > 0:
        n_elements_FT = data.tabl_FT_like[:, :, 4].stack(stacked_dim=('echantillon', 'Y')).size
        export_tab_FT = {
            "sample": data.tabl_FT_like[:, :, 4].stack(stacked_dim=('echantillon', 'Y')),
            "type": ["FT"] * n_elements_FT,
            "obs. ages [Ma]": data.tabl_FT_like[:, :, 1].stack(stacked_dim=('echantillon', 'Y')),
            "obs. error [Ma]": data.tabl_FT_like[:, :, 2].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - ages [Ma]": data.tabl_FT_like[:, :, 0].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - error [Ma]": data.tabl_FT_like[:, :, 3].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - ages [Ma]": data.tabl_FT_post[:, :, 0].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - error [Ma]": data.tabl_FT_post[:, :, 3].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - ages [Ma]": data.tabl_FT_expect[:, :, 0].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - error [Ma]": data.tabl_FT_expect[:, :, 3].stack(stacked_dim=('echantillon', 'Y')),
            "obs kin. par.": data.tabl_FT_like[:, :, 8].stack(stacked_dim=('echantillon', 'Y')),
            "obs kin. par. error.": data.tabl_FT_like[:, :, 9].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - kin. par.": data.tabl_FT_like[:, :, 6].stack(stacked_dim=('echantillon', 'Y')),
            "Max Like - kin. par. error": data.tabl_FT_like[:, :, 7].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - kin. par.": data.tabl_FT_post[:, :, 6].stack(stacked_dim=('echantillon', 'Y')),
            "Max Post - kin. par. error": data.tabl_FT_post[:, :, 7].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - kin. par.": data.tabl_FT_expect[:, :, 6].stack(stacked_dim=('echantillon', 'Y')),
            "Expect - kin. par. error": data.tabl_FT_expect[:, :, 7].stack(stacked_dim=('echantillon', 'Y')),
        }
        export_tab_FT = DataFrame(export_tab_FT)

    # Concaténation si les deux tables ont été correctement générées
    export_tab = concat([export_tab_He, export_tab_FT], ignore_index=True)

    # Remplacement des valeurs
    if not export_tab.empty:
        export_tab['crystal'] = export_tab['crystal'].replace("0", "ap.").replace("1", "zr.").replace("2", "other")
        export_tab['sample'] = export_tab['sample'].replace("Max-Like", "")
        export_tab.replace("nan", NaT, inplace=True)
        export_tab = export_tab[export_tab['obs. ages [Ma]'].notna() & (export_tab['obs. ages [Ma]'] != '')]
        
        _, file_extension = path.splitext(filepath)
        if file_extension == ".xlsx":
            export_tab.to_excel(filepath, index=False, header=True)
        elif file_extension == ".csv":
            export_tab.to_csv(filepath, index=False, header=True)
    
def export_length(data:RInversion(), *, filepath=None):
    if not filepath : filepath = savers.get_path(extension='xlsx, csv')
    
    export_tab_LFT = {"sample" : data.tabl_LFT[:,:,5].stack(stacked_dim=('echantillon','Y')),
                      "length [µm]" : data.tabl_LFT[:,:,0].stack(stacked_dim=('echantillon','Y')),
                      "observed FTL [µm]" : data.tabl_LFT[:,:,1].stack(stacked_dim=('echantillon','Y')),
                      "Max Like predicted FTL [µm]" : data.tabl_LFT[:,:,2].stack(stacked_dim=('echantillon','Y')),
                      "Max Post predicted FTL[µm]" : data.tabl_LFT[:,:,3].stack(stacked_dim=('echantillon','Y')),
                      "Expected predicted FTL[µm]" : data.tabl_LFT[:,:,3].stack(stacked_dim=('echantillon','Y')),
                     }
    export_tab = DataFrame(export_tab_LFT)

    if not export_tab.empty:
        export_tab["sample"] = export_tab["sample"].str.replace("<built-in function empty>", "nan")
        export_tab.replace("nan", NaT, inplace=True)
        export_tab.dropna(how='all', inplace=True)
        
        _, file_extension = path.splitext(filepath)
        if file_extension == ".xlsx":
            export_tab.to_excel(filepath, index=False, header=True)
        elif file_extension == ".csv":
            export_tab.to_csv(filepath, index=False, header=True)
        