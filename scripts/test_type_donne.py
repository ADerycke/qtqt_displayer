

# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

#from dataclasses import dataclass
import sys

#for the Qt window
try:
    from PySide6.QtWidgets import QApplication, QFileDialog
except:
    from PyQt5.QtWidgets import QApplication, QFileDialog

        
def get_file(*, racine=''):
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()

    if "win" in sys.platform:
        filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)')
    else:
        filepath, _ = QFileDialog.getOpenFileNames(None, 'Select one or multiple QTQt output file(s)', racine, 'Fichiers texte (*.txt)',  options=QFileDialog.Options() | QFileDialog.DontUseNativeDialog)

    return filepath




class HeData:
    
    def __init__(self):
        # --- chemical and age ---
        self.He : float
        self.U: float
        self.Th: float
        self.Sm: float
        
        self.age: float
        self.age_err: float
        
        # --- cristal parameters ---
    
        self.length: float
        self.width: float
        self.height: float
        
        self.mineral: str
        
        # --- model parameters ---
        
        self.alpha_ejection: float
        self.D0: float
        self.Ea: float
        
        self.model: str
        self.geometry: str
        
        # --- custom model ---
        #sampling :
        self.Rs_code: str
        self.Rs_min: float 
        self.Rs_max: float 
        
        self.eU: float
        self.eU_var: float
            
        # 3 row
        # self.c0: float
        # self.c1: float
        # self.c2: float
        # self.c3: List[float]
    
class FTData:
    
    def __init__(self):
        # --- counting data ---
        self.nlengths: float 
        self.ncounts: int 
        self.zeta: float 
        self.rhod: float 
        self.Nd: float 
        
        # --- sample data ---
        self.age: float
        self.age_err: float
        self.MTL: float 
        self.MTL_err: float
        self.MTL_stdev : float 
        self.MTL_stdev_err: float 
        
        self.compo_value: float 
        self.compo_error: float 
        
        
        # --- model data ---
        self.model_anneal: int 
        self.model_compo: int 
        
        self.model_init_tl : int
        self.size_init_tl : float
        
        self.projected_code: int 
        self.confined_code: int 
        self.acide_code: int 
        
        self.ns_ni: list[tuple[float, float]] = []
        self.tl: list[tuple[float, float, float]] = []
    
class SampleData:
    
    def __init__(self):
        self.name: str
       
        # --- geographical information ---
        self.X: float 
        self.Y: float 
        self.Z: float 
        
        # --- inversion parameters ---
        self.tT_point: list[tuple[float, float]]
        self.tT_present: tuple[float, float]
        
        # --- sample data ---
        self.FT = FTData()
        self.He: list[HeData] = []


def parse_qtqt_sample(path: str) -> SampleData:
    with open(path, "r") as f:
        lines = [l.strip() for l in f if l.strip()]

    i = 0
    sample = SampleData()

    #nom
    sample.name = lines[i]

    #coordinate
    i += 1
    tempo_line = list(map(float, lines[i].split()))
    sample.X = tempo_line[0]
    sample.Y = tempo_line[1]
    sample.Z = tempo_line[2]

    #FT info 1
    i += 1
    tempo_line = list(map(float, lines[i].split()))
    tT_nb = int(tempo_line[0])
    sample.FT.nlengths = int(tempo_line[1])
    sample.FT.ncounts = int(tempo_line[2])
    sample.FT.zeta = tempo_line[3]
    sample.FT.rhod = tempo_line[4]
    sample.FT.Nd = tempo_line[5]

    #FT model
    i += 1
    sample.FT.model_anneal = int(lines[i])
    i += 1
    tempo_line = list(map(float, lines[i].split()))
    sample.FT.model_compo = tempo_line[0]
    sample.FT.compo_value = tempo_line[1]
    sample.FT.compo_error = tempo_line[2]

    i += 1
    tempo_line = list(map(float, lines[i].split()))
    sample.FT.model_init_tl = tempo_line[0]
    sample.FT.size_init_tl = tempo_line[1]

    i += 1
    sample.FT.projected_code = int(lines[i][0])
    i += 1
    sample.FT.confined_code = int(lines[i][0])
    i += 1
    sample.FT.acide_code = int(lines[i][0])

    #time-temperature constrain points
    if tT_nb > 0 :
        for j in range(tT_nb):
            i += 1
            tempo_line = list(map(float, lines[i].split()))
            sample.tT_point.append([tempo_line[0],tempo_line[1]])

    # i += 1
    # tempo_line = list(map(float, lines[i].split()))
    # sample.tT_present=[tempo_line[0],tempo_line[1]]

    #FT info 2
    i += 1
    tempo_line = list(map(float, lines[i].split()))
    sample.FT.age = tempo_line[0]
    sample.FT.age_err = tempo_line[1]
    i += 1
    tempo_line = list(map(float, lines[i].split()))
    sample.FT.MTL = tempo_line[0]
    sample.FT.MTL_err = tempo_line[1]
    i += 1
    tempo_line = list(map(float, lines[i].split()))
    sample.FT.MTL_stdev = tempo_line[0]
    sample.FT.MTL_stdev_err = tempo_line[1]

    #counted data
    if sample.FT.ncounts > 0 :
        for j in range(sample.FT.ncounts):
            i += 1
            tempo_line = list(map(float, lines[i].split()))
            sample.FT.ns_ni.append((tempo_line[0], tempo_line[1]))
    
    #TL data
    if sample.FT.nlengths > 0 :
        for j in range(sample.FT.nlengths):
            i += 1
            tempo_line = list(map(float, lines[i].split()))
            if len(tempo_line) == 3 :
                sample.FT.tl.append((tempo_line[0], tempo_line[1],tempo_line[2] ))
            else:
                sample.FT.tl.append((tempo_line[0], tempo_line[1],0 ))
    
    #He data
    i += 1
    He_nb = int(lines[i][0])
    i += 1
    He_model = int(lines[i][0])

    for j in range(He_nb):
        i += 1
        tempo_He = HeData()
        tempo_data = list(map(float, lines[i].split()))
        i += 1
        tempo_model = list(map(str, lines[i].split()))
        
        tempo_He.He = tempo_data[0]
        tempo_He.U = tempo_data[1]
        tempo_He.Th = tempo_data[2]
        tempo_He.Sm = tempo_data[3]
        tempo_He.age = tempo_data[4]
        tempo_He.age_err = tempo_data[5]
        tempo_He.length = tempo_data[6]
        tempo_He.width = tempo_data[7]
        tempo_He.height = tempo_data[8]
        
        tempo_He.mineral = tempo_model[0]
        tempo_He.alpha_ejection = float(tempo_model[1])
        tempo_He.D0 = float(tempo_model[2])
        tempo_He.Ea = float(tempo_model[3])
        tempo_He.model = int(tempo_model[4])
        tempo_He.geometry = int(tempo_model[5])
        tempo_He.eU_var = float(tempo_model[6])
        
        #ajouter le test sur le model pour savoir la 3eme ligne
        if abs(tempo_He.model) >= 4 :
            i += 1
            tempo_add = list(map(float, lines[i].split()))
        
        sample.He.append(tempo_He)
        
    return sample


chemin = get_file()[0]
data_all = parse_qtqt_sample(chemin)

