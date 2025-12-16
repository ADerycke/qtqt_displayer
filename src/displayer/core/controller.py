# qtqt/core/controller.py

"""
Controller
----------
Relie l'UI (MainWindow) avec la logique métier (parser, plotter, exports).
"""

# IMPORT LIBRARY

#basic librairy

#dicuss with the machine
import traceback

#for plotting 
from matplotlib.colors import TABLEAU_COLORS, hex2color
from matplotlib.pyplot import rcParams

#for the Qt window
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QThread, Signal


# === Import logique interne ===
from displayer.ui.main_window import MainWindow, ResampleWindow
from displayer.ui.dialogs import ProgressWindow, ColorSelectionDialog, HelpWindow, ErrorDialog
from displayer.data import parser
from displayer.data.datatypes import RInversion
from displayer.plotting.customfig import InverseFig

from . import savers, workers


class Controller():
    
    def __init__(self, Application:QApplication, parent=None):
        super().__init__()
        
        self.main_application = Application
        self.main_window = MainWindow(self)  
        self.main_window.stop.connect(self.window_quit)
        self.parameters = self.get_inversion_parameters()
        self.process = False
        
        self.tab_sample = {}
        self.color_list = []
        self.invers_data = RInversion()
        self.resample_window = None
        
        #Generate a base color list
        self.tab_color = {}
        n=1
        for i in range(50):
            for item, value in TABLEAU_COLORS.items():
                self.tab_color["sample " + str(n)] = hex2color(value)
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
        
    # --------------------------
    # == Process long (MainProcess)
    # --------------------------    
    def start_process_inverse(self):  
        
        filespaths = savers.get_file()
        if len(filespaths)> 0 :
            self.process = True
            
            self.progress_window = ProgressWindow()
            self.progress_window.stop.connect(self.window_quit)
            self.progress_window.show()
            
            self.resample_window = ResampleWindow()
            self.resample_window.stop.connect(self.window_quit)
            
            self.tqdm_stream = LoadingProcess()
            self.tqdm_stream.progress.connect(self.progress_window.update_sub_progress)
            
            self.process_inverse = InvertProcess(self, filespaths, self.get_inversion_parameters(), self.tab_color)
            self.process_inverse.setObjectName("inverse")
            
            self.process_inverse.progress.connect(self.progress_window.update_progress)
            self.process_inverse.show_wind.connect(self.show_hide_wind)
            
            self.process_inverse.stop.connect(self.window_quit)
            self.process_inverse.send_data.connect(self.get_data)
            self.process_inverse.error.connect(self.error_handler)
            
            self.process_inverse.finished.connect(lambda: self.process_end(self.process_inverse.objectName()))
            self.process_inverse.start()  
        
        else:
            self.main_window.button_process.setDisabled(False)

        
    def get_inversion_parameters(self):
        return self.main_window.send_inversion_parameters()  
    
    def export_data(self, export_type:str):
        if len(self.invers_data.sample_list) > 0:
            filespath = savers.get_path(extension=".xlsx, .csv")
            if len(filespath)> 0 :
                self.process_export = ExportData(self.invers_data, export_type, filespath)
                self.process_export.setObjectName("export")
                self.process_export.finished.connect(lambda: self.process_end(self.process_export.objectName()))
                self.process_export.start() 
    
    def process_end(self, process:str):
        if process == "inverse":
            self.process_inverse.quit()
            self.process_inverse.wait()
            self.tqdm_stream.quit()
            self.tqdm_stream.wait()
            self.progress_window.close()
            self.main_window.button_process.setDisabled(False)
            
            self.process = False
            
        elif process == 'export':
            self.process_export.quit()
            self.process_export.wait()
            QMessageBox.information(None, "Success", "File have been well exported")

    # --------------------------
    # == gestion des fenetres et des retours process
    # --------------------------
    def get_data(self, window_name, data):
        if window_name == "color_picker":
            self.color_list = data
            self.invers_data.color_list = data
        elif window_name == "invers_process":
            self.invers_data.set_data(data)
            self.tab_sample = self.invers_data.sample_list
    
    def show_hide_wind(self, window_name, action):
        if window_name == "progress":
            if action == True :
                self.progress_window.show()
            else :
                self.progress_window.hide()
        elif window_name == "resample":
            if action == True :
                self.resample_window.show()
            else :
                self.resample_window.hide()
        elif window_name == "main":
            if action == True :
                self.main_window.show()
            else :
                self.main_window.hide()        
    
    def window_quit(self, window_name):
        if window_name == "progress":
            self.end_process_inverse()
        if window_name == "invers_process":
            self.end_process_inverse()
        elif window_name == "resample":
            self.resample_window.close()
        elif window_name == "main":
            if self.process == True :
                reply = QMessageBox.question('Confirmation',
                                               'are you sure to stop the process ?',
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.end_process_inverse()
                    self.main_window.close()
                    self.main_application.quit()
            else:
                self.main_window.close()
                self.main_application.quit()
                
    def error_handler(self, origin, stage, traceback):
        print("error at : " + origin + " for the process " + stage)
        error_window = ErrorDialog(origin, stage, traceback)
        error_window.exec_()

    # --------------------------
    # == Fonctions de tracés
    # --------------------------
    
    def re_draw_fig(self, fig_type, fig:InverseFig):
        if len(self.invers_data.sample_list) > 0:
            self.parameters = self.get_inversion_parameters()
            
            if fig_type == "time_scale":
                fig.plot_time_scale(self.invers_data.tabl_tT_history,
                                        niveau=self.parameters['niveau'], time_min=self.parameters['time_min'], time_max=self.parameters['time_max'], temp_min=self.parameters['temp_min'], temp_max=self.parameters['temp_max'])
            
            elif fig_type == "age":
                fig.plot_pred_ages(self.invers_data.tabl_He_like, self.invers_data.tabl_He_post, self.invers_data.tabl_He_expect,
                                       self.invers_data.tabl_FT_like, self.invers_data.tabl_FT_post, self.invers_data.tabl_FT_expect,
                                       self.invers_data.color_list, model=self.parameters['model'])
                fig.plot_LFT(fig, self.invers_data.tabl_LFT, self.invers_data.color_list, model=self.parameters['model'])
            
            elif fig_type == "history":
                
                if "tabl_grid_history" in self.invers_data :
                    fig.plot_histoire(self.invers_data.tabl_tT_history, self.invers_data.tabl_tT_pred, self.invers_data.tabl_tT_pred_vertical, self.invers_data.tabl_constrain,
                                          classement=self.parameters['classement'], color=self.parameters['hist_color'], history=self.parameters['chemin'], gradiant=self.parameters['gradiant'],
                                          time_min=self.parameters['time_min'], time_max=self.parameters['time_max'], temp_min=self.parameters['temp_min'], temp_max=self.parameters['temp_max'],
                                          colormap=self.parameters['colormap'], vertical_profile=self.parameters['vertical_profile'],
                                          data_stat=self.invers_data.tabl_grid_history, enveloppe=self.invers_data.distrib_envelopp,grid_info = self.invers_data.grid_info,
                                          #tqdm_stream=self.tqdm_stream
                                          )
                else:
                    fig.plot_histoire(self.invers_data.tabl_tT_history, self.invers_data.tabl_tT_pred, self.invers_data.tabl_tT_pred_vertical, self.invers_data.tabl_constrain,
                                          classement=self.parameters['classement'], color=self.parameters['hist_color'], history=self.parameters['chemin'], gradiant=self.parameters['gradiant'],
                                          time_min=self.parameters['time_min'], time_max=self.parameters['time_max'], temp_min=self.parameters['temp_min'], temp_max=self.parameters['temp_max'],
                                          colormap=self.parameters['colormap'], vertical_profile=self.parameters['vertical_profile'],
                                          #tqdm_stream=self.tqdm_stream
                                          )
            
    def action_help(self, graph_nom):
        help_window = HelpWindow(graph_nom)
        help_window.exec_()
        
    def action_colors_picker(self):
        color_window = ColorSelectionDialog(self.tab_sample, self.color_list)
        color_window.send_data.connect(self.get_data)
        color_window.exec_()


# THREAD SECONDAIRE et SOUS THREAD

class InvertProcess(QThread):
    progress = Signal(int,int,str,int)
    show_wind = Signal(str,bool)

    stop = Signal(str)
    send_data = Signal(str,object)
    error = Signal(str,str,str)
    
    def __init__(self, main_process, filepaths, parameters, tab_color):
        super().__init__()
        self.main_process = main_process
        #self.tqdm_stream = tqdm_stream
        self.displayer_fig = self.main_process.main_window.displayer_fig
        self.filepaths = filepaths
        self.parameters = parameters
        self.tab_color = tab_color
        self.nb_file_total = len(filepaths)
        self.n_file = 0
        
        self.show_wind.emit('progress',True)
        #window.progress_window.show() # à garder pour une raison inconnue
        self.pourcentage = 0
        self.stage = 'Start'
        
        #memory for available files
        self.file_tto_fix = False
        self.file_Hierachical = False
    
    def send_signal(self, pourcentage, stage): #send a signal to the sub-process (emit function)
        self.pourcentage = pourcentage
        self.stage = stage
        self.progress.emit(self.n_file + 1, self.nb_file_total, stage, pourcentage)
        
    def error_handler(self, stage):
        self.error.emit("process inversion data", stage, traceback.format_exc())
        self.stop.emit("invers_process")
        raise SystemExit 
        
    def run(self):
        for n in range(self.nb_file_total):
            self.n_file = n
            
            #OUVRIR LE FICHIER
            self.send_signal(0, 'reading file')
            try:
                QTQt_summary, QTQt_tto_fix, QTQt_Hierachical = workers.read_QTQt_files(self.filepaths[n])                
            except:
                self.error_handler('open files')
            
            #GET SAMPLES INFORMATION  
            self.send_signal(1, 'samples determination')
            try:
                info_list, sample_list, color_list, tabl_constrain = workers.samples_info(QTQt_summary, self.tab_color)
            except:
                self.error_handler('get samples info')
            
            #GET t(T) HISTORIES 
            self.send_signal(2, 'getting t(T)')
            try :
                tabl_tT_history = parser.extract_tT_history(QTQt_summary)
                #self.tqdm_stream.write(' 50%]')
                #optional files
                if not isinstance(QTQt_tto_fix, str):
                    self.file_tto_fix = True
                    tabl_grid_history, distrib_envelopp, grid_info = parser.extract_grid_history(QTQt_tto_fix)
                if not isinstance(QTQt_Hierachical, str):
                    self.file_Hierachical = True
                    tab_init_resample, tab_resample = parser.extract_resample(QTQt_Hierachical)
                #self.tqdm_stream.write(' 100%]')
            except:
                self.error_handler('get t(T) histories')

            #GET RESULTS
            try :
                self.send_signal(3, 'getting resutls')
                tabl_constrain = parser.extract_constrain(QTQt_summary)
                #self.tqdm_stream.write(' 20%]')
                tabl_tT_pred = parser.extract_tT_pred(QTQt_summary)
                tabl_tT_pred_vertical = parser.extract_tT_pred_vertical(QTQt_summary, sample_list)
                #self.tqdm_stream.write(' 40%]')
                tabl_He_like, tabl_He_post, tabl_He_expect = parser.extract_He_Ages(QTQt_summary)
                #self.tqdm_stream.write(' 60%]')
                tabl_FT_like, tabl_FT_post, tabl_FT_expect = parser.extract_FT_Ages(QTQt_summary)
                #self.tqdm_stream.write(' 80%]')
                tabl_LFT = parser.extract_FT_Length(QTQt_summary)
                #self.tqdm_stream.write('100%]')
            except:
                self.error_handler('get predictions')
            
            #USE RESAMPLE
            try: 
                k = -1
                if self.file_Hierachical:
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
            except:
                self.error_handler('get use resample')
            
            #MAIN FIGURE
            self.send_signal(3, 'drawing iteration')
            try: 
                self.displayer_fig.plot_iteration(tabl_tT_history, info_list)
            except:
                self.error_handler('drawing iteration')
            
            self.send_signal(4, 'drawing predicted ages/LFT')
            try:
                self.displayer_fig.plot_pred_ages(tabl_He_like, tabl_He_post, tabl_He_expect,
                                       tabl_FT_like, tabl_FT_post, tabl_FT_expect,
                                       color_list, model=self.parameters['model'])
            except:
                self.error_handler('drawing predicted ages/LFT')
            
            try:
                self.displayer_fig.plot_LFT(tabl_LFT, color_list, model=self.parameters['model'])
            except:
                self.error_handler('')
            
            
            self.send_signal(5, 'drawing t(T) paths')
            try:
                if self.file_tto_fix:
                    self.displayer_fig.plot_histoire(tabl_tT_history, tabl_tT_pred, tabl_tT_pred_vertical, tabl_constrain,
                                          classement=self.parameters['classement'], color=self.parameters['hist_color'], history=self.parameters['chemin'], gradiant=self.parameters['gradiant'],
                                          time_min=self.parameters['time_min'], time_max=self.parameters['time_max'], temp_min=self.parameters['temp_min'], temp_max=self.parameters['temp_max'],
                                          colormap=self.parameters['colormap'], vertical_profile=self.parameters['vertical_profile'],
                                          data_stat=tabl_grid_history, enveloppe=distrib_envelopp,grid_info = grid_info,
                                          #tqdm_stream=self.tqdm_stream
                                          )
                else:
                    self.displayer_fig.plot_histoire(tabl_tT_history, tabl_tT_pred, tabl_tT_pred_vertical, tabl_constrain,
                                          classement=self.parameters['classement'], color=self.parameters['hist_color'], history=self.parameters['chemin'], gradiant=self.parameters['gradiant'],
                                          time_min=self.parameters['time_min'], time_max=self.parameters['time_max'], temp_min=self.parameters['temp_min'], temp_max=self.parameters['temp_max'],
                                          colormap=self.parameters['colormap'], vertical_profile=self.parameters['vertical_profile'],
                                          #tqdm_stream=self.tqdm_stream
                                          )                      
            except:
                self.error_handler('drawing t(T) paths')
            
            try:
                self.displayer_fig.plot_time_scale(tabl_tT_history,
                                        niveau=self.parameters['niveau'], time_min=self.parameters['time_min'], time_max=self.parameters['time_max'], temp_min=self.parameters['temp_min'], temp_max=self.parameters['temp_max'])
            except:
                self.error_handler('drawing time_scale')
            
            self.send_signal(6, 'writting information')
            try:
                self.displayer_fig.add_information(info_list)
                self.displayer_fig.add_samples(sample_list, color_list)
            except:
                self.error_handler('writting information')
            
            self.send_signal(7, 'generating figure (unknow time...)')
            self.main_process.main_window.canvas.draw()
            
            #DRAW RESAMPLE
            if self.file_Hierachical:
                #rescale figure
                num_graphs = 2
                # compter le nombre d'echantillon avec des data He
                for i in range(tab_init_resample.shape[0] ):
                    if int(tab_init_resample[i, 5]) > 0 : num_graphs = num_graphs + 1      
                self.main_process.resample_window.resample_figure.update_size(num_graphs)
                
                self.main_process.resample_window.resample_figure.plot_resample(tab_init_resample, tab_resample, sample_list, color_list) 
                self.main_process.resample_window.canvas.draw()
                self.show_wind.emit("resample",True)
            else:
                self.stop.emit("resample")
            
            #SAVE FIGURES
            try:
                if self.parameters['fig_format'] != '':
                    inverse_fig, resample_fig, _, _ = savers.get_output_filepath(self.filepaths[n],
                                                                                image_format=self.parameters['fig_format'],
                                                                                table_format=self.parameters['tab_format'],
                                                                                groupe=self.parameters['grp_export'],
                                                                                autopath=self.parameters['auto_save_path'])
                    
                    self.main_process.main_window.displayer_fig.canvas.setFixedWidth(1680)
                    self.main_process.main_window.displayer_fig.canvas.setFixedHeight(500)
                    self.main_process.main_window.displayer_fig.savefig(inverse_fig, bbox_inches='tight')
                    if self.file_Hierachical:
                        self.main_process.resample_window.canvas.setFixedWidth(900)
                        self.main_process.resample_window.canvas.setFixedHeight(150*num_graphs)
                        self.main_process.resample_window.resample_figure.savefig(resample_fig, bbox_inches='tight')
            except:
                self.error_handler('auto save')
            
            #PUT DATA IN MEMORY
            data={'info_list':info_list, 'sample_list':sample_list, 'color_list':color_list,
                'tabl_constrain':tabl_constrain,
                'tabl_tT_history':tabl_tT_history, 'tabl_tT_pred':tabl_tT_pred,'tabl_tT_pred_vertical':tabl_tT_pred_vertical,
                'tabl_He_like':tabl_He_like, 'tabl_He_post':tabl_He_post, 'tabl_He_expect':tabl_He_expect,
                'tabl_FT_like':tabl_FT_like, 'tabl_FT_post':tabl_FT_post, 'tabl_FT_expect':tabl_FT_expect,
                'tabl_LFT':tabl_LFT
                }
            
            if self.file_tto_fix :
                data['tabl_grid_history']=tabl_grid_history
                data['distrib_envelopp']=distrib_envelopp
                data['grid_info']=grid_info
            if self.file_Hierachical :
                data['tab_init_resample']=tab_init_resample
                data['tab_resample']=tab_resample
            
            self.send_data.emit('invers_process', data)
            
            self.send_signal(8, '')
            
            
class ExportData(QThread): 
    def __init__(self, data:RInversion(), export_type:str, filepath):
        super().__init__()
        self.data = data
        self.filepath = filepath
        self.export_type = export_type

    def run(self):
        if self.export_type == "ages" :
            workers.export_age(self.data, filepath=self.filepath)
        elif self.export_type == "lenghts" :
            workers.export_length(self.data, filepath=self.filepath)
        

class LoadingProcess(QThread):
    progress = Signal(int)
    
    def __init__(self, parent=None, gui=True):
        super().__init__(parent)
        self.memoire = ''
    
    def write(self, text):
        if ']' in text:
            self.memoire = self.memoire + text
            index = self.memoire.find('%')
            if '' == self.memoire[index-3:index].strip() : 
                avancement = 0
            else:
                avancement = int(self.memoire[index-3:index].strip())
            self.progress.emit(avancement)
            self.memoire = ''
        else:
            self.memoire = self.memoire + text


