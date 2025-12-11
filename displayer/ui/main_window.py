# qtqt/ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QComboBox, QMenu, QScrollArea
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal

from matplotlib.pyplot import figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt import NavigationToolbar2QT


# === Import logique interne ===
from displayer.plotting.customfig import InverseFig, ResampleFig

# == Class MainWindow ==
class MainWindow(QMainWindow):
    stop = Signal(str)
    
    def __init__(self, controller):
        super().__init__()

        # == Figure initialisation
        self.displayer_fig = figure(FigureClass=InverseFig)
        self.helping_menu_init()

        # == Widgets
        self.widget_creation()
        widget = QWidget()
        window_layout = QHBoxLayout(widget)
        window_layout.addLayout(self.action_layout)
        window_layout.addWidget(self.canvas)
        self.setCentralWidget(widget)

        # == Controller
        self.controller = controller

        # == Configuration fenêtre principale
        self.setWindowTitle("QTQt displayer")
        self.canvas.resize(1680, 500)
        self.resize(1875, 500)

    # --------------------------
    # == Figure et menus
    # --------------------------
    def helping_menu_init(self):
        self.menu_info = QMenu(self)
        self.help_info = self.menu_info.addAction("Help about the informations meaning")
        self.help_info.triggered.connect(lambda: self.action_help("infos"))

        self.menu_like = QMenu(self)
        self.help_like = self.menu_like.addAction("Help about likelihood value")
        self.help_like.triggered.connect(lambda: self.action_help("likelihood"))

        self.menu_post = QMenu(self)
        self.help_post = self.menu_post.addAction("Help about posterior value")
        self.help_post.triggered.connect(lambda: self.action_help("posterior"))

        self.menu_age = QMenu(self)
        self.help_age = self.menu_age.addAction("Help about the meaning of pred. ages")
        self.help_age.triggered.connect(lambda: self.action_help("ages"))
        self.export_age = self.menu_age.addAction("Export data")
        self.export_age.triggered.connect(lambda: self.action_export("ages"))

        self.menu_lft = QMenu(self)
        self.export_lft = self.menu_lft.addAction("Export data")
        self.export_lft.triggered.connect(lambda: self.action_export("lenghts"))

        self.menu_history = QMenu(self)
        self.help_history = self.menu_history.addAction("Help about the history prediction")
        self.help_history.triggered.connect(lambda: self.action_help("history"))


    # --------------------------
    # == Actions principales
    # --------------------------
    def send_inversion_parameters(self):
        inversion_param = {}
        
        inversion_param['auto_save_path'] = self.combobox_savedirect.itemData(self.combobox_savedirect.currentIndex())
        inversion_param['grp_export'] = False
        inversion_param['tab_format'] = '.xlsx'
        inversion_param['fig_format'] = self.combobox_saveformat.itemData(self.combobox_saveformat.currentIndex())


        inversion_param['chemin'] = self.combobox_envelop.itemData(self.combobox_envelop.currentIndex())
        inversion_param['colormap'] = self.combobox_colormap.itemData(self.combobox_colormap.currentIndex())
        inversion_param['classement']=self.combobox_order.currentText()
        inversion_param['hist_color'] = self.combobox_color.currentText()
        inversion_param['model'] = self.combobox_prediction.currentText()
        
        inversion_param['gradiant'] = float(self.editbox_gradient.text())
        
        inversion_param['niveau'] = self.combobox_timescale.currentText()
        
        inversion_param['vertical_profile'] = self.combobox_vertical.currentText()
        
        if self.editbox_minTime.text() != '':
            inversion_param['time_min']=float(self.editbox_minTime.text())
        else:
            inversion_param['time_min']=-1
        if self.editbox_maxTime.text() != '':
            inversion_param['time_max']=float(self.editbox_maxTime.text())
        else:
            inversion_param['time_max']=0
        if self.editbox_minTemp.text() != '':
            inversion_param['temp_min']=float(self.editbox_minTemp.text())
        else:
            inversion_param['temp_min']=-1
        if self.editbox_maxTemp.text() != '':
            inversion_param['temp_max']=float(self.editbox_maxTemp.text())
        else:
            inversion_param['temp_max']=0
        
        return inversion_param


    def on_canvas_click(self, event):
        if event.button == 3:  # clic droit
            if event.inaxes == self.displayer_fig.subplot_age:
                self.menu_age.exec(self.mapToGlobal(event.guiEvent.pos()))
            elif event.inaxes == self.displayer_fig.subplot_FT_bis:
                self.menu_lft.exec(self.mapToGlobal(event.guiEvent.pos()))
            elif event.inaxes == self.displayer_fig.subplot_like:
                self.menu_like.exec(self.mapToGlobal(event.guiEvent.pos()))
            elif event.inaxes == self.displayer_fig.subplot_post:
                self.menu_post.exec(self.mapToGlobal(event.guiEvent.pos()))
            elif event.inaxes == self.subplot_history:
                self.menu_history.exec(self.mapToGlobal(event.guiEvent.pos()))
            elif event.inaxes == self.displayer_fig.subplot_hist_parameters:
                self.menu_info.exec(self.mapToGlobal(event.guiEvent.pos()))

    # --------------------------
    # == Actions button
    # --------------------------
    def action_button_process(self):
        self.button_process.setDisabled(True)
        self.controller.start_process_inverse()
    
    def action_replot_history(self):
        self.controller.re_draw_fig("history", self.displayer_fig)
        self.canvas.draw()

    def action_combo_prediction(self, text):
        self.controller.re_draw_fig("age", self.displayer_fig)
        self.canvas.draw()

    def action_combo_timescale(self, text):
        self.controller.re_draw_fig("time_scale", self.displayer_fig)
        self.canvas.draw()

    def action_button_color(self):
        self.controller.action_colors_picker()
        

    def action_help(self, graph_nom):
        self.controller.action_help(graph_nom)

    def action_export(self, data_type):
        self.controller.export_data(data_type)


    # --------------------------
    # == Widgets
    # --------------------------
    def matplotlib_canvas(self):
        self.canvas = FigureCanvasQTAgg(self.displayer_fig)
        self.addToolBar(NavigationToolbar2QT(self.canvas))
        self.canvas.mpl_connect("button_press_event", self.on_canvas_click)

    def button(self):
        self.button_process = QPushButton("Start")
        self.button_process.clicked.connect(self.action_button_process)
        self.button_color = QPushButton("Select sample(s) color(s)")
        self.button_color.clicked.connect(self.action_button_color)

    def combobox(self):
        self.combobox_saveformat = QComboBox()
        self.combobox_saveformat.addItem("no save","")
        self.combobox_saveformat.addItem("png",".png")
        self.combobox_saveformat.addItem("pdf",".pdf")
        self.combobox_saveformat.addItem("svg",".svg")
        
        self.combobox_savedirect = QComboBox()
        self.combobox_savedirect.addItem("automatic",True)
        self.combobox_savedirect.addItem("manual",False)
        
        self.combobox_envelop = QComboBox()
        self.combobox_envelop.addItem("all t(T) paths", "all")
        self.combobox_envelop.addItem("t(T) paths percentage", "heatmap")
        self.combobox_envelop.addItem("96% envelop", "simple")
        self.combobox_envelop.currentTextChanged.connect(self.action_replot_history)
        
        self.combobox_order = QComboBox()
        self.combobox_order.addItems(["Likelihood", "Posterior", "Iteration"])
        self.combobox_order.currentTextChanged.connect(self.action_replot_history)
        
        self.combobox_color = QComboBox()
        self.combobox_color.addItems(["Likelihood", "Posterior"])
        self.combobox_color.currentTextChanged.connect(self.action_replot_history)
        
        self.combobox_vertical = QComboBox()
        self.combobox_vertical.addItems(["no", "Max Likelihood", "Max Posterior", "Expected"])
        self.combobox_vertical.currentTextChanged.connect(self.action_replot_history)
        
        self.combobox_colormap = QComboBox()
        self.combobox_colormap.addItem("mid value", "viridis_r")
        self.combobox_colormap.addItem("extrem value", "cividis_r")
        self.combobox_colormap.addItem("continue", "jet")
        self.combobox_colormap.addItem("QTQt", "QTQt_old")
        self.combobox_colormap.currentTextChanged.connect(self.action_replot_history)
        
        self.combobox_prediction = QComboBox()
        self.combobox_prediction.addItems(["Max Likelihood", "Max Posterior", "Expected"])
        self.combobox_prediction.currentTextChanged.connect(self.action_combo_prediction)
        
        self.combobox_timescale = QComboBox()
        self.combobox_timescale.addItems(["Epoch", "Eon", "Era", "Period", "Superepoch", "Age"])
        self.combobox_timescale.currentTextChanged.connect(self.action_combo_timescale)

    def editbox(self):
        self.editbox_gradient = QLineEdit()
        self.editbox_gradient.setText("30")
        width = 50
        self.editbox_minTime = QLineEdit(); self.editbox_minTime.setMaximumWidth(width)
        self.editbox_maxTime = QLineEdit(); self.editbox_maxTime.setMaximumWidth(width)
        self.editbox_minTemp = QLineEdit(); self.editbox_minTemp.setMaximumWidth(width)
        self.editbox_maxTemp = QLineEdit(); self.editbox_maxTemp.setMaximumWidth(width)

    def textbox(self):
        font_size = 9
        font_header = QFont("Times", font_size + 2, QFont.Bold)
        font_info = QFont("Times", font_size, italic=True)
        self.header_1 = QLabel("Saving options :"); self.header_1.setFont(font_header)
        self.header_2 = QLabel("t(T) paths options :"); self.header_2.setFont(font_header)
        self.header_3 = QLabel("Other options :"); self.header_3.setFont(font_header)
        self.header_4 = QLabel("Select and process file(s):"); self.header_4.setFont(font_header)
        self.info_10 = QLabel("formats :"); self.info_10.setFont(font_info)
        self.info_11 = QLabel("destination :"); self.info_11.setFont(font_info)
        self.info_20 = QLabel("color range on :"); self.info_20.setFont(font_info)
        self.info_21 = QLabel("order (opt.) :"); self.info_21.setFont(font_info)
        self.info_212 = QLabel("vertical profile :"); self.info_212.setFont(font_info)
        self.info_22 = QLabel("colormap :"); self.info_22.setFont(font_info)
        self.info_23 = QLabel("paths :"); self.info_23.setFont(font_info)
        self.info_3 = QLabel("Results model :"); self.info_3.setFont(font_info)
        self.info_4 = QLabel("Gradient [°/km] :"); self.info_4.setFont(font_info)
        self.info_5 = QLabel("Timescale :"); self.info_5.setFont(font_info)
        self.info_64 = QLabel("Constrain time-temperature plot :"); self.info_64.setFont(font_info)
        self.info_60 = QLabel("min :"); self.info_60.setFont(font_info)
        self.info_61 = QLabel("max :"); self.info_61.setFont(font_info)
        self.info_62 = QLabel("Time :"); self.info_62.setFont(font_info)
        self.info_63 = QLabel("Temperature :"); self.info_63.setFont(font_info)
        self.end = QLabel("")

    def widget_creation(self):
        self.matplotlib_canvas()
        self.button()
        self.combobox()
        self.editbox()
        self.textbox()

        # structuration des widgets pour les actions selon une colonne
        self.action_layout = QVBoxLayout()

        self.action_layout.addWidget(self.header_1)
        split_10 = QHBoxLayout()
        split_10.addWidget(self.info_10)
        split_10.addWidget(self.combobox_saveformat)
        self.action_layout.addLayout(split_10)
        
        split_11 = QHBoxLayout()
        split_11.addWidget(self.info_11)
        split_11.addWidget(self.combobox_savedirect)
        self.action_layout.addLayout(split_11)

        self.action_layout.addWidget(self.header_2)
        split_20 = QHBoxLayout()
        split_20.addWidget(self.info_20)
        split_20.addWidget(self.combobox_color)
        self.action_layout.addLayout(split_20)
        
        split_21 = QHBoxLayout()
        split_21.addWidget(self.info_21)
        split_21.addWidget(self.combobox_order)
        self.action_layout.addLayout(split_21)
        
        split_212 = QHBoxLayout()
        split_212.addWidget(self.info_212)
        split_212.addWidget(self.combobox_vertical)
        self.action_layout.addLayout(split_212)
        
        split_22 = QHBoxLayout()
        split_22.addWidget(self.info_22)
        split_22.addWidget(self.combobox_colormap)
        self.action_layout.addLayout(split_22)
        
        split_3 = QHBoxLayout()
        split_3.addWidget(self.info_23)
        split_3.addWidget(self.combobox_envelop)
        self.action_layout.addLayout(split_3)

        self.action_layout.addWidget(self.header_3)
        
        split_4 = QHBoxLayout()
        split_4.addWidget(self.info_3)
        split_4.addWidget(self.combobox_prediction)
        self.action_layout.addLayout(split_4)
        
        split_5 = QHBoxLayout()
        split_5.addWidget(self.info_5)
        split_5.addWidget(self.combobox_timescale)
        self.action_layout.addLayout(split_5)
        
        split_6 = QHBoxLayout()
        split_6.addWidget(self.info_4)
        split_6.addWidget(self.editbox_gradient)
        self.action_layout.addLayout(split_6)
        
        self.action_layout.addWidget(self.info_64)

        split_7 = QHBoxLayout()
        split_7.addWidget(self.end)
        split_7.addWidget(self.info_60)
        split_7.addWidget(self.info_61)
        self.action_layout.addLayout(split_7)

        split_8 = QHBoxLayout()
        split_8.addWidget(self.info_62)
        split_8.addWidget(self.editbox_minTime)
        split_8.addWidget(self.editbox_maxTime)
        self.action_layout.addLayout(split_8)

        split_9 = QHBoxLayout()
        split_9.addWidget(self.info_63)
        split_9.addWidget(self.editbox_minTemp)
        split_9.addWidget(self.editbox_maxTemp)
        self.action_layout.addLayout(split_9)
        
        self.action_layout.addWidget(self.button_color)
        
        self.action_layout.addWidget(self.end)
        self.action_layout.addWidget(self.end)

        self.action_layout.addWidget(self.header_4)
        self.action_layout.addWidget(self.button_process)

    def closeEvent(self, event):
        self.stop.emit("main")
        event.ignore()

# == Class ResampleWindow ==
class ResampleWindow(QMainWindow):
    stop = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        self.setGeometry(100, 100, 900, 500)  # Position et taille de la fenêtre
        self.setWindowTitle("Results of resampling kinetic parameters")
        
        # Création de la figure de base 
        self.resample_figure = figure(FigureClass=ResampleFig)
        self.canvas = FigureCanvasQTAgg(self.resample_figure)
        self.addToolBar(NavigationToolbar2QT(self.canvas)) # "", self" ? useless ?
        
        # Création du widget central et du layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Création de la zone de défilement
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Définition d'une taille minimum pour le canvas pour garantir le défilement
        self.canvas.setMinimumSize(850, 400)  # Largeur fixe, hauteur augmentée

        # Ajout du canvas à la zone de défilement
        self.scroll_area.setWidget(self.canvas)

        # Ajout de la zone de défilement au layout principal
        layout.addWidget(self.scroll_area)
    
   
    def closeEvent(self, event):
        self.stop.emit("resample")
        event.ignore()
