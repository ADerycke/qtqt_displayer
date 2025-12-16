# IMPORT LIBRARY

#basic librairy
import numpy
from pandas import DataFrame

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
        
def get_He(n, echant_nom, nb_He, tab_destination, dataframe, filtre):
    
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

def def_valeur(valeur, remplacement): # change valeur to display for exploration parameters
    if 'nan' in valeur:
        text = remplacement
    elif '-' in valeur:
        text = remplacement
    elif float(valeur) == 0:
        text = remplacement
    else:
        if remplacement != '' :
            text = str(round(float(valeur)*100)) + "%"
        else:
            text = ' (' + str(round(float(valeur)*100)) + "%)"
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


