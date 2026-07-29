# IMPORT LIBRARY

#basic librairy
import numpy

#for plotting 
from matplotlib.ticker import FuncFormatter, MultipleLocator
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Patch
from matplotlib.colors import LinearSegmentedColormap, to_rgba

from scipy.interpolate import UnivariateSpline
from pyrolite.util.time import Timescale

#internal lib
from . import utils


# === FIG : plot_iteration === plot_iteration(data_tT):

def plot_iteration(plot_list, data_tT, info_list):
    
    # == detail graph ==
    plot_like = plot_list[0]
    plot_post = plot_list[1]
    
    # === graphique du like ===
    plot_like.clear()
    x= data_tT[:,0,3]
    y= data_tT[:,1,3]
    plot_like.plot(x, y, color='red', linewidth = 0.5)
    
    # === graphique du Post ===
    plot_post.clear()
    x= data_tT[:,0,3]
    y_bis= data_tT[:,2,3]
    plot_post.plot(x, y_bis, color='blue', linewidth = 0.5)

    # Defining the label
    
    
    plot_like.set_xlabel('Exploration info.' + ' (' + utils.val_to_time_str(info_list['time total']) +')')
    plot_like.xaxis.set_label_position('top') 
    
    y_min, y_max = plot_post.get_ylim()
    x_min, x_max = plot_post.get_xlim()
    
    plot_like.xaxis.set_major_formatter(FuncFormatter(lambda x, p: '{:,}'.format(int(x)).replace(",", " ")))

    plot_like.set_ylabel('likelihood')
    plot_like.yaxis.set_label_position('right')
    plot_post.set_ylabel('posterior')
    plot_post.yaxis.set_label_position('right') 
    
def layout_iteration(plot_list):
    
    # == detail graph ==
    plot_like = plot_list[0]
    plot_post = plot_list[1]
    
    plot_like.set_xlabel('Exploration info.' + ' (total time)')
    
    plot_like.set_ylabel('likelihood', style='italic', color= 'red')
    plot_like.xaxis.set_label_position('top') 
    plot_like.yaxis.set_label_position('right') 
    plot_like.tick_params(labelbottom=False, labeltop=True, labelleft=True, labelright=False)
    plot_like.tick_params(axis='x', labelrotation=20)
    plot_like.xaxis.set_major_formatter(FuncFormatter(lambda x, p: '{:,}'.format(int(x)).replace(",", " ")))

    # suppr border
    plot_like.spines['bottom'].set_visible(False)

    plot_like.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,top=True ,bottom=True  )
    plot_like.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,top=True ,bottom=True  )

    plot_like.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,left=True ,right=False  )
    plot_like.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,left=True ,right=False  )
    
    # Defining the label
    plot_post.tick_params(labelbottom=False, labeltop=False, labelleft=True, labelright=False )
    # Defining the label
    plot_post.set_ylabel('posterior', style='italic', color= 'blue')
    plot_post.yaxis.set_label_position('right') 
    plot_post.spines['bottom'].set_visible(True)
    plot_post.spines['top'].set_visible(False)
    
    plot_post.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,bottom=True ,top=False  )
    plot_post.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelsize='10' ,labelcolor='black' ,bottom=True ,top=False  )

    plot_post.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,left=True ,right=False  )
    plot_post.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,left=True ,right=False  )



# === FIG : plot_pred_ages(data_He, data_FT) ===

def plot_pred_ages(plot_age, 
                   tabl_He_like, tabl_He_post, tabl_He_expect, 
                   tabl_FT_like, tabl_FT_post, tabl_FT_expect, 
                   sample_list,*, model='like'):
    
    plot_age.clear()
    
    if 'Post' in model:
        data_He = tabl_He_post
        data_FT = tabl_FT_post
        #txt_info = 'max posterior'
    elif 'Expect' in model:
        data_He = tabl_He_expect
        data_FT = tabl_FT_expect
        #txt_info = 'expected'
    elif 'Like' in model:
        data_He = tabl_He_like
        data_FT = tabl_FT_like
        #txt_info = 'max likelihood'
        
    #plot the He data
    if len(data_He) !=0 :
        for i in range(data_He.shape[0]):
            x = data_He[i,:,2].astype(dtype=float)
            dx = data_He[i,:,3].astype(dtype=float)
            y = data_He[i,:,0].astype(dtype=float)
            dy = data_He[i,:,1].astype(dtype=float)
            nom = data_He[i,0,8].values
            
            for j in range(len(x)):  #obligation d'itération pour le cas où des cristaux sont différents
                crystal_num = data_He[i,j,9].astype(dtype=float)
                if crystal_num==0 : #apatite
                    crystal_type = "o"
                elif crystal_num==1 : #zircon
                    crystal_type = "D" 
                elif crystal_num==2 : #other
                    crystal_type = "v"
                else:
                    crystal_type = ","#pixel
                
                plot_age.scatter(x[j] , y[j], s=30,
                                 color=sample_list.get_color_by_name(nom),
                                 marker=crystal_type,
                                 label=nom,
                                 linewidths=0.5,
                                 edgecolors = "black",
                                 alpha=0.50)
                plot_age.errorbar(x[j] , y[j], xerr=dx[j], yerr=dy[j],
                                       fmt=crystal_type,
                                       markersize=0,
                                       ecolor=sample_list.get_color_by_name(nom))
    
    #plot the FT data
    if len(data_FT) !=0 :
        for i in range(data_FT.shape[0]):
            x = data_FT[i,0,1].astype(dtype=float)
            y = data_FT[i,0,0].astype(dtype=float)
            dx = data_FT[i,0,3].astype(dtype=float)
            dy = data_FT[i,0,2].astype(dtype=float)
            nom = data_FT[i,0,4].values
            plot_age.scatter(x , y, s=30,
                             color=sample_list.get_color_by_name(nom),
                             marker="s",
                             label=nom,
                             linewidths=0.5,
                             edgecolors = "black",
                             alpha=0.50)
            plot_age.errorbar(x , y, xerr=dx, yerr=dy, fmt="s", markersize=0, ecolor=sample_list.get_color_by_name(nom))

    # Layout mandatory
    y_min, y_max = plot_age.get_ylim()
    x_min, x_max = plot_age.get_xlim()
    
    #plot_age.text(x_max*1.15, (y_max-y_min)/2+y_min, 'prediction : ' + txt_info, style='italic', rotation='vertical',verticalalignment='center')
    
    y_min = y_min * 0.9
    y_max = y_max * 1.1
    x_min = x_min * 0.9
    x_max = x_max * 1.1
    
    plot_age.set_xlim(left=x_min, right=x_max)
    plot_age.set_ylim(bottom=y_min, top=y_max)

    major, minor = utils.get_scale(x_max - x_min)
    plot_age.xaxis.set_major_locator(MultipleLocator(major))
    plot_age.xaxis.set_minor_locator(MultipleLocator(minor))
    plot_age.yaxis.set_major_locator(MultipleLocator(major))
    plot_age.yaxis.set_minor_locator(MultipleLocator(minor))
    
    plot_age.axline((0, 0), slope=1, linewidth=0.5, color='black', alpha = 0.75, linestyle='--')  
    
    legend_elements = [Line2D([0], [0], marker='o', label='AHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='D', label='ZHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='v', label='He', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='s', label='FT', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5)
                      ]
    plot_age.legend(handles=legend_elements, ncol=2, bbox_to_anchor=(0, 1), fontsize='x-small')
    plot_age.set_xlabel('Obs. ages [Ma]')
    plot_age.set_ylabel('Pred. ages [Ma]')
    
def layout_pred_ages(plot_age):
    
    plot_age.axline((0, 0), slope=1, linewidth=0.5, color='black', alpha = 0.75, linestyle='--')  
    
    legend_elements = [Line2D([0], [0], marker='o', label='AHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='D', label='ZHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='v', label='He', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='s', label='FT', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5)
                      ]
    plot_age.legend(handles=legend_elements, ncol=2, bbox_to_anchor=(0, 1), fontsize='x-small')

    plot_age.set_xlabel('Obs. ages [Ma]')
    plot_age.set_ylabel('Pred. ages [Ma]')
    plot_age.xaxis.set_label_position('bottom') 
    plot_age.yaxis.set_label_position('left') 

    plot_age.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,bottom=True ,top=True  )
    plot_age.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,bottom=True ,top=True  )
    plot_age.xaxis.set_major_formatter('{x:.0f}')
    
    plot_age.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,left=True ,right=True  )
    plot_age.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,left=True ,right=True  )
    plot_age.yaxis.set_major_formatter('{x:.0f}')


# === FIG : plot_LFT(data_LFT, data_FT) === note : bar position on QTQt are not the same ansd can note be reproduce simply....

def plot_LFT(plot_list, data_LFT, sample_list, *, model='Like'):
    
    # == detail graph ==
    plot_FT = plot_list[0]
    plot_FT_bis = plot_list[1]
    
    plot_FT.clear()
    plot_FT_bis.clear()
    
    if 'Like' in model:
        data_type = 2
    elif 'Post' in model:
        data_type = 3
    elif 'Expect' in model:
        data_type = 4
    
    #gestion de la largeur et transparence des barres
    nb_LFT = 0
    for n in range(data_LFT.shape[0]):
        if numpy.nansum(data_LFT[n,:,1].astype(dtype=float)) > 0:
            nb_LFT=nb_LFT+1
    
    width = 0.8
    if nb_LFT == 1 :
        alpha_FT = 0.5
    else:
        alpha_FT = 0.1
    
    #ajout des barre (stacker les une sur les autres pour plus de lisibilité)
    for n in range(data_LFT.shape[0]):
        if numpy.nansum(data_LFT[n,:,1].astype(dtype=float)) > 0:
            #nb_LFT_bis = nb_LFT_bis+1
            x = data_LFT[n,:,0].astype(dtype=float)
            y_curve = data_LFT[n,:,data_type].astype(dtype=float)
            y_bar = data_LFT[n,:,1].astype(dtype=float)
            
            nom = data_LFT[n,0,5]
            color = sample_list.get_color_by_name(nom)
            
            color = to_rgba(color)[:3] # recuperation du rgb
            
            plot_FT.bar(x - 0.5, y_bar, width=width, align='center', facecolor=(*color, alpha_FT), edgecolor=(*color, 1.0), linewidth=1)
            plot_FT_bis.plot(x, y_curve, color=sample_list.get_color_by_name(nom), linewidth=3, alpha=1)

    y_min, y_max = plot_FT.get_ylim()
    major, minor = utils.get_scale((y_max - y_min))
    plot_FT.yaxis.set_major_locator(MultipleLocator(major))
    plot_FT.yaxis.set_minor_locator(MultipleLocator(minor))
    plot_FT.xaxis.set_major_locator(MultipleLocator(5))
    plot_FT.xaxis.set_minor_locator(MultipleLocator(1))
    
    plot_FT_bis.set_xlim(7, 18)
    plot_FT_bis.set_ylim(ymin=0) 
    plot_FT.set_xlim(6, 19)
    plot_FT.set_xlabel('Tracks length [µm]')
    plot_FT.set_ylabel('nb of tracks')
    
    legend_elements = [Line2D([0], [0], marker='s', label='obs.', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([], [], color='gray', label="pred.", linestyle='solid', linewidth= 1.5),
                      ]
    plot_FT.legend(handles=legend_elements, ncol=1, bbox_to_anchor=(0, 1), fontsize='x-small')

    
def layout_LFT(plot_list):
    
    # == detail graph ==
    plot_FT = plot_list[0]
    plot_FT_bis = plot_list[1]

    plot_FT_bis.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, bottom=False, top=False, left=False, right=False)
    plot_FT_bis.spines['right'].set_visible(False)
    plot_FT_bis.spines['bottom'].set_visible(False)
    plot_FT_bis.spines['top'].set_visible(False)
    plot_FT_bis.spines['left'].set_visible(False)
    
    plot_FT_bis.set_xlim(7, 18)
    plot_FT_bis.set_ylim(ymin=0)        
    plot_FT.set_xlim(6, 19)
    
    legend_elements = [Line2D([0], [0], marker='s', label='obs.', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([], [], color='gray', label="pred.", linestyle='solid', linewidth= 1.5),
                      ]
    plot_FT.legend(handles=legend_elements, ncol=1, bbox_to_anchor=(0, 1), fontsize='x-small')
    
    
    plot_FT.set_xlabel('Tracks length [µm]')
    plot_FT.set_ylabel('nb of tracks')
    plot_FT.xaxis.set_label_position('top')
    plot_FT.yaxis.set_label_position('left')
    plot_FT.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False, bottom=True, top=False, left=True, right=False)
    plot_FT.spines['right'].set_visible(False)
    plot_FT.spines['top'].set_visible(False)
    
    plot_FT.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black', labelcolor='black' ,bottom=True ,top=False  )
    plot_FT.xaxis.set_tick_params(which='minor' ,direction='out',length=2 ,width=0.5 ,color='black', labelcolor='black' ,bottom=True ,top=False  )
    plot_FT.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black', labelcolor='black' ,left=True ,right=False  )
    plot_FT.yaxis.set_tick_params(which='minor' ,direction='out',length=2 ,width=0.5 ,color='black', labelcolor='black' ,left=True ,right=False  )



# === FIG : plot_histoire(data_tT_plot, data_Chemin_plot, data_Chemin_vertical, data_constrain, *, classement='Max like', gradiant=30, surface_t=10, time_min=-1, time_max=0, temp_min=-10, temp_max=0, constante=[0], vertical_profile=False):
 
def plot_histoire(plot_list, data_tT, data_Chemin_pred, data_constrain, *,
                  data_stat=None, enveloppe="vide", grid_info = [],
                  tqdm_stream='',
                  
                  history='all', color='Max like', classement='Max like', 
                  gradiant=30, surface_t=10, time_min=0, time_max=-1, temp_min=0, temp_max=-1, 
                  predicted_path = ['Max Like', 'Max Post', 'Expected'], main_sample = 0,
                  constante=[0], colormap=[''],
                  
                  parameters=None,
                  ):   
    
    # == detail graph ==
    custom_fig = plot_list[0]
    plot_history = plot_list[1]
    plot_history_bis = plot_list[2]
    plot_hist_legen = plot_list[3]
    
    plot_history.clear()
    plot_history_bis.clear()
    plot_hist_legen.clear()
    
    # == cas du passage d'info par un bibliotheque
    if parameters != None :
        history = parameters['chemin']
        color = parameters['hist_color']
        classement = parameters['classement']
        gradiant = parameters['gradiant']
        time_min = parameters['time_min']
        time_max = parameters['time_max']
        temp_min = parameters['temp_min']
        temp_max = parameters['temp_max']
        predicted_path = parameters['predicted_paths']
        main_sample = parameters['main_sample']
        colormap = parameters['colormap']
        

    x_max=time_max
    x_min=time_min
    y_max=temp_max
    y_min=temp_min
    
    # == Filter the non-used t(T) paths for the predicted vertical
    filters = []
    if "Max Likelihood" in predicted_path:
        filter_like = numpy.where(data_Chemin_pred.loc[:,1,2] == "Max Like")[0]
        filters.append(filter_like)
    if "Max Posterior" in predicted_path:
        filter_post = numpy.where(data_Chemin_pred.loc[:,1,2] == "Max Post")[0]
        filters.append(filter_post)
    if "Max Mode" in predicted_path:
        filter_mode = numpy.where(data_Chemin_pred.loc[:,1,2] == "Max Mode")[0]
        filters.append(filter_mode)
    if "Expected" in predicted_path:
        filter_expect = numpy.where(data_Chemin_pred.loc[:,1,2] == "EXPECTED")[0]
        filters.append(filter_expect)
    # add the envelopp - on garde les matchs
    if history == 'simple':
        filter_envelop = numpy.where(['Envelop' in val  for val in data_Chemin_pred.loc[:, 1, 2].values])[0]
        filters.append(filter_envelop)
    
    # filter if only one sample need
    if str(main_sample).isdigit() :
        #note : dico have an key "name" also
        filter_sample = numpy.where([sample == main_sample for sample in data_Chemin_pred.loc[:, 0, 2].values])[0]
        sample_filter = filter_sample
    
    # Application des filtres OU pour les premiers filtres
    if len(filters) > 0:
        combined_filter = filters[0]
        for filter in filters[1:]:
            combined_filter = numpy.union1d(combined_filter, filter)  # Union (OU)
    else:
        combined_filter = numpy.array([], dtype=int)
    
    # Application du filtre ET pour le sample
    if str(main_sample).isdigit() :
        combined_filter = numpy.intersect1d(combined_filter, sample_filter)  # Intersection (ET)
    data_Chemin_pred_filtered = data_Chemin_pred.sel(Chemin=data_Chemin_pred.Chemin.isin(combined_filter))

    
    # simlificate the data_array for plotting decouper 
    data_Chemin_pred_filtered_clean = data_Chemin_pred_filtered.drop_sel(X=[2])
    data_Chemin_pred_filtered_clean = data_Chemin_pred_filtered_clean.drop_sel(Y=[0])
    data_Chemin_pred_filtered_clean = data_Chemin_pred_filtered_clean.astype(float)

    # == built data for envelopp ploting :
    if history == 'simple':
        all_env_time = {} #X
        all_env_sup = {}  #Y
        all_env_inf = {}  #Y
        all_env_color = {}
        
        mem = ''
        for n in range(data_Chemin_pred_filtered.shape[0]):
            sample = data_Chemin_pred_filtered[n,0,2].values.item() 
            type_info = str(data_Chemin_pred_filtered[n,1,2].values.item())
            
            if sample.id_ != mem :
                mem = sample.id_
                env = 0
            
            if 'Envelop' in type_info :
                env += 1
    
                if env == 1:
                    tempo_time = data_Chemin_pred_filtered[n, :, 0].astype(dtype=float)
                    tempo_temp_sup = data_Chemin_pred_filtered[n, :, 1].astype(dtype=float)
                else:
                    tempo_temp_inf = data_Chemin_pred_filtered[n, :, 1].astype(dtype=float)
                
                    all_env_time[mem] = tempo_time
                    all_env_sup[mem] = tempo_temp_sup
                    all_env_inf[mem] = tempo_temp_inf
                    all_env_color[mem] = sample.color_ 

    
    
    # == Filter data if 'heatmap' represenation rather than 'all'
    if history == "heatmap" and data_stat is not None:
        # Initialisation des structures pour stocker les résultats
        all_X = []
        all_Y = []
        all_Z_masked = []
        max_Y_heatmap = -1
        max_X_heatmap = -1
        
        # Boucle sur tous les échantillons
        for n in range(len(grid_info)):
            # Création de la grille temps/température
            X_Time = numpy.arange(0, grid_info[n]["nb_time"] * grid_info[n]["time_step"],
                              grid_info[n]["time_step"])
            Y_Temp = numpy.linspace(-grid_info[n]["max_tempe"],
                                grid_info[n]["nb_tempe"]-grid_info[n]["max_tempe"],
                                grid_info[n]["nb_tempe"])
            X, Y = numpy.meshgrid(X_Time, Y_Temp)
        
            # Extraction des données pour l'échantillon courant
            Z = data_stat[n, :, :]
        
            # select the sample to display and hide the data near 0
            no_nul_data_stat = Z.where(Z != 0)
            Z_masked = numpy.ma.masked_less(Z, no_nul_data_stat.min())
        
            # Stockage des résultats
            all_X.append(X)
            all_Y.append(Y)
            all_Z_masked.append(Z_masked)
            
            # calculate max for the range (latter min and max)
            valid = ~Z_masked.mask
            max_Y_heatmap = max(max_Y_heatmap, Y_Temp[numpy.where(valid)[0]].max())
            max_X_heatmap = max(max_X_heatmap, X_Time[numpy.where(valid)[1]].max())
            
        
    # == Order t(T) paths if  and color
    if 'all' in history :
        if 'Like' in color:
            a=1
        elif 'Post' in color:
            a=2
        if 'Iter' in classement:
            a=0
            
        if 'downscale' in history:
            data_tT_downscale = utils.tT_downscale(data_tT, y_index=a)
            data_tT_trie = data_tT_downscale.sortby(data_tT[:,a,3])
        else:
            data_tT_trie = data_tT.sortby(data_tT[:,a,3])

        data_color = data_tT_trie[:,a,3]
        # simlificate the data_array for plotting decouper 
        data_tT_plot = data_tT_trie.drop_sel(X=[2,3])
        

    #init min and max :
    if x_max == -1 :
        if 'all' in history :
            x_max = data_tT_plot[:,:,0].max()*1.05
        elif history == 'heatmap':
            x_max = max_X_heatmap*1.05
        else:
            x_max = data_Chemin_pred_filtered_clean[:,:,0].max()*1.05
    if y_max == -1 :
        if 'all' in history :
            y_max = data_tT_plot[:,:,1].max()*1.05
        elif history == 'heatmap':
            y_max = max_Y_heatmap*1.05
        else:
            y_max = data_Chemin_pred_filtered_clean[:,:,1].max()*1.05
    if x_min == -1 : x_min = 0
    if y_min == -1 : y_min = 0
    
    if custom_fig :
        custom_fig.tT_min_time = x_min
        custom_fig.tT_max_time = x_max
        
    # == Paths and legend layout
    #paths 
    if 'all' in history:
        if 'Like' in color:
            text_legend_1 = 't(T) path likelihood'
        elif 'Post' in color:
            text_legend_1 = 't(T) path posterior'
    elif history=='simple':
        text_legend_1 = ''
    elif history=='heatmap':
        text_legend_1 = 'Percent of all paths'
    
    #init cmap for color
    if colormap == 'QTQt_old':
        cmap = LinearSegmentedColormap.from_list("mycmap", ['blue','cyan','lime','yellow','magenta','red'])
    else:
        cmap = colormap

    # == Simple path layout
    chemin_style = ["--" for x in range(data_Chemin_pred_filtered.shape[0])]
    chemin_color = ["black" for x in range(data_Chemin_pred_filtered.shape[0])]
    chemin_width = [1 for x in range(data_Chemin_pred_filtered.shape[0])]

    for n in range(data_Chemin_pred_filtered.shape[0]):
        sample = data_Chemin_pred_filtered[n,0,2].values.item() 
        type_info = str(data_Chemin_pred_filtered[n,1,2].values.item())
        
        if 'max like' in type_info.lower() :
            chemin_style[n]= 'dashed'
            chemin_color[n]= 'blue'
            chemin_width[n]= 1.5
        
        elif 'max post' in type_info.lower():
            chemin_style[n]= 'dashed'
            chemin_color[n]= 'white'
            chemin_width[n]= 1.5
        
        elif 'max mode' in type_info.lower():
            chemin_style[n]= 'dotted'
            chemin_color[n]= 'grey'
            chemin_width[n]= 0.5
        
        elif 'expect' in type_info.lower():
            chemin_style[n]= 'solid'
            chemin_color[n]= sample.color_
            chemin_width[n]= 4
        
        elif 'envelop' in type_info.lower():
            chemin_style[n]= 'dotted'
            chemin_color[n]= sample.color_
            chemin_width[n]= 1.5


    # == Plot exploration t(T) paths 
    if 'all' in history: #all paths
        if isinstance(tqdm_stream, str): #case for no interface
            t_T_path_graph = LineCollection(data_tT_plot,
                                            cmap=cmap,
                                            array=data_color,
                                            linewidths=0.01,
                                            linestyles='solid',
                                            alpha=1)
        else: #connecte to the time interface
            from tqdm import tqdm
            t_T_path_graph = LineCollection(tqdm(data_tT_plot, file=tqdm_stream),
                                            cmap=cmap,
                                            array=data_color,
                                            linewidths=0.01,
                                            linestyles='solid',
                                            alpha=1)
        plot_history.add_collection(t_T_path_graph)
        
        # legende
        plot_hist_legen.set_visible(True)
        legende_1 = custom_fig.colorbar(t_T_path_graph,cax=plot_hist_legen, orientation="vertical", aspect = 40, label=text_legend_1)
        legende_1.ax.tick_params(labelsize='x-small', labelrotation=45)
    
    elif history == 'heatmap':  #add meshgrid and envelopp
        
        #security
        if not str(main_sample).isdigit() : main_sample = 0
    
        #heatmap
        t_T_path_graph = plot_history.contourf(all_X[main_sample], all_Y[main_sample], all_Z_masked[main_sample], 25, cmap=cmap, alpha=1)
        
        #envelop
        for cle, valeur in enveloppe[main_sample].items():
            if "068" in cle : color = "white"
            if "096" in cle : color = "gray"
            if "100" in cle : color = "black"
            #lissage
            spline = UnivariateSpline(all_X[main_sample][0], valeur) 
            y_smooth = spline(all_X[main_sample][0])
            plot_history.plot(all_X[main_sample][0], y_smooth, color = color, linewidth=0.75, alpha=0.75)
        
        #legende
        plot_hist_legen.set_visible(True)
        legende_1 = custom_fig.colorbar(t_T_path_graph, cax=plot_hist_legen, orientation="vertical", aspect = 40, label=text_legend_1)
        legende_1.ax.tick_params(labelsize='x-small', labelrotation=0)
        
    elif history == 'simple': #add envoloppe rather than t(T) paths
        if str(main_sample).isdigit(): # cas one sample to plot 
            plot_history.fill_between(
                all_env_time[main_sample],
                all_env_sup[main_sample],
                all_env_inf[main_sample],
                alpha=0.2,
                color=all_env_color[main_sample]
            )
        else:
            for n in range(len(all_env_time)):
                plot_history.fill_between(
                                        all_env_time[n],all_env_sup[n],all_env_inf[n],
                                        alpha=0.2,
                                        color=all_env_color[n]
                                        )
            
        #legende
        plot_hist_legen.set_visible(False)

    
    # == Plot predicted t(T) paths 
    chemin = LineCollection(data_Chemin_pred_filtered_clean,
                                      colors = chemin_color,
                                      linewidths=2,
                                      linestyles=chemin_style,
                                      alpha=0.75)
    plot_history.add_collection(chemin)


    # === plot the expected path to add another scale (depth) ===
    x = data_Chemin_pred_filtered_clean[0,0].astype(dtype=float)
    y = data_Chemin_pred_filtered_clean[0,1].astype(dtype=float)
    y_bis = numpy.divide(y-surface_t,gradiant)
    plot_history_bis.plot(x, y_bis, color='red', alpha=0) #transparent path    
    
    
    # == additionnale data to plot
    #add the temperature line
    for n in range(len(constante)):
        if constante[n] != 0:
            plot_history.hlines(y=constante[n], xmin=x_min, xmax=x_max, linewidth=0.5,
                                color='black', alpha = 0.5, linestyle='--', zorder=4)

    #add the boxes (exploration box, constrains...)
    for n in range(data_constrain.shape[0]):
        if data_constrain[n,4] == "explo_box":
            color='grey'
            size = 0.5
            tiret = '--'
            fill = False
        elif data_constrain[n,4] == "external_contraint":
            color='black'
            size = 1
            tiret = '-'
            fill = True
        elif data_constrain[n,4] == "sample_contraint":
            color='green'
            size = 1
            tiret = '-'
            fill = True
        time_ori =float(data_constrain[n,0])+float(data_constrain[n,1])
        time_d =float(data_constrain[n,1])*2
        temp_ori =float(data_constrain[n,2])+float(data_constrain[n,3])
        temp_d =float(data_constrain[n,3])*2
        plot_history.add_patch(Rectangle((time_ori,temp_ori), -time_d, -temp_d,
                                         alpha= 0.5, linestyle= tiret, linewidth = size,
                                         edgecolor=color, facecolor='white', fill=fill, zorder=3))
        
    # === Layout updated ==    
    #axes min-max
    plot_history.set_xlim(x_max, x_min)
    plot_history.set_ylim(y_max, y_min)
    
    plot_history_bis.set_xlim(x_max, x_min)
    plot_history_bis.set_ylim((y_max-surface_t)/gradiant, (y_min-surface_t)/gradiant)
    
    #axes name
    plot_history.set_ylabel('Temperature [°C]')
    
    plot_history_bis.set_ylabel('Depth [km] (' + str(gradiant) + '°/km)' )
    plot_history_bis.spines['left'].set_position(('outward',50))
    
    #axes markers
    time_major, time_minor = utils.get_scale(x_max - x_min)
    tempe_major, tempe_minor = utils.get_scale(y_max - y_min)   
    plot_history.xaxis.set_major_locator(MultipleLocator(time_major))
    plot_history.xaxis.set_minor_locator(MultipleLocator(time_minor))
    plot_history.yaxis.set_major_locator(MultipleLocator(tempe_major))
    plot_history.yaxis.set_minor_locator(MultipleLocator(tempe_minor))
    
    depth_major, depth_minor = utils.get_scale((y_max-surface_t)/gradiant - (y_min-surface_t)/gradiant)
    plot_history_bis.yaxis.set_major_locator(MultipleLocator(depth_major))
    plot_history_bis.yaxis.set_minor_locator(MultipleLocator(depth_minor))
    
    #layers position
    plot_history.patch.set_alpha(0)
    plot_history.patch.set_visible(False)
    legend_elements = [Patch(facecolor='white', edgecolor='grey',alpha= 1, linestyle= '--', linewidth = 0.5, label="exploration box"),
                       Patch(facecolor='white', edgecolor='black',alpha= 1, linestyle= '-', linewidth = 1, label="constrain box"),
                       Line2D([], [], color='black', linestyle='solid', linewidth= 3, label="expected path"),
                      ]
    if history != 'heatmap':
        pos_y = 0.27
        legend_elements.append(Line2D([], [], color='blue', linestyle='dashed', linewidth= 1.5, label="max likelihood path"))
        legend_elements.append(Line2D([], [], color='grey', linestyle='dashed', linewidth= 1.5, label="max posterior path"))
        legend_elements.append(Line2D([], [], color='black', linestyle='dotted', linewidth= 1.5, label="96% envelop (all paths)"))   
    else:
        pos_y = 0.27
        legend_elements.append(Line2D([], [], color='white', linestyle='solid', linewidth= 1.5, label="68% envelopp"))
        legend_elements.append(Line2D([], [], color='gray', linestyle='solid', linewidth= 1.5, label="96% envelopp"))
        legend_elements.append(Line2D([], [], color='black', linestyle='solid', linewidth= 1.5, label="99% envelopp"))
    plot_history.legend(handles=legend_elements, ncol=1, fontsize='x-small', bbox_to_anchor=(0.80, pos_y))
    
    
def layout_history(plot_list):
    
    # == detail graph ==
    custom_fig = plot_list[0]
    plot_history = plot_list[1]
    plot_history_bis = plot_list[2]
    plot_hist_legen = plot_list[3]
    
    # == init legend ==
    plot_hist_legen.set_visible(False)
    # legende_1 = custom_fig.colorbar(t_T_path_graph, cax=plot_hist_legen, orientation="vertical", aspect = 40, label=text_legend_1)
    # legende_1.ax.tick_params(labelsize='x-small', labelrotation=0)
    
    
    # === add the légende ===  
    legend_elements = [Patch(facecolor='white', edgecolor='grey',alpha= 1, linestyle= '--', linewidth = 0.5, label="exploration box"),
                       Patch(facecolor='white', edgecolor='black',alpha= 1, linestyle= '-', linewidth = 1, label="constrain box"),
                       Line2D([], [], color='black', linestyle='solid', linewidth= 3, label="expected path"),
                       Line2D([], [], color='blue', linestyle='dashed', linewidth= 1.5, label="max likelihood path"),
                       Line2D([], [], color='grey', linestyle='dashed', linewidth= 1.5, label="max posterior path"),
                       Line2D([], [], color='black', linestyle='dotted', linewidth= 1.5, label="96% envelop (all paths)"),
                      ]
    plot_history.legend(handles=legend_elements, ncol=1, fontsize='x-small', bbox_to_anchor=(0.82, 0.27))

    #Defining the label
    plot_history.set_ylabel('Temperature [°C]')
    plot_history.yaxis.label.set_color('darkred')
    plot_history.yaxis.set_label_position('left') 
    plot_history.tick_params(labelbottom=False, labeltop=False, labelleft=True, labelright=False, bottom=False, top=True, left=True, right=False)
    
    plot_history_bis.set_ylabel('Depth [km] (30°/km)' )
    plot_history_bis.yaxis.label.set_color('darkgreen')
    plot_history_bis.yaxis.set_label_position('left')    
    plot_history_bis.tick_params(labelleft=True, labelright=False,left=True, right=False)
    plot_history_bis.spines['left'].set_position(('outward',50))
    
    #suppr border
    plot_history.spines['right'].set_visible(False)
    plot_history.spines['bottom'].set_visible(False)
    plot_history.spines['top'].set_visible(False)
    plot_history.spines['left'].set_color('darkred')
    
    plot_history_bis.spines['right'].set_visible(False)
    plot_history_bis.spines['bottom'].set_visible(False)
    plot_history_bis.spines['top'].set_visible(False)
    plot_history_bis.spines['left'].set_color('darkgreen')
    
    #axes marker
    plot_history.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,
                                       color='black' ,labelcolor='black' ,
                                       bottom=False ,top=True)
    plot_history.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,
                                       color='black' ,labelcolor='black' ,
                                       bottom=False ,top=True  )
    plot_history.xaxis.set_major_formatter('{x:.0f}')
    plot_history.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,
                                       color='darkred' ,labelcolor='darkred' ,
                                       left=True ,right=False  )
    plot_history.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,
                                       color='darkred' ,labelcolor='darkred' ,
                                       left=True ,right=False  )
    plot_history.yaxis.set_major_formatter('{x:.0f}')
    
    plot_history_bis.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,
                                           color='darkgreen' ,labelcolor='darkgreen' ,
                                           left=True ,right=False  )
    plot_history_bis.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,
                                           color='darkgreen' ,labelcolor='darkgreen' ,
                                           left=True ,right=False  )
    plot_history_bis.yaxis.set_major_formatter('{x:.0f}')
    
    #change the z position to get the temperature on the Qt graph
    plot_history.patch.set_alpha(0)
    plot_history.set_zorder(plot_history_bis.get_zorder()+1)
    plot_history.patch.set_visible(False)
    

# === FIG : plot_time_scale(*, niveau='Epoch', data_tT, **,time_min=-1, time_max=0, temp_min=-1, temp_max=0): ===
#['Eon', 'Era', 'Period', 'Superepoch', 'Epoch', 'Age']

def plot_time_scale(plot_timescale, *, niveau='Epoch', time_min=-1, time_max=-1):
    
    plot_timescale.clear()
    
    for ix, level in enumerate(Timescale().levels):
        if level == niveau:
            stage = Timescale().data.loc[Timescale().data.Level == level, :]
            for pix, period in stage.iterrows():
                plot_timescale.barh(ix,
                                    period.Start - period.End,
                                    facecolor=period.Color,
                                    left=period.End,
                                    height=0.8,
                                    edgecolor="grey",
                                    linewidth=0.5
                                    )

    x_max=time_max
    x_min=time_min
    
    if x_min == -1 : x_min = 0
    if x_max == -1 : x_max = 10
    
    major, minor = utils.get_scale(x_max - x_min)
    
    # plot_timescale.set_xlim(x_max, x_min)
    plot_timescale.xaxis.set_major_locator(MultipleLocator(major))
    plot_timescale.xaxis.set_minor_locator(MultipleLocator(minor))
    plot_timescale.set_xlabel('Time [Ma]')
    plot_timescale.xaxis.set_label_position('top')
    
def layout_time_scale(plot_timescale):
    plot_timescale.set_xlabel('Time [Ma]')
    plot_timescale.xaxis.set_label_position('top')
    plot_timescale.tick_params(labelbottom=False, labeltop=True, labelleft=False, labelright=False, bottom=True, top=True, left=False, right=False)
    plot_timescale.spines['left'].set_visible(False)
    plot_timescale.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black', labelcolor='black' ,bottom=True ,top=True  )
    plot_timescale.xaxis.set_tick_params(which='minor' ,direction='out',length=2 ,width=0.5 ,color='black', labelcolor='black' ,bottom=True ,top=True  )
    plot_timescale.xaxis.set_major_formatter('{x:.0f}')



# === FIG : plot_info(info_list)

def add_hist_information(plot_hist_parameters, parameters): 
        
    #built the legend data
    legend_str=[
        #column :
        'Acceptance :',
        'point birth = ' + utils.val_to_str(parameters['Acceptance Birth'],sufixe='%'),
        'point death = ' + utils.val_to_str(parameters['Acceptance Death'],sufixe='%'),
        '',
        '',
            
        #column 1:
        't(T) point move :',
        'time = ' + utils.val_to_str(parameters['time gaussian'],sufixe='Ma', remplacement='no') + ' ' + utils.val_to_str(parameters['Acceptance time'],prefixe='(',sufixe='%)'),
        'temp. = ' +  utils.val_to_str(parameters['temperature gaussian'], sufixe='°C', remplacement='no') + ' ' +  utils.val_to_str(parameters['Acceptance temperature'], prefixe='(', sufixe='%)'),
        'offset = ' +  utils.val_to_str(parameters['offset gaussian'], sufixe='°/km', remplacement='no') + ' ' +   utils.val_to_str(parameters['Acceptance offset'], prefixe='(', sufixe='%)'),
        '',
        
        #column 2:
        'Error resample :',
        'FT = ' +  utils.val_to_str(parameters['FT resample'], sufixe='%', remplacement='no') + ' ' +  utils.val_to_str(parameters['Acceptance FT'],prefixe='(',sufixe='%)'),
        'He = ' +  utils.val_to_str(parameters['He resample'], sufixe='%', remplacement='no') + ' ' +  utils.val_to_str(parameters['Acceptance He'],prefixe='(',sufixe='%)'),
        'VR = ' +  utils.val_to_str(parameters['VR resample'], sufixe='%', remplacement='no') + ' ' +  utils.val_to_str(parameters['Acceptance VR'],prefixe='(',sufixe='%)'),
        '',
        
        #column 3:
        'Exploration param. :',
        'keep complex histories = ' + str(parameters['Keep complex history']), 
        'resample outside of prior = ' + str(parameters['Gaussian exploration']),
        'dT/dt limite = ' +  utils.val_to_str(parameters['Max allowable dTdt'],sufixe='°/Ma', remplacement='no', test = 1000),
        'paths keep = 1 over ' + str(parameters['Thinning']),
        
        #column 4:
        'Calculation param. :',
        'diffusion (ap.-oth.) = ' + utils.val_to_str(parameters['Temperature steps diffusion Ap'], sufixe='°C') + ' - ' + utils.val_to_str(parameters['Temperature steps diffusion Other'], sufixe='°C'),
        'annealing (ap.-oth.) = ' + utils.val_to_str(parameters['Temperature steps radi dam Ap'], sufixe='°C') + ' - ' + utils.val_to_str(parameters['Temperature steps radi dam Other'], sufixe='°C'),
        'FT adapatative timestep = ' + str(parameters['Adaptive time step']),
        '',
        ]
    
    #convert to legend elements 
    legend_elements = []
    for i in range(len(legend_str)):
        legend_elements.append(Line2D([],[],color='none',label=legend_str[i]))
        
    leg = plot_hist_parameters.legend(
        handles=legend_elements,
        #loc='upper left',
        bbox_to_anchor=(0.1, 0.8),
        ncol=5,
        edgecolor="steelblue",
        facecolor='whitesmoke',
        handlelength=0,
        handletextpad=0,
        borderaxespad=0,
        alignment='center',
        fontsize='medium',
        frameon=True,
        )
    #self.plot_hist_parameters.patch.set_alpha(0.5)
    
    
    #font parameters legend elements   
    for t in leg.get_texts():
        txt = t.get_text()
        fsize = t.get_fontsize()
        t.set_fontsize(fsize-1)
        
        if ":" in txt:
            t.set_fontweight("bold")
    
        if "no" in txt:
            t.set_fontstyle("italic")
            t.set_color("grey")


def add_plotted_information(plot_plot_parameters, inversion_param):
    
    #built the legend data
    legend_str=[
            #column :
            'Plotted options :',
            'predicted data = ' + str(inversion_param['model'])
            ]
    
    if inversion_param['chemin'] == "heatmap":
        legend_str.append(
            't(T) representation = paths heatmap'
            )
    elif inversion_param['chemin'] == "simple":
         legend_str.append(
             't(T) representation = paths envelop'
             )
    elif inversion_param['chemin'] == "all":
        legend_str.append(
            't(T) coloration = ' + str(inversion_param['hist_color'])
            )
        legend_str.append(
            'paths z order = ' + str(inversion_param['classement'])
            )
    
    #convert to legend elements 
    legend_elements = []
    for i in range(len(legend_str)):
        legend_elements.append(Line2D([],[],color='none',label=legend_str[i]))
        
    leg = plot_plot_parameters.legend(
        handles=legend_elements,
        #loc='center',
        bbox_to_anchor=(1, 0.5),
        ncol=1,
        #edgecolor="white",
        #facecolor='white',
        handlelength=0,
        handletextpad=0,
        borderaxespad=0,
        #alignment='center',
        fontsize='large',
        frameon=False,
        )
    
    #font parameters legend elements   
    for t in leg.get_texts():
        txt = t.get_text()
        fsize = t.get_fontsize()
        t.set_fontsize(fsize-1)
        if ":" in txt:
            t.set_fontweight("bold")
        if "=" in txt:
            t.set_fontstyle("italic")

            
# === FIG : plot_legend

def add_samples(plot_samples, sample_list):
        
    legend_elements = []
    
    for sample in sample_list.list_summary_samples():
        nom = sample.name_
        color = sample.color_
        legend_elements.append(Patch(facecolor=color, edgecolor='black', alpha=0.5, label=nom))
    
    plot_samples.legend(
        title='Samples (files) :',
        handles=legend_elements,
        bbox_to_anchor=(-0.2, 0.9),
        ncols=1,
        edgecolor="gray",
        alignment='left'
        )
    plot_samples.patch.set_alpha(0.0)
    
def layout_informations(subplot):
    
    subplot.tick_params(labelleft=False, labelright=False,left=False, right=False,labeltop=False, labelbottom=False,top=False, bottom=False)
    
    subplot.spines['right'].set_visible(False)
    subplot.spines['bottom'].set_visible(False)
    subplot.spines['top'].set_visible(False)
    subplot.spines['left'].set_visible(False)
    
    subplot.patch.set_alpha(0.0)

