# IMPORT LIBRARY

#basic librairy
import numpy
from xarray import DataArray

#for plotting 
from matplotlib.gridspec import GridSpec
from matplotlib.pyplot import figure

from matplotlib.ticker import FuncFormatter, MultipleLocator
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Patch
from matplotlib.colors import LinearSegmentedColormap

from scipy.interpolate import UnivariateSpline
from pyrolite.util.time import Timescale

#internal lib
from . import utils

# == FIG : init ==

def built_fig():
    #init matplotlib fig
    displayer_figure = figure(figsize=(17, 5))
    displayer_figure.tight_layout()
    displayer_figure.subplots_adjust(left=0.04, right=0.96, bottom=0.1, top=0.9)
    
    #figure generale
    QTQt_structure = GridSpec(
        ncols=8,
        width_ratios=[1, 0.2, 1, 0.6, 1, 1, 1, 0.05],
        nrows=5,
        height_ratios=[0.2, 1, 1, 1, 1],
    )
    #add sub plot
    displayer_figure.plot_FT = displayer_figure.add_subplot(QTQt_structure[1:3, 0])
    displayer_figure.plot_FT_bis = displayer_figure.plot_FT.twinx()
    displayer_figure.plot_legend = displayer_figure.add_subplot(QTQt_structure[3:5, 0])
    displayer_figure.plot_like = displayer_figure.add_subplot(QTQt_structure[1, 2])
    displayer_figure.plot_post = displayer_figure.add_subplot(QTQt_structure[2, 2])
    displayer_figure.plot_age = displayer_figure.add_subplot(QTQt_structure[3:, 2])
    displayer_figure.plot_history = displayer_figure.add_subplot(QTQt_structure[1:, 4:7])
    displayer_figure.plot_history_bis = displayer_figure.plot_history.twinx()
    displayer_figure.plot_timescale = displayer_figure.add_subplot(
        QTQt_structure[0, 4:7], sharex=displayer_figure.plot_history
    )
    displayer_figure.plot_hist_legen = displayer_figure.add_subplot(QTQt_structure[1:, 7])
    
    #info de modelisation
    x = 0.505
    y = 0.125
    dx = 0.115
    font_size = 9
    displayer_figure.fond = displayer_figure.patches.extend(
        [
            Rectangle(
                (x - 0.005, y),
                0.44,
                -0.1,
                fill=True,
                color="whitesmoke",
                alpha=1,
                zorder=0,
                transform=displayer_figure.transFigure,
                figure=displayer_figure,
            )
        ]
    )
    displayer_figure.inversion_info_1 = displayer_figure.text(
        x, y - 0.01, "", size=font_size, color="gray", style="italic"
    )
    displayer_figure.inversion_info_2 = displayer_figure.text(
        x + dx * 1, y - 0.01, "", size=font_size, color="tan", style="italic"
    )
    displayer_figure.inversion_info_3 = displayer_figure.text(
        x + dx * 2, y - 0.01, "", size=font_size, color="mediumaquamarine", style="italic"
    )
    displayer_figure.inversion_info_4 = displayer_figure.text(
        x + dx * 3, y - 0.01, "", size=font_size, color="palevioletred", style="italic"
    )
    
    # chart layout
    layout_iteration(displayer_figure)
    layout_pred_ages(displayer_figure)
    layout_LFT(displayer_figure)
    layout_history(displayer_figure)
    layout_time_scale(displayer_figure)
    layout_legend(displayer_figure)
    
    return displayer_figure

def built_resample_fig(*, fig=None, num_graphs=2):  
    if fig :
        fig.set_size_inches(10, num_graphs * 4, forward=True)
    else:
        fig = figure(figsize=(10, num_graphs * 4))
    fig.axs = fig.subplots(num_graphs, 1, sharex=True) 
    return fig

# === FIG : plot_iteration === plot_iteration(data_tT):

def plot_iteration(self, data_tT, info_list):
    # === graphique du like ===
    self.plot_like.clear()
    x= data_tT[:,0,3]
    y= data_tT[:,1,3]
    self.plot_like.plot(x, y, color='red', linewidth = 0.5)
    
    # === graphique du Post ===
    self.plot_post.clear()
    x= data_tT[:,0,3]
    y_bis= data_tT[:,2,3]
    self.plot_post.plot(x, y_bis, color='blue', linewidth = 0.5)

    # Defining the label
    self.plot_like.set_xlabel('Exploration info.' + ' (' + info_list['time total'] +')')
        
    y_min, y_max = self.plot_post.get_ylim()
    x_min, x_max = self.plot_post.get_xlim()
    
    self.plot_like.xaxis.set_major_formatter(FuncFormatter(lambda x, p: '{:,}'.format(int(x)).replace(",", " ")))

    self.plot_like.set_ylabel('likelihood')
    self.plot_post.set_ylabel('posterior')
    
def layout_iteration(self):
    
    self.plot_like.set_xlabel('Exploration info.' + ' (total time)')
    
    self.plot_like.set_ylabel('likelihood', style='italic', color= 'red')
    self.plot_like.xaxis.set_label_position('top') 
    self.plot_like.yaxis.set_label_position('right') 
    self.plot_like.tick_params(labelbottom=False, labeltop=True, labelleft=True, labelright=False)
    self.plot_like.tick_params(axis='x', labelrotation=20)
    self.plot_like.xaxis.set_major_formatter(FuncFormatter(lambda x, p: '{:,}'.format(int(x)).replace(",", " ")))

    # suppr border
    self.plot_like.spines['bottom'].set_visible(False)

    self.plot_like.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,top=True ,bottom=True  )
    self.plot_like.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,top=True ,bottom=True  )

    self.plot_like.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,left=True ,right=False  )
    self.plot_like.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,left=True ,right=False  )
    
    # Defining the label
    self.plot_post.tick_params(labelbottom=False, labeltop=False, labelleft=True, labelright=False )
    # Defining the label
    self.plot_post.set_ylabel('posterior', style='italic', color= 'blue')
    self.plot_post.yaxis.set_label_position('right') 
    self.plot_post.spines['bottom'].set_visible(True)
    self.plot_post.spines['top'].set_visible(False)
    
    self.plot_post.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,bottom=True ,top=False  )
    self.plot_post.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelsize='10' ,labelcolor='black' ,bottom=True ,top=False  )

    self.plot_post.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,left=True ,right=False  )
    self.plot_post.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,left=True ,right=False  )



# === FIG : plot_pred_ages(data_He, data_FT) ===

def plot_pred_ages(self, tabl_He_like, tabl_He_post, tabl_He_expect, tabl_FT_like, tabl_FT_post, tabl_FT_expect, color_list,*, model='like'):
    
    self.plot_age.clear()
    
    if 'Post' in model:
        data_He = tabl_He_post
        data_FT = tabl_FT_post
        txt_info = 'max posterior'
    elif 'Expect' in model:
        data_He = tabl_He_expect
        data_FT = tabl_FT_expect
        txt_info = 'expected'
    elif 'Like' in model:
        data_He = tabl_He_like
        data_FT = tabl_FT_like
        txt_info = 'max likelihood'

    if len(data_He) !=0 :
        for i in range(data_He.shape[0]):
            x = data_He[i,:,2].astype(dtype=float)
            dx = data_He[i,:,3].astype(dtype=float)
            y = data_He[i,:,0].astype(dtype=float)
            dy = data_He[i,:,1].astype(dtype=float)
            nom = data_He[i,0,8].str.replace(".txt","").str.replace("_"," ")
            nom = str(nom.values)
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
                self.plot_age.scatter(x[j] , y[j], s=30,
                                 color=color_list[nom],
                                 marker=crystal_type,
                                 label=nom,
                                 linewidths=0.5,
                                 edgecolors = "black",
                                 alpha=0.50)
                self.plot_age.errorbar(x[j] , y[j], xerr=dx[j], yerr=dy[j],
                                       fmt=crystal_type,
                                       markersize=0,
                                       ecolor=color_list[nom])
    
    if len(data_FT) !=0 :
        for i in range(data_FT.shape[0]):
            x = data_FT[i,0,1].astype(dtype=float)
            y = data_FT[i,0,0].astype(dtype=float)
            dx = data_FT[i,0,3].astype(dtype=float)
            dy = data_FT[i,0,2].astype(dtype=float)
            nom = data_FT[i,0,4].str.replace(".txt","").str.replace("_"," ")
            nom = str(nom.values)
            self.plot_age.scatter(x , y, s=30,
                             color=color_list[nom],
                             marker="s",
                             label=nom,
                             linewidths=0.5,
                             edgecolors = "black",
                             alpha=0.50)
            self.plot_age.errorbar(x , y, xerr=dx, yerr=dy, fmt="s", markersize=0, ecolor=color_list[nom])

    # Layout mandatory
    y_min, y_max = self.plot_age.get_ylim()
    x_min, x_max = self.plot_age.get_xlim()
    
    self.plot_age.text(x_max*1.15, (y_max-y_min)/2+y_min, 'prediction : ' + txt_info, style='italic', rotation='vertical',verticalalignment='center')
    
    y_min = y_min * 0.9
    y_max = y_max * 1.1
    x_min = x_min * 0.9
    x_max = x_max * 1.1
    
    self.plot_age.set_xlim(left=x_min, right=x_max)
    self.plot_age.set_ylim(bottom=y_min, top=y_max)

    major, minor = utils.get_scale(x_max - x_min)
    self.plot_age.xaxis.set_major_locator(MultipleLocator(major))
    self.plot_age.xaxis.set_minor_locator(MultipleLocator(minor))
    self.plot_age.yaxis.set_major_locator(MultipleLocator(major))
    self.plot_age.yaxis.set_minor_locator(MultipleLocator(minor))
    
    self.plot_age.axline((0, 0), slope=1, linewidth=0.5, color='black', alpha = 0.75, linestyle='--')  
    
    legend_elements = [Line2D([0], [0], marker='o', label='AHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='D', label='ZHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='v', label='He', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='s', label='FT', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5)
                      ]
    self.plot_age.legend(handles=legend_elements, ncol=2, bbox_to_anchor=(0, 1), fontsize='x-small')
    self.plot_age.set_xlabel('Obs. ages [Ma]')
    self.plot_age.set_ylabel('Pred. ages [Ma]')
    
def layout_pred_ages(self):
    
    self.plot_age.axline((0, 0), slope=1, linewidth=0.5, color='black', alpha = 0.75, linestyle='--')  
    
    legend_elements = [Line2D([0], [0], marker='o', label='AHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='D', label='ZHe', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='v', label='He', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([0], [0], marker='s', label='FT', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5)
                      ]
    self.plot_age.legend(handles=legend_elements, ncol=2, bbox_to_anchor=(0, 1), fontsize='x-small')

    self.plot_age.set_xlabel('Obs. ages [Ma]')
    self.plot_age.set_ylabel('Pred. ages [Ma]')
    self.plot_age.xaxis.set_label_position('bottom') 
    self.plot_age.yaxis.set_label_position('left') 

    self.plot_age.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,bottom=True ,top=True  )
    self.plot_age.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,bottom=True ,top=True  )
    self.plot_age.xaxis.set_major_formatter('{x:.0f}')
    
    self.plot_age.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black' ,labelcolor='black' ,left=True ,right=True  )
    self.plot_age.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,color='black' ,labelcolor='black' ,left=True ,right=True  )
    self.plot_age.yaxis.set_major_formatter('{x:.0f}')


# === FIG : plot_LFT(data_LFT, data_FT) === note : bar position on QTQt are not the same ansd can note be reproduce simply....

def plot_LFT(self, data_LFT, color_list, *, model='Like'):
    
    self.plot_FT.clear()
    self.plot_FT_bis.clear()
    
    if 'Like' in model:
        data_type = 2
    elif 'Post' in model:
        data_type = 3
    elif 'Expect' in model:
        data_type = 4
    
    #gestion de la largeur des barres
    nb_LFT = 0
    for n in range(data_LFT.shape[0]):
        if numpy.nansum(data_LFT[n,:,1].astype(dtype=float)) > 0:
            nb_LFT=nb_LFT+1
            width = 0.8/nb_LFT
    
    nb_LFT_bis = 0
    for n in range(data_LFT.shape[0]):
        if numpy.nansum(data_LFT[n,:,1].astype(dtype=float)) > 0:
            nb_LFT_bis = nb_LFT_bis+1
            x = data_LFT[n,:,0].astype(dtype=float)
            y_curve = data_LFT[n,:,data_type].astype(dtype=float)
            y_bar = data_LFT[n,:,1].astype(dtype=float)
            nom = data_LFT[n,0,5]
            nom = str(nom.values).replace(".txt","").replace("_"," ").replace("(","").replace(")","")
            width_mod = (nb_LFT_bis - nb_LFT / 2) * width - width / 2
            self.plot_FT.bar(x+(width_mod), y_bar, width=width, color=color_list[nom], edgecolor="black", linewidth=0.5, alpha=0.5)
            self.plot_FT_bis.plot(x, y_curve, color=color_list[nom], linewidth=3, alpha=1)

    y_min, y_max = self.plot_FT.get_ylim()
    major, minor = utils.get_scale((y_max - y_min))
    self.plot_FT.yaxis.set_major_locator(MultipleLocator(major))
    self.plot_FT.yaxis.set_minor_locator(MultipleLocator(minor))
    self.plot_FT.xaxis.set_major_locator(MultipleLocator(5))
    self.plot_FT.xaxis.set_minor_locator(MultipleLocator(1))
    
    self.plot_FT_bis.set_xlim(7, 18)
    self.plot_FT_bis.set_ylim(ymin=0) 
    self.plot_FT.set_xlim(6, 19)
    self.plot_FT.set_xlabel('Tracks length [µm]')
    self.plot_FT.set_ylabel('nb of tracks')
    
    legend_elements = [Line2D([0], [0], marker='s', label='obs.', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([], [], color='gray', label="pred.", linestyle='solid', linewidth= 1.5),
                      ]
    self.plot_FT.legend(handles=legend_elements, ncol=1, bbox_to_anchor=(0, 1), fontsize='x-small')

    
def layout_LFT(self):
    self.plot_FT_bis.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, bottom=False, top=False, left=False, right=False)
    self.plot_FT_bis.spines['right'].set_visible(False)
    self.plot_FT_bis.spines['bottom'].set_visible(False)
    self.plot_FT_bis.spines['top'].set_visible(False)
    self.plot_FT_bis.spines['left'].set_visible(False)
    
    self.plot_FT_bis.set_xlim(7, 18)
    self.plot_FT_bis.set_ylim(ymin=0)        
    self.plot_FT.set_xlim(6, 19)
    
    legend_elements = [Line2D([0], [0], marker='s', label='obs.', markeredgecolor='gray',markerfacecolor='w', color='w', markersize=5),
                       Line2D([], [], color='gray', label="pred.", linestyle='solid', linewidth= 1.5),
                      ]
    self.plot_FT.legend(handles=legend_elements, ncol=1, bbox_to_anchor=(0, 1), fontsize='x-small')
    
    
    self.plot_FT.set_xlabel('Tracks length [µm]')
    self.plot_FT.set_ylabel('nb of tracks')
    self.plot_FT.xaxis.set_label_position('top')
    self.plot_FT.yaxis.set_label_position('left')
    self.plot_FT.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False, bottom=True, top=False, left=True, right=False)
    self.plot_FT.spines['right'].set_visible(False)
    self.plot_FT.spines['top'].set_visible(False)
    
    self.plot_FT.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black', labelcolor='black' ,bottom=True ,top=False  )
    self.plot_FT.xaxis.set_tick_params(which='minor' ,direction='out',length=2 ,width=0.5 ,color='black', labelcolor='black' ,bottom=True ,top=False  )
    self.plot_FT.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black', labelcolor='black' ,left=True ,right=False  )
    self.plot_FT.yaxis.set_tick_params(which='minor' ,direction='out',length=2 ,width=0.5 ,color='black', labelcolor='black' ,left=True ,right=False  )



# === FIG : plot_histoire(data_tT_plot, data_Chemin_plot, data_Chemin_vertical, data_constrain, *, classement='Max like', gradiant=30, surface_t=10, time_min=-1, time_max=0, temp_min=-10, temp_max=0, constante=[0], vertical_profile=False):
 

def plot_histoire(self, data_tT, data_Chemin, data_Chemin_vertical, data_constrain, *, 
                  history='all', color='Max like', classement='Max like', 
                  gradiant=30, surface_t=10, time_min=-1, time_max=0, temp_min=-10, temp_max=0, 
                  constante=[0], colormap=[''], vertical_profile='no',
                  data_stat="vide", enveloppe="vide", grid_info = [],
                  tqdm_stream=''
                  ):   

    self.plot_history.clear()
    self.plot_history_bis.clear()
    self.plot_hist_legen.clear()

    x_max=time_max
    x_min=time_min
    y_max=temp_max
    y_min=temp_min
    
    #filter the non-used t(T) paths for the predicted vertical
    if vertical_profile == "Max Likelihood":
        filter_vertical = numpy.where((data_Chemin_vertical.loc[:,1,2] != "Max Like"))[0]
        vertical_color = "blue"
        vertical_marker = "dashed"
    elif vertical_profile == "Max Posterior": 
        filter_vertical = numpy.where((data_Chemin_vertical.loc[:,1,2] != "Max Post"))[0]
        vertical_color = "grey"
        vertical_marker = "dashed"
    elif vertical_profile == "Expected": 
        filter_vertical = numpy.where((data_Chemin_vertical.loc[:,1,2] != "EXPECTED"))[0]
        vertical_color = "black"
        vertical_marker = "solid"
    else:
        filter_vertical = numpy.where((data_Chemin_vertical.loc[:,1,2] != "EXPECTED"))[0]
    data_Chemin_vertical = data_Chemin_vertical.sel(Chemin=~data_Chemin_vertical.Chemin.isin(filter_vertical))
    
    #prep data if stat rather than all
    if isinstance(data_stat, str):
        Z_masked = ""
    else:
        # create the meshgrid for the t(T) file
        X_Time = numpy.arange(0, grid_info[0] * grid_info[1], grid_info[1])
        Y_Temp = numpy.linspace(-grid_info[3],grid_info[2]-grid_info[3], grid_info[2])
        X, Y = numpy.meshgrid(X_Time, Y_Temp)
        # select the sample to display and hide the data near 0
        Z = data_stat[0,:,:]
        no_nul_data_stat = data_stat.where(data_stat != 0)
        Z_masked = numpy.ma.masked_less(Z, no_nul_data_stat.min())

    
    # legende
    if history=='all':
        if 'Like' in color:
            text_legend_1 = 't(T) path likelihood'
        elif 'Post' in color:
            text_legend_1 = 't(T) path posterior'
    elif history=='simple':
        text_legend_1 = ''
    elif history=='heatmap':
        text_legend_1 = 'Percent of all paths'
    
    # fonction de couleur et classement   
    if 'Like' in color:
        a=1
    elif 'Post' in color:
        a=2
    data_tT_trie = data_tT.sortby(data_tT[:,a,3])
    data_color = data_tT_trie[:,a,3]
    if 'Iter' in classement:
        a=0
    data_tT_trie = data_tT.sortby(data_tT[:,a,3])
    
    #creation de la cmap
    if colormap == 'QTQt_old':
        cmap = LinearSegmentedColormap.from_list("mycmap", ['blue','cyan','lime','yellow','magenta','red'])
    else:
        cmap = colormap

    #decouper les donnee en forme 
    data_tT_plot = data_tT_trie.drop_sel(X=[2,3])
    data_Chemin_plot = data_Chemin.drop_sel(X=[2])
    data_Chemin_vertical_plot = data_Chemin_vertical.drop_sel(X=[2])
    data_Chemin_vertical_plot = data_Chemin_vertical_plot.astype(float)

    #def des min et max
    if x_max == 0 : x_max = data_tT_plot[:,:,0].max()*1.05
    if y_max == 0 : y_max = data_tT_plot[:,:,1].max()*1.05
    if vertical_profile != 'no' :
        y_max_vertical = data_Chemin_vertical_plot[:,:,1].max()*1.05
        if y_max_vertical > y_max: y_max = y_max_vertical

    #def la mise en page des chemins
    chemin_style = ["--" for x in range(data_Chemin.shape[0])]
    chemin_color = ["black" for x in range(data_Chemin.shape[0])]
    chemin_width = [1 for x in range(data_Chemin.shape[0])]

    chemin_envelop = DataArray(
        data=[[numpy.nan for i in range(3)] for j in range(data_Chemin.shape[1])],
        coords={'X': range(3), 'Y': range(data_Chemin.shape[1])},
        dims=('Y', 'X')
        )
    env=1
    for n in range(data_Chemin.shape[0]):
        if data_Chemin[n,0,2] == 'Max likelihood':
            chemin_style[n]= 'dashed'
            chemin_color[n]= 'blue'
            chemin_width[n]= 1.5
        elif data_Chemin[n,0,2] == 'Max posterior':
            chemin_style[n]= 'dashed'
            chemin_color[n]= 'white'
            chemin_width[n]= 1.5
        elif data_Chemin[n,0,2] == 'Expected model':
            chemin_style[n]= 'solid'
            chemin_color[n]= 'black'
            chemin_width[n]= 4
            n_expect = n
        elif data_Chemin[n,0,2] == 'Max mode model':
            chemin_style[n]= 'dotted'
            chemin_color[n]= 'grey'
            chemin_width[n]= 0.5
        elif 'Envelope ' in str(data_Chemin[n,0,2]):
            chemin_style[n]= 'dotted'
            chemin_color[n]= 'black'
            chemin_width[n]= 1.5
            chemin_envelop[:,0]=data_Chemin[n,:,0]
            chemin_envelop[:,env]=data_Chemin[n,:,1]
            env = env + 1

    #add t(T) paths as LineCollection (go faster for lot of paths)
    if history=='all':
        if isinstance(tqdm_stream, str):
            t_T_path_graph = LineCollection(data_tT_plot,
                                            cmap=cmap,
                                            array=data_color,
                                            linewidths=0.01,
                                            linestyles='solid',
                                            alpha=1)
        else:
            from tqdm import tqdm
            t_T_path_graph = LineCollection(tqdm(data_tT_plot, file=tqdm_stream),
                                            cmap=cmap,
                                            array=data_color,
                                            linewidths=0.01,
                                            linestyles='solid',
                                            alpha=1)
        self.plot_history.add_collection(t_T_path_graph)
        # == legende ===
        self.plot_hist_legen.set_visible(True)
        legende_1 = self.figure.colorbar(t_T_path_graph,cax=self.plot_hist_legen, orientation="vertical", aspect = 40, label=text_legend_1)
        legende_1.ax.tick_params(labelsize='x-small', labelrotation=45)
        #add predicted paths
        chemin = LineCollection(data_Chemin_plot,
                                  colors = chemin_color,
                                  linewidths=chemin_width,
                                  linestyles=chemin_style,
                                  alpha=0.75)
        self.plot_history.add_collection(chemin)
    
    #add envoloppe rather than t(T) paths
    elif history == 'simple': 
        self.plot_history.fill_between(chemin_envelop[:,0], chemin_envelop[:,1],chemin_envelop[:,2], alpha=0.2, color= "grey")
        self.plot_hist_legen.set_visible(False)
        #add predicted paths
        chemin = LineCollection(data_Chemin_plot,
                                  colors = chemin_color,
                                  linewidths=chemin_width,
                                  linestyles=chemin_style,
                                  alpha=0.75)
        self.plot_history.add_collection(chemin)
        
    #add meshgrid and envelopp
    elif history == 'heatmap': 
        # Créez une figure
        t_T_path_graph = self.plot_history.contourf(X, Y, Z_masked, 25, cmap=cmap, alpha=1)
        self.plot_hist_legen.set_visible(True)
        legende_1 = self.figure.colorbar(t_T_path_graph, cax=self.plot_hist_legen, orientation="vertical", aspect = 40, label=text_legend_1)
        legende_1.ax.tick_params(labelsize='x-small', labelrotation=0)
        for cle, valeur in enveloppe.items():
            if "068" in cle : color = "white"
            if "096" in cle : color = "gray"
            if "100" in cle : color = "black"
            #lissage
            spline = UnivariateSpline(X_Time, valeur) 
            y_smooth = spline(X_Time)
            self.plot_history.plot(X_Time, y_smooth, color = color, linewidth=0.75, alpha=0.75)
        #add only the expected path
        self.plot_history.plot(data_Chemin_plot[n_expect,:,0].astype(dtype=float), data_Chemin_plot[n_expect,:,1].astype(dtype=float),   
                                  color = chemin_color[n_expect],
                                  linewidth=2,
                                  linestyle=chemin_style[n_expect],
                                  alpha=0.75)
    
    #add vertical paths
    if vertical_profile != 'no' :
        chemin_vertical = LineCollection(data_Chemin_vertical_plot,
                                          colors = vertical_color,
                                          linewidths=1.5,
                                          linestyles=vertical_marker,
                                          alpha=0.75)
        self.plot_history.add_collection(chemin_vertical)


    #add the temperature line
    for n in range(len(constante)):
        if constante[n] != 0:
            self.plot_history.hlines(y=constante[n], xmin=x_min, xmax=x_max, linewidth=0.5,
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
        self.plot_history.add_patch(Rectangle((time_ori,temp_ori), -time_d, -temp_d,
                                         alpha= 0.5, linestyle= tiret, linewidth = size,
                                         edgecolor=color, facecolor='white', fill=fill, zorder=3))
    
    
    # === plot the expected path to add another scale (depth) ===
    x = data_Chemin_plot[2,:,0].astype(dtype=float)
    y = data_Chemin_plot[2,:,1].astype(dtype=float)
    y_bis = numpy.divide(y-surface_t,gradiant)
    self.plot_history_bis.plot(x, y_bis, color='red', alpha=0) #transparent path
    
    # === Layout updated ==    
    #axes min-max
    self.plot_history.set_xlim(x_max, x_min)
    self.plot_history.set_ylim(y_max, y_min)
    
    self.plot_history_bis.set_ylim((y_max-surface_t)/gradiant, (y_min-surface_t)/gradiant)
    
    #axes name
    self.plot_history.set_ylabel('Temperature [°C]')
    
    self.plot_history_bis.set_ylabel('Depth [km] (' + str(gradiant) + '°/km)' )
    self.plot_history_bis.spines['left'].set_position(('outward',50))
    
    #axes markers
    time_major, time_minor = utils.get_scale(x_max - x_min)
    tempe_major, tempe_minor = utils.get_scale(y_max - y_min)   
    self.plot_history.xaxis.set_major_locator(MultipleLocator(time_major))
    self.plot_history.xaxis.set_minor_locator(MultipleLocator(time_minor))
    self.plot_history.yaxis.set_major_locator(MultipleLocator(tempe_major))
    self.plot_history.yaxis.set_minor_locator(MultipleLocator(tempe_minor))
    
    depth_major, depth_minor = utils.get_scale((y_max-surface_t)/gradiant - (y_min-surface_t)/gradiant)
    self.plot_history_bis.yaxis.set_major_locator(MultipleLocator(depth_major))
    self.plot_history_bis.yaxis.set_minor_locator(MultipleLocator(depth_minor))
    
    #layers position
    self.plot_history.patch.set_alpha(0)
    self.plot_history.patch.set_visible(False)
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
    self.plot_history.legend(handles=legend_elements, ncol=1, fontsize='x-small', bbox_to_anchor=(0.80, pos_y))
    
def layout_history(self):
    
    # === add the légende ===  
    legend_elements = [Patch(facecolor='white', edgecolor='grey',alpha= 1, linestyle= '--', linewidth = 0.5, label="exploration box"),
                       Patch(facecolor='white', edgecolor='black',alpha= 1, linestyle= '-', linewidth = 1, label="constrain box"),
                       Line2D([], [], color='black', linestyle='solid', linewidth= 3, label="expected path"),
                       Line2D([], [], color='blue', linestyle='dashed', linewidth= 1.5, label="max likelihood path"),
                       Line2D([], [], color='grey', linestyle='dashed', linewidth= 1.5, label="max posterior path"),
                       Line2D([], [], color='black', linestyle='dotted', linewidth= 1.5, label="96% envelop (all paths)"),
                      ]
    self.plot_history.legend(handles=legend_elements, ncol=1, fontsize='x-small', bbox_to_anchor=(0.82, 0.27))

    #Defining the label
    self.plot_history.set_ylabel('Temperature [°C]')
    self.plot_history.yaxis.label.set_color('darkred')
    self.plot_history.yaxis.set_label_position('left') 
    self.plot_history.tick_params(labelbottom=False, labeltop=False, labelleft=True, labelright=False, bottom=False, top=True, left=True, right=False)
    
    self.plot_history_bis.set_ylabel('Depth [km] (30°/km)' )
    self.plot_history_bis.yaxis.label.set_color('darkgreen')
    self.plot_history_bis.yaxis.set_label_position('left')    
    self.plot_history_bis.tick_params(labelleft=True, labelright=False,left=True, right=False)
    self.plot_history_bis.spines['left'].set_position(('outward',50))
    
    #suppr border
    self.plot_history.spines['right'].set_visible(False)
    self.plot_history.spines['bottom'].set_visible(False)
    self.plot_history.spines['top'].set_visible(False)
    self.plot_history.spines['left'].set_color('darkred')
    
    self.plot_history_bis.spines['right'].set_visible(False)
    self.plot_history_bis.spines['bottom'].set_visible(False)
    self.plot_history_bis.spines['top'].set_visible(False)
    self.plot_history_bis.spines['left'].set_color('darkgreen')
    
    #axes marker
    self.plot_history.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,
                                       color='black' ,labelcolor='black' ,
                                       bottom=False ,top=True)
    self.plot_history.xaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,
                                       color='black' ,labelcolor='black' ,
                                       bottom=False ,top=True  )
    self.plot_history.xaxis.set_major_formatter('{x:.0f}')
    self.plot_history.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,
                                       color='darkred' ,labelcolor='darkred' ,
                                       left=True ,right=False  )
    self.plot_history.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,
                                       color='darkred' ,labelcolor='darkred' ,
                                       left=True ,right=False  )
    self.plot_history.yaxis.set_major_formatter('{x:.0f}')
    
    self.plot_history_bis.yaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,
                                           color='darkgreen' ,labelcolor='darkgreen' ,
                                           left=True ,right=False  )
    self.plot_history_bis.yaxis.set_tick_params(which='minor' ,direction='in',length=2 ,width=0.5 ,
                                           color='darkgreen' ,labelcolor='darkgreen' ,
                                           left=True ,right=False  )
    self.plot_history_bis.yaxis.set_major_formatter('{x:.0f}')
    
    #change the z position to get the temperature on the Qt graph
    self.plot_history.patch.set_alpha(0)
    self.plot_history.set_zorder(self.plot_history_bis.get_zorder()+1)
    self.plot_history.patch.set_visible(False)
    



# === FIG : plot_time_scale(*, niveau='Epoch', data_tT, **,time_min=-1, time_max=0, temp_min=-1, temp_max=0): ===
#['Eon', 'Era', 'Period', 'Superepoch', 'Epoch', 'Age']

def plot_time_scale(self, data_tT, *, niveau='Epoch', time_min=-1, time_max=0, temp_min=-1, temp_max=0):
    
    self.plot_timescale.clear()
    
    for ix, level in enumerate(Timescale().levels):
        if level == niveau:
            stage = Timescale().data.loc[Timescale().data.Level == level, :]
            for pix, period in stage.iterrows():
                self.plot_timescale.barh(ix,
                                    period.Start - period.End,
                                    facecolor=period.Color,
                                    left=period.End,
                                    height=0.8,
                                    edgecolor="grey",
                                    linewidth=0.5
                                    )

    x_max=time_max
    x_min=time_min
    y_max=temp_max
    y_min=temp_min
    if x_max == 0 : x_max = data_tT[:,:,0].max()*1.05
    if y_max == 0 : y_max = data_tT[:,:,1].max()*1.05
    major, minor = utils.get_scale(x_max - x_min)
    
    self.plot_timescale.set_xlim(x_max, x_min)
    self.plot_timescale.xaxis.set_major_locator(MultipleLocator(major))
    self.plot_timescale.xaxis.set_minor_locator(MultipleLocator(minor))
    self.plot_timescale.set_xlabel('Time [Ma]')
    
def layout_time_scale(self):
    self.plot_timescale.set_xlabel('Time [Ma]')
    self.plot_timescale.xaxis.set_label_position('top')
    self.plot_timescale.tick_params(labelbottom=False, labeltop=True, labelleft=False, labelright=False, bottom=True, top=True, left=False, right=False)
    self.plot_timescale.spines['left'].set_visible(False)
    self.plot_timescale.xaxis.set_tick_params(which='major' ,direction='inout',length=5 ,width=1 ,color='black', labelcolor='black' ,bottom=True ,top=True  )
    self.plot_timescale.xaxis.set_tick_params(which='minor' ,direction='out',length=2 ,width=0.5 ,color='black', labelcolor='black' ,bottom=True ,top=True  )
    self.plot_timescale.xaxis.set_major_formatter('{x:.0f}')



# === FIG : plot_info(info_list)

def plot_info(self, info_list):
    self.inversion_info_1.set_text('')
    self.inversion_info_2.set_text('')
    self.inversion_info_3.set_text('')
    self.inversion_info_4.set_text('')
    
    info_column_1 = 'Keep complex histories = ' + str(info_list['Keep complex history']) + '\n' + 'Gaussian exploration = ' + str(info_list['Gaussian exploration']) + '\n' + 't(T) path show = 1/' + str(info_list['Thinning'])
    info_column_2 = 'Time move = ' + str(info_list['time gaussian']) + ' Ma (' + str(info_list['Acceptance time']) + '%) \n' + 'Temp. move = ' + str(info_list['temperature gaussian']) + '°C (' + str(info_list['Acceptance temperature']) + '%) \n' + 'Offset move = ' + str(info_list['offset gaussian']) + ' ' + str(info_list['Acceptance offset'])
    info_column_3 = 'FT resample = ' + str(info_list['FT resample']) + str(info_list['Acceptance FT']) +  '\n' + 'He resample = ' + str(info_list['He resample']) + str(info_list['Acceptance He'])  + '\n' + 'VR resample = ' + str(info_list['VR resample']) + str(info_list['Acceptance Vitr']) 
    info_column_4 = 'Max. rate = ' + str(info_list['Rate tolerance']) + ' °/Ma \n' + 'Diff. step = '+ str(info_list['Temperature steps diffusion Ap']) + '°C / ' + str(info_list['Temperature steps diffusion Other']) + '°C \n Ann. step = ' + str(info_list['Temperature steps radi dam Ap']) + '°C / ' + str(info_list['Temperature steps radi dam Other']) + '°C'
    
    self.inversion_info_1.set_text(info_column_1)
    self.inversion_info_2.set_text(info_column_2)
    self.inversion_info_3.set_text(info_column_3)
    self.inversion_info_4.set_text(info_column_4)



# === FIG : plot_legend

def add_legende(self, sample_list, color_list):
        
    legend_elements = []
    
    for n in sample_list:
        nom = sample_list[n]['name']
        legend_elements.append(Patch(facecolor=color_list[nom], edgecolor='black', alpha=0.5, label=nom))
    
    self.plot_legend.legend(handles=legend_elements, bbox_to_anchor=(-0.2, 1), ncols=1, edgecolor="gray", title='Samples (files) :', alignment='left')
    self.plot_legend.patch.set_alpha(0.0)
    
def layout_legend(self):
    
    self.plot_legend.tick_params(labelleft=False, labelright=False,left=False, right=False,labeltop=False, labelbottom=False,top=False, bottom=False)
    
    self.plot_legend.spines['right'].set_visible(False)
    self.plot_legend.spines['bottom'].set_visible(False)
    self.plot_legend.spines['top'].set_visible(False)
    self.plot_legend.spines['left'].set_visible(False)
    
    self.plot_legend.patch.set_alpha(0.0)


# === FIG : plot_resample ===

def plot_resample(self, data_init, data_resample, sample_list, color_list):
    
    num_sample = data_init.shape[0] 
    linestyles = ['-', '--', '-.', ':', (0, (5, 1)), (0, (3, 5, 1, 5)), (0, (5, 5)), (0, (3, 1, 1, 1)), 
                  (0, (1, 1)), (0, (5, 10))]

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
                self.axs[graph_pos].plot(x, y_bis, linestyle=linestyles[j % len(linestyles)], color=color_list[sample_list[i]['name']])

            # Ajouter des labels et une légende à chaque subplot
            self.axs[graph_pos].set_ylabel(sample_list[i]['name'] + '\neU [ppm]')
    
    num_graphs = graph_pos + 1
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
    
    # Ajuster l'espacement entre les subplots
    #self.fig.tight_layout()



