# IMPORT LIBRARY

#dicuss with the machine
import sys
from os import path
from subprocess import Popen

#for the Qt window
from PySide6.QtWidgets import QApplication, QDialogButtonBox, QDialog, QColorDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QProgressBar
from PySide6.QtGui import QCloseEvent, QColor, QImage, QPixmap
from PySide6.QtCore import Qt, Signal

#for plotting 
from matplotlib.colors import TABLEAU_COLORS, hex2color, to_hex 


# == Class HelpWindows ==
class HelpWindow(QDialog):
        
    def __init__(self, help_case, parent=None):
        super().__init__(parent)
        
        self.racine = path.join(path.dirname(__file__), "ressources")
        self.QTQt_help = "QTQt_User_Guide.pdf"
        
        if help_case == "ages":
            window_title = "How to interprete Ages Obs. vs Ages Pred. ?"
            file_name = "ages_help.txt"
            file_image = "ages_help.png"
            
        elif help_case == "infos":
            window_title = "What does those values mean"
            file_name = "infos_help.txt"
            file_image = ""
        
        elif help_case == "likelihood":
            window_title = "How to interprete the likelihood value"
            file_name = "likelihood_help.txt"
            file_image = "likelihood_help.png"
            
        elif help_case == "posterior":
            window_title = "How to interprete the posterior value"
            file_name = "posterior_help.txt"
            file_image = "posterior_help.png"
        
        elif help_case == "history":
            window_title = "How to look at the t(T) path prediction"
            file_name = "history_help.txt"
            file_image = "history_help.png"

        self.setGeometry(200, 200, 500, 200)
        self.setWindowTitle(window_title)
        
        self.layout = QVBoxLayout(self)
        
        if file_name != "" :
            help_text = self.openTEXT(file_name)
            label_1 = QLabel(help_text, self)
            label_1.setAlignment(Qt.AlignCenter)
            #label_1.setTextFormat(Qt.RichText) #use if it's a HTML layout
            self.layout.addWidget(label_1)
   
        if file_image != "" :
            image = QImage(path.join(self.racine, file_image))
            label_2 = QLabel()
            pixmap = QPixmap.fromImage(image)
            label_2.setPixmap(pixmap)
            self.layout.addWidget(label_2)
        
        #add a button to open the pdf
        open_pdf_button = QPushButton('Open the QTQt User Guide', self)
        open_pdf_button.clicked.connect(self.openPDF)
        
        self.layout.addWidget(open_pdf_button)
        
    def openPDF(self):
        pdf_file = path.join(self.racine, self.QTQt_help)
        try:
            if sys.platform == 'win32':
                Popen(['start', f'{pdf_file}'], shell=True)
            elif sys.platform == 'darwin':
                Popen(['open', f'{pdf_file}'])
            else:
                Popen(['xdg-open', f'{pdf_file}'])
        except Exception as e:
            print(f"Erreur lors de l'ouverture du PDF : {str(e)}")
            
    def openTEXT(self, file_name):
        txt_file = path.join(self.racine, file_name)
        print(txt_file)
        with open(txt_file, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            return file_contents
       

# == Class ColorSelectionDialog == selection de la couleurs des echant
class ColorSelectionDialog(QDialog):
    send_data = Signal(str, object)
    
    def __init__(self, tab_sample, color_list, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Select samples colors:')
        self.tab_sample = tab_sample
        self.color_list = color_list
        
        self.elements = []
        self.colors = []
                
        self.layout = QVBoxLayout(self)

        # Bouton pour ajouter un nouvel échantillon
        self.add_button = QPushButton("Add new sample", self)
        self.add_button.clicked.connect(self.add_sample)
        self.layout.addWidget(self.add_button)

        # init le tableau de couleur si non vide vide
        if len(self.tab_sample) > 0 :
            for n in self.tab_sample:
                self.add_sample()
        else:
            self.tab_sample = self.generate_color_table()
            self.add_sample()

    def add_sample(self):
        # find the new name / color to display
        sample_index = len(self.elements)
        info_sample = list(self.tab_sample)[sample_index]
        
        # input the parameters
        element_name = str(info_sample)
        self.elements.append(element_name)
        color = to_hex(self.tab_sample[str(info_sample)])
        self.colors.append(color)
        
        # Création du layout et des widgets pour le nouvel élément
        element_layout = QHBoxLayout()
        label = QLabel(element_name)
        label.setAlignment(Qt.AlignmentFlag.AlignRight)

        button = QPushButton(element_name, self)
        button.setStyleSheet(f"background-color: {color}; color: rgba(0, 0, 0, 0)")
        button.setFixedWidth(50)
        button.clicked.connect(self.select_color)
        
        # Ajout du label et du bouton au layout de l'élément
        element_layout.addWidget(label)
        element_layout.addWidget(button)
        
        # Ajout du layout de l'élément au layout principal
        self.layout.addLayout(element_layout)

    def select_color(self):
        button = self.sender()
        index = self.elements.index(button.text())
        color = QColorDialog.getColor(QColor(self.colors[index]))
        if color.isValid():
            color_name = color.name()
            button.setStyleSheet(f"background-color: {color_name}; color: rgba(0, 0, 0, 0)")
            self.tab_sample[button.text()] = hex2color(color_name)
            self.color_list[button.text()] = hex2color(color_name)
            self.send_data.emit("color_picker", self.color_list)

    def generate_color_table(self, *, nb=50):
        #Generate a base color list
        tab_color = {}
        n=1
        for i in range(nb):
            for item, value in TABLEAU_COLORS.items():
                tab_color["sample " + str(n)] = hex2color(value)
                n = n + 1
        
        return tab_color
      
    def closeEvent(self, event):
        self.send_data.emit("color_picker", self.color_list)
        

# == Class ProgressWindow == creation et gestion de la barre de progresion

class ProgressWindow(QWidget):
    stop = Signal(str)
    
    def __init__(self, parent=None, gui=True):
        super().__init__(parent)
        
        self.memoire = ''
        
        self.setWindowTitle('Processing....')
        self.resize(250,25)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.text()
        self.progressbar()
        
        layout = QVBoxLayout()
        layout_0 = QHBoxLayout()
        layout_0.addWidget(self.progress_label)
        layout_0.addWidget(self.progress_files)
        
        layout.addLayout(layout_0)
        layout.addWidget(self.progress)
        layout.addWidget(self.sub_progress)
        
        self.setLayout(layout)
    
    def update_progress(self, n, n_tot,stage,value):
        self.progress_files.setText(str(n) + " / " + str(n_tot))
        self.progress.setFormat("File step : " + stage)
        self.progress.setValue(value)
        if value == 0 : self.sub_progress.setValue(0)
            
    def update_sub_progress(self,value):
        self.sub_progress.setValue(value)
        if value == 100 : self.sub_progress.setValue(0)
            
    # specification des widgets
    def text(self):
        self.progress_label = QLabel('Files : ', self)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.progress_files = QLabel('', self)
        self.progress_files.setAlignment(Qt.AlignmentFlag.AlignLeft)
    def progressbar(self):
        self.progress = QProgressBar(self)
        self.progress.setMaximum(8)
        self.progress.setFormat("File step : ")
        self.progress.setStyleSheet("""QProgressBar {text-align: center; /* Centre le texte horizontalement */}
                            QProgressBar::chunk {text-align: center; /* Centre le texte à l'intérieur de la barre de progression */}""")
        self.sub_progress = QProgressBar(self)
        self.sub_progress.setMaximum(100)
        self.sub_progress.setStyleSheet("QProgressBar { height: 8px; }")
        self.sub_progress.setFormat("step progression : %p%")
        self.sub_progress.setStyleSheet("""QProgressBar {text-align: center; /* Centre le texte horizontalement */}
                          QProgressBar::chunk {text-align: center; /* Centre le texte à l'intérieur de la barre de progression */}""")


    def closeEvent(self, event: QCloseEvent):
        if event.spontaneous():
            reply = QMessageBox.question('Confirmation',
                                           'are you sure to stop the process ?',
                                           QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.emit.stop("progress")
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
                

# == Class ErrorWinwdow ==
class ErrorDialog(QDialog):
    def __init__(self, origin: str, stage: str, error_message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        # Layout principal
        layout = QVBoxLayout(self)

        # Titre de l'erreur
        title_label = QLabel(f"<b>Error during the process {origin} at the stage: {stage}</b>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Message d'erreur (avec traceback)
        error_label = QLabel(f"<pre>{error_message}</pre>")
        error_label.setWordWrap(True)
        layout.addWidget(error_label)

        # Bouton pour copier l'erreur dans le presse-papiers
        copy_button = QPushButton("Copy Error to Clipboard")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(error_message))
        layout.addWidget(copy_button)

        # Boutons standard (OK)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

    def copy_to_clipboard(self, text: str):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
