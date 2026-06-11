# IMPORT LIBRARY

#basic librairy
import numpy
from pandas import DataFrame
from matplotlib.colors import TABLEAU_COLORS, hex2color


# === SUB FUNCTION === #

def get_chemin(n, tab_destination, dataframe, dataframe_2, max_p, nb_p, column):
    if nb_p == max_p:
        tab_destination[n,:,0]=dataframe.Time
        tab_destination[n,:,1]=dataframe[column]
    else:
        data_temp = dataframe.Time
        tab_destination[n,:,0]=numpy.pad(data_temp, (0 ,max_p-nb_p), 'constant', constant_values='nan')
        data_temp = dataframe[column]
        tab_destination[n,:,1]=numpy.pad(data_temp, (0 ,max_p-nb_p), 'constant', constant_values='nan')
    if isinstance(dataframe_2, DataFrame):
        tab_destination[n,1,2]=dataframe_2.iloc[0].Like
        tab_destination[n,2,2]=dataframe_2.iloc[0].Posterior
        
def get_He_old(n, echant_nom, nb_He, tab_destination, dataframe, filtre):
    
    a = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Pred_ages
    b = nb_He-len(a)
    
    #pred Ages
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Pred_ages
    tab_destination[n,:,0] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #error
    data_temp = ''
    tab_destination[n,:,1] = numpy.pad(data_temp, (0 ,nb_He), 'constant', constant_values='nan')
    #obs Ages
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Obs_age
    tab_destination[n,:,2] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #error
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Error
    tab_destination[n,:,3] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #Rs
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Rs
    tab_destination[n,:,4] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #Tc
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Tc
    tab_destination[n,:,5] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #eU
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].eU
    tab_destination[n,:,6] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #Pred Ages (Corr)
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Cor_Pred_age
    tab_destination[n,:,7] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')
    #Crystal
    data_temp = dataframe[dataframe.Nom.str.fullmatch('He_' + echant_nom) & dataframe.type.str.contains(filtre) & dataframe.type_bis.str.contains('1')].Crystal
    tab_destination[n,:,9] = numpy.pad(data_temp, (0 ,b), 'constant', constant_values='nan')

def get_He(n, echant_nom, nb_He, tab_destination, dataframe, filtre):
    

    # Filtre commun pour toutes les requêtes
    mask = (
            dataframe['Nom'].str.fullmatch('He_' + echant_nom) &  # Plus simple que fullmatch
            dataframe['type'].str.contains(filtre) &
            dataframe['type_bis'].str.contains('1')
            )    
    
    # Calcul du nombre de valeurs manquantes
    a = dataframe.loc[mask, 'Pred_ages']
    b = nb_He - len(a)  

    # Récupération des données avec le masque
    data = dataframe.loc[mask, [
        'Pred_ages', 'Obs_age', 'Error', 'Rs', 'Tc', 'eU', 'Cor_Pred_age', 'Crystal'
    ]]
    
    # Remplissage des données dans tab_destination
    for i, col in enumerate(['Pred_ages', 'Error_pred', 'Obs_age', 'Error', 'Rs', 'Tc', 'eU', 'Cor_Pred_age']):
        
        if col != "Error_pred":
            data_temp = data[col].values
            tab_destination[n, :, i] = numpy.pad(
                data_temp,
                (0, b),
                'constant',
                constant_values=numpy.nan
            )
        else:
            data_temp = ''
            tab_destination[n, :, i] = numpy.pad(
                data_temp,
                (0, b),
                'constant',
                constant_values=numpy.nan
            )

    # Cas particulier pour Crystal (index 9)
    if 'Crystal' in data.columns:
        data_temp = data['Crystal'].values
        tab_destination[n, :, 9] = numpy.pad(
            data_temp,
            (0, b),
            'constant',
            constant_values=numpy.nan
        )
    else:
        tab_destination[n, :, 9] = numpy.full(nb_He, numpy.nan)

    return tab_destination


def def_valeur(valeur, prefixe = '', remplacement = '', sufixe = ''): # change valeur to display for exploration parameters
    if 'nan' in valeur:
        text = remplacement
    elif '-' in valeur:
        text = remplacement
    elif float(valeur) == 0:
        text = remplacement
    else:
        valeur = float(valeur)
        if "%" in sufixe : valeur = valeur * 100
        text = prefixe + str(round(valeur)) + sufixe
        
    return text

def find_envelop(dataframe_column, value):
    # Find the maximum value index and initialize
    max_index = dataframe_column.argmax()
    total_sum = dataframe_column[max_index]
    start, end = max_index, max_index
    iteration = 0
    
    # Initialize the left and right bounds for expansion
    left, right = max_index - 1, max_index + 1
    if left < 0 : left = 0
    if right > len(dataframe_column) : right = len(dataframe_column)
    
    # Iterate until total_sum exceeds value or the entire column is traversed
    while total_sum <= value and (left > 0 or right < len(dataframe_column) - 1):
        iteration += 1
        # Expand left if there are still elements to the left
        
        if dataframe_column[left] > 0:
            total_sum += dataframe_column[left]
            start = left
        if left > 0 : left -= 1
        
        # Expand right if there are still elements to the right
        if dataframe_column[right] > 0:
            total_sum += dataframe_column[right]
            end = right
        if right < len(dataframe_column)-1 : right += 1
            
    return start, end

def clean_name(name):
    name_clean = str(name)
    name_clean = name_clean.replace(".txt", "")
    
    name_clean = name_clean.replace(" ", "_")
    name_clean = name_clean.replace("(",'')
    name_clean = name_clean.replace(")",'')
    name_clean = name_clean.replace("[","")
    name_clean = name_clean.replace("]","")
    name_clean = name_clean.replace("'","")
    
    return name_clean

def init_color_table():
    # load an initial color liste for sample
    tab_color = []
    for i in range(50): #50 = nb of max files for QTQt
        for item, value in TABLEAU_COLORS.items():
            tab_color.append(hex2color(value))
    
    return tab_color

def tab_samples_get_id(tab_samples, id_target):    
    for cle, sous_dict in tab_samples.items():
        if sous_dict['id'] == id_target:
            return cle
    
    return ''