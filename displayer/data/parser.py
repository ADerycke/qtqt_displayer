# IMPORT LIBRARY

#basic librairy
import numpy
from xarray import DataArray
from pandas import DataFrame
from pandas import to_numeric

#internal lib
from . import utils



# === GET SAMPLES color and name ===

def get_colorlist(data, tab_color_init, *, color_list=''):
    
    nb_file = int(data.iloc[0])
    files = data[1 : nb_file + 1]
    #files = files.squeeze()

    for index, row in files.iterrows():
        #row = row.str.replace(".txt","")
        row = row.str.replace(" ","_")
        test_1 = row.str.split(pat='/',n=-1, expand=True)
        test_2 = test_1[test_1.shape[1]-1].values
        nom_ech = test_2[0].split('.txt')
        files.loc[index,:] = nom_ech[0]
    
    if color_list == '': color_list = {} 
    sample = {}
    
    n=1
    
    for i in tab_color_init:
        if n > nb_file:
            pass
        else:
            nom = str(files.loc[n].values).replace("(",'').replace(")",'').replace("[","").replace("]","").replace("'","").replace(".txt","").replace("_"," ")
            if nom in color_list :
                pass
            else:
                color_list[nom] = tab_color_init[i]
            sample[n - 1] = {'id' : n-1, 'name' : nom, 'color' : color_list[nom]}
            n=n+1     
            
    return color_list, sample

# === GET INFO ===

def get_inversion_info(data):
    
    info_list = {}
    # empty_dataframe
    empty_dataframe = {}
    for i in range(0, 10):
        empty_dataframe[i] = [0]

    #info recuperation
    
    info_loc1 = data[data[data.columns[0]].str.contains('Monitoring')]
    info_1 = data[info_loc1.index[0]+1 : info_loc1.index[0]+2]
    info_1 = info_1.squeeze()
    info_1 = info_1.replace(' =', '_=').replace('  ', ' ')
    info_1 = info_1.split(' ')
    info_2 = data[info_loc1.index[0]+2 : info_loc1.index[0]+3]
    info_2 = info_2.squeeze()
    info_2 = info_2.replace(' =', '_=').replace('#IO ', ' #IO').replace('  -nan', '-nan').replace('  ', ' ')
    info_2 = info_2.split(' ')
    
    info_loc2 = data[data[data.columns[0]].str.contains('Max allowable dTdt')]
    info_3 = data[info_loc2.index[0] : info_loc2.index[0]+1]
    info_3 = info_3.squeeze()
    info_3 = info_3.replace(' =', '_=').replace('  ', ' ')
    info_3 = info_3.split(' ')
    
    info_loc3 = data[data[data.columns[0]].str.contains('AdaptiveTimestep')]
    if info_loc3.empty:
        info_4 = DataFrame(empty_dataframe)
        info_5 = DataFrame(empty_dataframe)
    else:
        info_4 = data[info_loc3.index[0]+1 : info_loc3.index[0]+2]
        info_4 = info_4.squeeze()
        info_4 = info_4.replace(' =', '_=').replace('  ', ' ')
        info_4 = info_4.split(' ')
        info_5 = data[info_loc3.index[0]+2 : info_loc3.index[0]+3]
        info_5 = info_5.squeeze()
        info_5 = info_5.replace(' =', '_=').replace('  ', ' ')
        info_5 = info_5.split(' ')
    
    info_6 = data.iloc[-2]
    info_6 = info_6.squeeze()
    info_6 = info_6.split(' ')
    info_7 = data.iloc[-1]
    info_7 = info_7.squeeze()
    info_7 = info_7.split(' ')
    
    info_loc4 = data[data[data.columns[0]].str.contains('Move 1 :')]
    info_8 = data[info_loc4.index[0] : info_loc4.index[0]+11]
    info_8 = info_8.squeeze()
    info_8 = info_8.str.split(n=-1, expand=True)
    info_8.rename(columns={4:"nb_prop", 5:"ratio_prop", 7:"nb_accep", 8:"ratio_accep"},inplace=True)
    
    #info association
    info_list['Thinning'] =int(info_1[5])
    if int(info_1[8]) == 0:
        info_list['Gaussian exploration'] = 'no'
    else:
        info_list['Gaussian exploration'] = 'yes'
    if int(info_1[11]) == 0:
        info_list['Keep complex history'] = 'yes'
    else:
        info_list['Keep complex history'] = 'no'
        
    if 'nan' or '-' in info_2[5]:
        info_list['offset gaussian'] = 'no'
    elif float(info_2[5]) == 0:
        info_list['offset gaussian'] = 'no'
    else:
        info_list['offset gaussian'] = str(round(float(info_2[5]),0)) + '°/km'
    info_list['time gaussian'] = float(info_2[1])
    info_list['temperature gaussian'] = float(info_2[3])
        
    if int(info_3[6]) == 0:
        info_list['allow reheating'] = 'yes'
    else:
        info_list['allow reheating'] = 'no'
    info_list['Max allowable dTdt'] = round(float(info_3[3]))
    info_list['Rate tolerance'] = round(float(info_3[9]))
    
    info_list['Temperature steps diffusion Ap'] = round(float(info_4[5]))
    info_list['Temperature steps diffusion Other'] = round(float(info_4[8]))
    info_list['Temperature steps radi dam Ap'] = round(float(info_5[6]))
    info_list['Temperature steps radi dam Other'] = round(float(info_5[9]))
    
    if round(float(info_6[0]),0)/60/60 >= 1:
        info_list['time burnin'] = str(round(float(info_6[0])/60/60,1)) + ' h.'
    else:
        info_list['time burnin'] = str(round(float(info_6[0])/60)) + ' min.'
        
    if round(float(info_7[0]),0)/60/60 >= 1:
        info_list['time total'] = str(round(float(info_7[0])/60/60,1)) + ' h.'
    else:
        info_list['time total'] = str(round(float(info_7[0])/60)) + ' min.'
        
    info_list['Acceptance time'] = round(float(info_8.ratio_accep.iloc[0]) * 100) 
    info_list['Acceptance temperature'] = round(float(info_8.ratio_accep.iloc[1]) * 100)
    info_list['Acceptance offset'] = utils.def_valeur(info_8.ratio_accep.iloc[2],'')
    
    info_list['Acceptance Birth'] = round(float(info_8.ratio_accep.iloc[3]) * 100)
    info_list['Acceptance Death'] = round(float(info_8.ratio_accep.iloc[4]) * 100)
    
    info_list['FT resample'] = utils.def_valeur(info_2[16], 'no')
    info_list['He resample'] = utils.def_valeur(info_2[19], 'no')
    info_list['VR resample'] = utils.def_valeur(info_2[22], 'no')
    
    info_list['Acceptance FT'] = utils.def_valeur(info_8.ratio_accep.iloc[5],'')
    info_list['Acceptance He'] = utils.def_valeur(info_8.ratio_accep.iloc[6],'')
    info_list['Acceptance Vitr'] = utils.def_valeur(info_8.ratio_accep.iloc[7],'')
    
    if info_list['Acceptance FT'] == '': info_list['FT resample'] = 'no'
    if info_list['Acceptance He'] == '': info_list['He resample'] = 'no'
    if info_list['Acceptance Vitr'] == '': info_list['VR resample'] = 'no'
    
    if info_list['FT resample'] == 'no': info_list['Acceptance FT'] = ''
    if info_list['He resample'] == 'no': info_list['Acceptance He'] = ''
    if info_list['VR resample'] == 'no': info_list['Acceptance Vitr'] = ''
        
    return info_list


# === CHAIN === # def extract_tT_history(data, data_tT)

def extract_tT_history(data):
    Chain_loc = data[data[data.columns[0]].str.contains('CHAIN')]
    Chain = data[Chain_loc.index[0]+1 : Chain_loc.index[1]-1]
    Chain = Chain.squeeze()
    Chain_tab = Chain.str.split(n=-1, expand=True)
    #tqdm_stream.write(' 20%]')
    Chain_tab.rename(columns={0:"Step",1:"Likelihood",2:"Posterior",3:"nb_point"},inplace=True)
    Chain_tab = Chain_tab.apply(to_numeric, errors='coerce')
    #tqdm_stream.write(' 40%]')
    Chain_tab = Chain_tab.round(2)
    nb_ech = data.iloc[0].values
    #tqdm_stream.write(' 60%]')
   
    # HISTOIRE : convertir le format QTQt vers un format utilsable en passant par un array 3D
    
    X = range(4) #time, temperature, Z, info iteration
    Y = range(Chain_tab.shape[1]-4)
    iteration = range(Chain_tab.shape[0])    
    data_tT = DataArray(
        data=numpy.full((len(iteration), len(Y), len(X)), numpy.nan),
        coords={'X': X, 'Y': Y, 'iteration': iteration},
        dims=('iteration', 'Y', 'X')
    )
    
    #tqdm_stream.write(' 80%]')
    data_tT[:,0,3]=Chain_tab.Step
    data_tT[:,1,3]=Chain_tab.Likelihood
    data_tT[:,2,3]=Chain_tab.Posterior
    data_tT[:,3,3]=Chain_tab.nb_point

    #boucle dans les colonnes pour la recuperation
    i=0
    j=0
    if int(nb_ech) > 1:
        nb_data = 2
    else:
        nb_data = 1
        
    for column in Chain_tab.columns[4:]:
        data_tT[:,j,i]=Chain_tab[column]
        i = i+1
        if i > nb_data :
            i = 0
            j = j+1
    
    return data_tT



# === GRID === # extract_grid_history(data)

def extract_grid_history(data):
    #nb of sample
    sample_loc = data[data[data.columns[0]].str.contains('Sample')]
    nb_sample = sample_loc.shape[0]

    #read the matrix (nb of point of time and temperature)
    nb_time = int(data.iloc[1].str.split(n=-1, expand=True)[0])
    time_step = float(data.iloc[1].str.split(n=-1, expand=True)[2]) #size in Ma of a time step
    nb_tempe = int(data.iloc[1].str.split(n=-1, expand=True)[1])
    max_tempe = int(data.iloc[1].str.split(n=-1, expand=True)[3]) #the matrix include max_tempe point above 0 ???

    #init the t(T) envelopp
    enveloppe = {
        'Y_068_min': numpy.empty(nb_time),
        'Y_068_max': numpy.empty(nb_time),
        'Y_096_min': numpy.empty(nb_time),
        'Y_096_max': numpy.empty(nb_time),
        'Y_100_min': numpy.empty(nb_time),
        'Y_100_max': numpy.empty(nb_time)
    }

    #store in a xarray as usual
    Time = range(nb_time)
    Tempe = range(nb_tempe)
    Sample = range(nb_sample)
    data_stat = DataArray(
        data=numpy.full((len(Sample),len(Tempe),len(Time)), numpy.nan),
        coords={'X': Time, 'Y': Tempe, 'Sample': Sample},
        dims=('Sample','Y', 'X')
    )

    #file the xarray
    n = 0
    for index, row in sample_loc.iterrows():
        #get the sample matrix
        data_tempo = data.iloc[index+2:index+2+nb_time]
        data_tempo = data_tempo.astype(str)
        data_tempo = data_tempo[data_tempo.columns[0]].str.split(n=-1, expand=True)
        #get the nb of path and calcuate the proporation in %
        num_path = data_tempo.iloc[:,-1]
        data_tempo = data_tempo.iloc[:, :-1]
        for i in data_tempo.columns:
            data_tempo[i] = data_tempo[i].astype(int) / num_path.astype(int)
        #transpose to get the proper x-y axis
        data_tempo = data_tempo.transpose()

        #determine the t(T) path envelopp
        m=0
        if n == 0 :
            for i in data_tempo.columns:
                enveloppe['Y_068_min'][m], enveloppe['Y_068_max'][m] = utils.find_envelop(data_tempo[i], 0.6827)
                enveloppe['Y_096_min'][m], enveloppe['Y_096_max'][m] = utils.find_envelop(data_tempo[i], 0.9545)
                enveloppe['Y_100_min'][m], enveloppe['Y_100_max'][m] = utils.find_envelop(data_tempo[i], 0.9973)
                m=m+1

        # go from 0 - 1 to 0-100 for percentage
        data_tempo = data_tempo * 100
        data_stat[n,:,:]=data_tempo
        n=n+1

    # determine the differente X% enveloppe
    #remove the +100°C that make no sense here ?? care only ok if stage remaine 1°C
    enveloppe['Y_068_min'] = enveloppe['Y_068_min']-max_tempe
    enveloppe['Y_068_max'] = enveloppe['Y_068_max']-max_tempe
    enveloppe['Y_096_min'] = enveloppe['Y_096_min']-max_tempe
    enveloppe['Y_096_max'] = enveloppe['Y_096_max']-max_tempe
    enveloppe['Y_100_min'] = enveloppe['Y_100_min']-max_tempe
    enveloppe['Y_100_max'] = enveloppe['Y_100_max']-max_tempe
    
    info = [nb_time, time_step, nb_tempe, max_tempe]
    
    return data_stat, enveloppe, info



# === CONSTRAIN === # def extract_constrain(data)

def extract_constrain(data):
    # retriver the input constrains
    constrain_loc = data[data[data.columns[0]].str.contains('Setting tt points 1 =')]

    test = constrain_loc.squeeze()
    constrain_nb = test.split(' ')
    constrain = data[constrain_loc.index[0] + 1 : constrain_loc.index[0] + 1 + int(constrain_nb[5])]

    constrain_tab = constrain.squeeze()
    if isinstance(constrain_tab,str):
        constrain_tab = constrain_tab.split()
        constrain_tab = [['Time', 'dTime', 'Temp', 'dTemp','?'],constrain_tab]
        constrain_tab = DataFrame(constrain_tab[1:], columns=constrain_tab[0])
    else:
        constrain_tab = constrain_tab.str.split(n=-1, expand=True)
        constrain_tab.rename(columns={0:"Time",1:"dTime",2:"Temp",3:"dTemp"},inplace=True)
    
    # retriver the sample constrains
    sample_constrain_loc = data[data[data.columns[0]].str.contains('Predep')]
    sample_constrain_tab = sample_constrain_loc.squeeze()
    sample_constrain_tab = sample_constrain_tab.str.split(n=-1, expand=True)
    sample_constrain_tab.rename(columns={1:"Time",2:"dTime",3:"Temp",4:"dTemp"},inplace=True)

    # merge data in a xarray
    X = range(5) #time, dtime, temperature, dtemperature, type
    Y = range(len(constrain_tab) + len(sample_constrain_tab)) #

    data_constrain = DataArray(
        data=numpy.full((len(Y),len(X)), numpy.nan, dtype=object),
        coords={'data': X, 'constrain_n': Y},
        dims=('constrain_n', 'data')
    )

    i=0
    for index, row in constrain_tab.iterrows():
        data_constrain[i,0]=row.Time
        data_constrain[i,1]=row.dTime
        data_constrain[i,2]=row.Temp
        data_constrain[i,3]=row.dTemp
        if i == 0 : 
            data_constrain[i,4]="explo_box"
        else:
            data_constrain[i,4]="external_contraint"
        i=i+1
    
    for index, row in sample_constrain_tab.iterrows():
        data_constrain[i,0]=row.Time
        data_constrain[i,1]=row.dTime
        data_constrain[i,2]=row.Temp
        data_constrain[i,3]=row.dTemp
        data_constrain[i,4]="sample_contraint"
        i=i+1
    
    return data_constrain


# === PREDICTED t(T) === # def extract_tT_pred(data, data_Chemin)

def extract_tT_pred(data):
    max_point = 3
    
    #bloc 1
    Chemin_loc = data[data[data.columns[0]].str.contains('Max Like')]
    nb_point_like = data[Chemin_loc.index[0]+2 : Chemin_loc.index[0]+3].values
    Chemin_val = data[Chemin_loc.index[0]+1 : Chemin_loc.index[0] + 3]
    Chemin_val_like = Chemin_val.squeeze()
    Chemin_val_like = Chemin_val_like.str.split(n=-1, expand=True)
    Chemin_val_like.rename(columns={2:"Like",4:"Posterior"},inplace=True)
    Chemin_point = data[Chemin_loc.index[0]+3 : Chemin_loc.index[0] + 3 + int(nb_point_like)]
    Chemin_point_like = Chemin_point.squeeze()
    Chemin_point_like = Chemin_point_like.str.split(n=-1, expand=True)
    Chemin_point_like.rename(columns={0:"point",1:"Time",2:"Temp",3:"Z"},inplace=True)
    max_point = max(int(nb_point_like),max_point)
    
    #bloc 2
    Chemin_loc = data[data[data.columns[0]].str.contains('Max Post')]
    nb_point_post = data[Chemin_loc.index[0]+2 : Chemin_loc.index[0]+3].values
    Chemin_val = data[Chemin_loc.index[0]+1 : Chemin_loc.index[0] + 3]
    Chemin_val_post = Chemin_val.squeeze()
    Chemin_val_post = Chemin_val_post.str.split(n=-1, expand=True)
    Chemin_val_post.rename(columns={2:"Like",4:"Posterior"},inplace=True)
    Chemin_point = data[Chemin_loc.index[0]+3 : Chemin_loc.index[0] + 3 + int(nb_point_post)]
    Chemin_point_post = Chemin_point.squeeze()
    Chemin_point_post = Chemin_point_post.str.split(n=-1, expand=True)
    Chemin_point_post.rename(columns={0:"point",1:"Time",2:"Temp",3:"Z"},inplace=True)
    max_point = max(int(nb_point_post),max_point)
    
    #bloc 3
    Chemin_loc = data[data[data.columns[0]].str.contains('EXPECTED')]
    nb_point_expect = data[Chemin_loc.index[0]+3 : Chemin_loc.index[0]+4].values
    nb_point_expect = nb_point_expect[0,0].split(' ')
    Chemin_point = data[Chemin_loc.index[0]+4 : Chemin_loc.index[0] + 4 + int(nb_point_expect[0])]
    Chemin_point_expect = Chemin_point.squeeze()
    Chemin_point_expect = Chemin_point_expect.str.split(n=-1, expand=True)
    Chemin_point_expect.rename(columns={0:"Time",1:"T_Expected",2:"T_Mode",3:"T_env_sup",4:"T_env_inf"},inplace=True)
    max_point = max(int(nb_point_expect[0]),max_point)
    
    #recup dans un xarray
    X = range(3) #time, temperature, info
    Y = range(max_point)
    Chemin = range(6)
    #data_tT.clear()
    data_Chemin = DataArray(
        data=numpy.full((len(Chemin),len(Y),len(X)), numpy.nan, dtype=object),
        coords={'X': X, 'Y': Y, 'Chemin': Chemin},
        dims=('Chemin','Y', 'X')
    )
    
    utils.get_chemin (0, data_Chemin, Chemin_point_like,Chemin_val_like, max_point, int(nb_point_like), 'Temp')
    data_Chemin[0,0,2]='Max likelihood'
    utils.get_chemin (1, data_Chemin, Chemin_point_post,Chemin_val_post, max_point, int(nb_point_post), 'Temp')
    data_Chemin[1,0,2]='Max posterior'
    utils.get_chemin (2, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_Expected')
    data_Chemin[2,0,2]='Expected model'
    utils.get_chemin (3, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_Mode')
    data_Chemin[3,0,2]='Max mode model'
    utils.get_chemin (4, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_env_sup')
    data_Chemin[4,0,2]='Envelope sup. (99%)'
    utils.get_chemin (5, data_Chemin, Chemin_point_expect, "",max_point, int(nb_point_expect[0]), 'T_env_inf')
    data_Chemin[5,0,2]='Envelope inf. (99%)'

    return data_Chemin



# === PREDICTED t(T) for vertical profile === # def extract_tT_pred_vertical(data, sample_list):

def extract_tT_pred_vertical(data, sample_list):
    sample_path_loc = data[data[data.columns[0]].str.contains('Max Like|Max Post|EXPECTED|Sample ID|MODE')]
    nb_ech = int(data.loc[0])
    
    #determine the maximim point :
    max_point = 0
    mem_type = ""
    Mode = False
    n = 0
    for index, row in sample_path_loc.iterrows():
        if 'Max Like' in row[0]:
            mem_type = row[0] 
        if 'Max Post' in row[0]:
            mem_type = row[0]  
        if 'EXPECTED' in row[0]:
            mem_type = row[0]
        if 'MODE' in row[0]:
            if "END" in row[0]:
                Mode = False
            else:
                Mode = True
        if 'Sample ID' in row[0]:
            if 'Sample ID =' not in row[0]:
                if mem_type != "EXPECTED":
                    nb_constrain = int(data.iloc[index+1])
                    nb_point = int(data.iloc[index + 2 + nb_constrain]) + 1
                    if nb_point > max_point: max_point = nb_point
            else: 
                if Mode == False :
                    data_tempo = data.iloc[index+1].str.split(n=-1, expand=True) 
                    nb_point = int(data_tempo[0]) + 1
                    if nb_point > max_point: max_point = nb_point
    
    # prepare the xarray for data storage ()
    X = range(3) #time, temperature,info
    Y = range(max_point)
    Chemin = range(nb_ech * 3) # 1 sample = 3 paths (Like, post, expected) 
    data_Chemin = DataArray(
        data=numpy.full((len(Chemin),len(Y),len(X)), numpy.nan, dtype=object),
        coords={'X': X, 'Y': Y, 'Chemin': Chemin},
        dims=('Chemin','Y', 'X')
    )
    
    #fill the xarray with the path
    mem_type = ""
    Mode = False
    n = 0
    for index, row in sample_path_loc.iterrows():
        if 'Max Like' in row[0]:
            mem_type = row[0] 
        if 'Max Post' in row[0]:
            mem_type = row[0]  
        if 'EXPECTED' in row[0]:
            mem_type = row[0]
        if 'MODE' in row[0]:
            if "END" in row[0]:
                Mode = False
            else:
                Mode = True
        if 'Sample ID' in row[0]:
            if 'Sample ID =' not in row[0]:
                if mem_type != "EXPECTED":
                    #retriver
                    data_tempo = row.str.split(n=-1, expand=True)
                    sample_ID = int(data_tempo[2])
                    nb_constrain = int(data.iloc[index+1])
                    nb_point = int(data.iloc[index + 2 + nb_constrain]) + 1
                    index_init = index + 3
                    #prepare
                    Chemin_point = data.iloc[index_init:index_init + nb_point].squeeze()
                    Chemin_point = Chemin_point.str.split(n=-1, expand=True)
                    Chemin_point.rename(columns={0:"Time",1:"Temp",2:"Gradiant",3:"?"},inplace=True)
                    
                    #input in xarray
                    data_Chemin[n,0,2] = sample_list[sample_ID]
                    data_Chemin[n,1,2] = mem_type
                    data_Chemin[n,0:nb_point,0] = Chemin_point.Time
                    data_Chemin[n,nb_point:,0] = numpy.full(max_point - (nb_point) , numpy.nan) #needed for the plotting
                    data_Chemin[n,0:nb_point,1] = Chemin_point.Temp
                    data_Chemin[n,nb_point:,1] = numpy.full(max_point - (nb_point) , numpy.nan)#needed for the plotting
                    n = n + 1

            else: 
                if Mode == False :
                    #retriver
                    data_tempo = row.str.split(n=-1, expand=True)
                    sample_ID = int(data_tempo[3])
                    data_tempo = data.iloc[index+1].str.split(n=-1, expand=True) 
                    nb_point = int(data_tempo[0]) + 1
                    index_init = index + 2   
                    
                    #prepare
                    Chemin_point = data.iloc[index_init:index_init + nb_point].squeeze()
                    Chemin_point = Chemin_point.str.split(n=-1, expand=True)
                    Chemin_point.rename(columns={0:"Time",1:"T_Expected",2:"T_Mode",3:"T_env_sup",4:"T_env_inf",9: "Gradiant"},inplace=True)

                    #input in xarray
                    data_Chemin[n,1,2] = sample_list[sample_ID]
                    data_Chemin[n,1,2] = mem_type
                    data_Chemin[n,0:nb_point,0] = Chemin_point.Time
                    data_Chemin[n,nb_point:,0] = numpy.full(max_point - (nb_point) , numpy.nan)#needed for the plotting
                    data_Chemin[n,0:nb_point,1] = Chemin_point.T_Expected
                    data_Chemin[n,nb_point:,1] = numpy.full(max_point - (nb_point) , numpy.nan)#needed for the plotting
                    n = n + 1
                    
    return data_Chemin



# === He AGES === # def extract_He_Ages(data, data_He_Maxlike, data_He_MaxPost, data_He_Expect):
         
def extract_He_Ages(data):
    # AGE : extraire du fichier Summary.txt les chemins
    He_Age_loc = data[data[data.columns[0]].str.contains('Max Like|Max Post|EXPECTED|File Name|He =|HeR')]
    nb_ech = int(data.loc[0])

    # nettoyage des echan sans helium
    nb_He = 0
    mem = ""
    mem_ech = 0
    mem_type = ""
    Expected = False
    mem_expected = 1
    nom_ech = ""
    for index, row in He_Age_loc.iterrows():
        if 'HeR =' in row[0]:
            He_Age_loc.loc[index,:] = row.str.replace("HeR =",'He_' + nom_ech)
            He_Age_loc.loc[index,:] = He_Age_loc.loc[index,:].str.replace("Pred Age", str(mem_type + " " + str(mem_expected)))

        if 'Max Like' in row[0]:
            mem_type = row[0] 
            He_Age_loc = He_Age_loc.drop(labels=[index], axis = 0)
        if 'Max Post' in row[0]:
            mem_type = row[0]  
            He_Age_loc = He_Age_loc.drop(labels=[index], axis = 0)
        if 'EXPECTED' in row[0]:
            mem_type = row[0]
            He_Age_loc = He_Age_loc.drop(labels=[index], axis = 0)
            Expected = True
            mem_expected = 0

        if 'File Name =' in row[0]:
            if Expected == True:
                mem_expected = mem_expected + 1
                if mem_expected > 2:
                    mem_expected = 1
            #row = row.str.replace(".txt","")
            row = row.str.replace(" ","_")
            test_1 = row.str.split(pat='/',n=-1, expand=True)
            nom_ech = str(test_1[test_1.shape[1]-1].values)
            nom_ech = nom_ech.replace("(",'').replace(")",'').replace("[","").replace("]","").replace("'","").replace(".txt","")
            He_Age_loc.loc[index,:] = nom_ech + " t " + mem_type + " " + str(mem_expected)
            mem_ech = mem_ech + 1
            if mem_ech > nb_ech:
                mem_ech = 1
                
        if 'NFT =' in row[0]:
            He_Age_loc = He_Age_loc.drop(labels=[index], axis = 0)
        elif 'He =' in row[0]:
            test = row.str.split(n=-1, expand=True)
            if int(test[2]) == 0:
                He_Age_loc = He_Age_loc.drop(labels=[mem, index], axis = 0)
            else:
                nb_He = max(nb_He,int(test[2]))
                He_Age_loc = He_Age_loc.drop(labels=[index], axis = 0)

        else:    
            mem = index
    
    if not He_Age_loc.empty:
        He_Age_loc = He_Age_loc.squeeze()
        He_Age_loc = He_Age_loc.str.replace("Max ","Max-")
        He_Age = He_Age_loc.str.split(n=-1, expand=True)
        He_Age.rename(columns={0:"Nom",1:"Rs",2:"type",3:"type_bis",5:"Pred_ages",9:"Obs_age",12:"Error",18:"Tc", 19:"Crystal",22:"eU",25:"Ft",28:"Cor_Pred_age"},inplace=True)
        nb_ech = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('Max-Like')].Nom.shape[0]
        
        #recup des He
        X = range(10) #Rs, Pred Ages, ±, Obs Ages, ±, Tc, crystal, eU, Pred Ages (Corr), echantillon + info
        if nb_He == 1:
            Y = range(nb_He + 1)
        else:        
            Y = range(nb_He)
        echantillon = range(nb_ech)

        #maxlike
        data_He_Maxlike = DataArray(
            data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon','Y', 'X')
        )
        #maxpost
        data_He_MaxPost = DataArray(
            data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon','Y', 'X')
        )
        #expect
        data_He_Expect = DataArray(
            data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon','Y', 'X')
        )

        data_He_Maxlike[:,0,8] = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('Max-Like')].Nom
        data_He_Maxlike[:,1,8] = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('Max-Like')].type
        data_He_MaxPost[:,0,8] = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('Max-Post')].Nom
        data_He_MaxPost[:,1,8] = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('Max-Post')].type
        data_He_Expect[:,0,8] = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('EXPECTED') & He_Age.type_bis.str.contains('1')].Nom
        data_He_Expect[:,1,8] = He_Age[He_Age.Rs.str.contains('t') & He_Age.type.str.contains('EXPECTED') & He_Age.type_bis.str.contains('1')].type

        for n in echantillon:
            ech = data_He_Maxlike[n,0,8].values
            utils.get_He(n, ech ,nb_He, data_He_Maxlike, He_Age, 'Max-Like')
            utils.get_He(n, ech ,nb_He, data_He_MaxPost, He_Age, 'Max-Post')
            utils.get_He(n, ech ,nb_He, data_He_Expect, He_Age, 'EXPECTED')

        for n in echantillon: #calculate pred error
            data_He_Maxlike[n,:,1] = data_He_Maxlike[n,:,3].astype(dtype=float) / data_He_Maxlike[n,:,2].astype(dtype=float) * data_He_Maxlike[n,:,0].astype(dtype=float)
            data_He_MaxPost[n,:,1] = data_He_MaxPost[n,:,3].astype(dtype=float) / data_He_MaxPost[n,:,2].astype(dtype=float) * data_He_MaxPost[n,:,0].astype(dtype=float)
            data_He_Expect[n,:,1] = data_He_Expect[n,:,3].astype(dtype=float) / data_He_Expect[n,:,2].astype(dtype=float) * data_He_Expect[n,:,0].astype(dtype=float)
        
        return data_He_Maxlike, data_He_MaxPost, data_He_Expect
    
    else:
        
        return '', '', ''



# === FT AGES === # def extract_He_Ages(data, data_He_Maxlike, data_He_MaxPost, data_He_Expect)

def extract_FT_Ages(data):
    
    FT_Age_loc = data[data[data.columns[0]].str.contains('Max Like|Max Post|EXPECTED|File Name|Pred FT age')]
    nb_ech = int(data.loc[0])
    # nettoyage des echan sans AFT
    mem_type = ""
    mem_nom = ""
    mem_expected = 0
    Expected = False
    for index, row in FT_Age_loc.iterrows():

        if 'Max Like' in row[0]:
            mem_type = row.str.replace(" ","_")
            FT_Age_loc = FT_Age_loc.drop(labels=[index], axis = 0)
        elif 'Max Post' in row[0]:
            mem_type = row.str.replace(" ","_")
            FT_Age_loc = FT_Age_loc.drop(labels=[index], axis = 0)
        elif 'EXPECTED' in row[0]:
            mem_type = row.str.replace(" ","_")
            FT_Age_loc = FT_Age_loc.drop(labels=[index], axis = 0)
            Expected = True   

        elif 'File Name =' in row[0]:
            if Expected == True:
                mem_expected = mem_expected + 1
                if mem_expected > 2:
                    mem_expected = 1
            
            #row = row.str.replace(".txt","")
            row = row.str.replace(" ","_")
            test = row.str.split(pat='/',n=-1, expand=True)
            mem_nom = str(test[test.shape[1]-1].values).replace("(",'').replace(")",'').replace("[","").replace("]","").replace("'","").replace(".txt","")
            FT_Age_loc = FT_Age_loc.drop(labels=[index], axis = 0)

        elif 'Pred FT age =' in row[0]:
            test = row.str.split(n=-1, expand=True)
            if float(test[5]) == -1:
                FT_Age_loc = FT_Age_loc.drop(labels=[index], axis = 0)
            else:
                tempo = data.loc[index+4]
                tempo_2 = FT_Age_loc.loc[index].str.replace("Pred FT", mem_nom + " " + str(mem_type.values) + " " + str(mem_expected))
                FT_Age_loc.loc[index] = tempo_2 + " " + tempo

    if not FT_Age_loc.empty:
        FT_Age_tab = FT_Age_loc.squeeze()
        FT_Age_tab = FT_Age_tab.str.split(n=-1, expand=True)
        FT_Age_tab.rename(columns={0:"nom",1:"type",2:"expect",5:"Pred_ages",6:"Obs_ages",20:"Obs_ages_error",39:"Pred_kin", 40:"Obs_kin",41:"Obs_kin_error"},inplace=True)
        
        nb_FT = FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].nom.shape[0]

        #recup dans un xarray
        X = range(10) #Pred_ages, dpred, Obs_ages, dobs, nom, type, pre_kin, dpred, obs_kin, d_obs
        Y = range(1)
        echantillon = range(int(nb_FT))

        #1
        data_FT_like = DataArray(
            data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon', 'Y', 'X')
        )
        #2
        data_FT_post = DataArray(
            data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon', 'Y', 'X')
        )
        #3
        data_FT_expect = DataArray(
            data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon', 'Y', 'X')
        )

        data_FT_like[:,0,0]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].Pred_ages
        data_FT_like[:,0,1]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].Obs_ages
        data_FT_like[:,0,2]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].Obs_ages_error
        data_FT_like[:,0,4]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].nom
        data_FT_like[:,0,5]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].type
        data_FT_like[:,0,6]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].Pred_kin
        data_FT_like[:,0,8]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].Obs_kin
        data_FT_like[:,0,9]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].Obs_kin_error
        
        data_FT_post[:,0,0]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].Pred_ages
        data_FT_post[:,0,1]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].Obs_ages
        data_FT_post[:,0,2]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].Obs_ages_error
        data_FT_post[:,0,4]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].nom
        data_FT_post[:,0,5]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].type
        data_FT_post[:,0,6]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].Pred_kin
        data_FT_post[:,0,8]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].Obs_kin
        data_FT_post[:,0,9]=FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')].Obs_kin_error

        data_FT_expect[:,0,0]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].Pred_ages
        data_FT_expect[:,0,1]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].Obs_ages
        data_FT_expect[:,0,2]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].Obs_ages_error
        data_FT_expect[:,0,4]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].nom
        data_FT_expect[:,0,5]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].type
        data_FT_expect[:,0,6]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].Pred_kin
        data_FT_expect[:,0,8]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].Obs_kin
        data_FT_expect[:,0,9]=FT_Age_tab[FT_Age_tab.type.str.contains('EXPECTED') & FT_Age_tab.expect.str.contains('1')].Obs_kin_error

        data_FT_like[:,0,3] = data_FT_like[:,0,2].astype(dtype=float) / data_FT_like[:,0,1].astype(dtype=float) * data_FT_like[:,0,0].astype(dtype=float)
        data_FT_post[:,0,3] = data_FT_post[:,0,2].astype(dtype=float) / data_FT_post[:,0,1].astype(dtype=float) * data_FT_post[:,0,0].astype(dtype=float)
        data_FT_expect[:,0,3] = data_FT_expect[:,0,2].astype(dtype=float) / data_FT_expect[:,0,1].astype(dtype=float) * data_FT_expect[:,0,0].astype(dtype=float)
        
        data_FT_like[:,0,7] = data_FT_like[:,0,9].astype(dtype=float) / data_FT_like[:,0,8].astype(dtype=float) * data_FT_like[:,0,6].astype(dtype=float)
        data_FT_post[:,0,7] = data_FT_post[:,0,9].astype(dtype=float) / data_FT_post[:,0,8].astype(dtype=float) * data_FT_post[:,0,6].astype(dtype=float)
        data_FT_expect[:,0,7] = data_FT_expect[:,0,9].astype(dtype=float) / data_FT_expect[:,0,8].astype(dtype=float) * data_FT_expect[:,0,6].astype(dtype=float)
        
        return data_FT_like, data_FT_post, data_FT_expect
        
    else:
        return '', '', ''



# === FT LENGTH === # def extract_He_Ages(data, data_He_Maxlike, data_He_MaxPost, data_He_Expect)

def extract_FT_Length(data):
    
    #handle modification from old QTQt version to find the position of LFT data (location was missing)
    FT_Length_loc = data[data[data.columns[0]].str.contains('Lc0')]
    if FT_Length_loc.empty:
        LFT_marker = '1 0.100000 0.000000 0.000000 0.000000'
        LFT_shift = 1
    else:
        LFT_marker = 'Lc0 '
        LFT_shift = 0
    
    FT_Length_loc = data[data[data.columns[0]].str.contains('Max Like|Max Post|EXPECTED|File Name|' + LFT_marker)]
    mem_type = ""
    mem_nom = ""
    mem_expected = 0
    Expected = False
    for index, row in FT_Length_loc.iterrows():

        if 'Max Like' in row[0]:
            mem_type = row.str.replace(" ","_")
            FT_Length_loc = FT_Length_loc.drop(labels=[index], axis = 0)
        elif 'Max Post' in row[0]:
            mem_type = row.str.replace(" ","_")
            FT_Length_loc = FT_Length_loc.drop(labels=[index], axis = 0)
        elif 'EXPECTED' in row[0]:
            mem_type = row.str.replace(" ","_")
            FT_Length_loc = FT_Length_loc.drop(labels=[index], axis = 0)
            Expected = True   

        elif 'File Name =' in row[0]:
            if Expected == True:
                mem_expected = mem_expected + 1
                if mem_expected > 2:
                    mem_expected = 1

            #row = row.str.replace(".txt","")
            row = row.str.replace(" ","_")
            test = row.str.split(pat='/',n=-1, expand=True)
            mem_nom = test[test.shape[1]-1].values
            FT_Length_loc = FT_Length_loc.drop(labels=[index], axis = 0)

        elif LFT_marker in row[0]:
            FT_Length_loc.loc[index] = str(mem_nom[0]) + " " + mem_type.values + " " + str(mem_expected)

    FT_Length_tab = FT_Length_loc.squeeze()
    FT_Length_tab = FT_Length_tab.str.split(n=-1, expand=True)
    FT_Length_tab.rename(columns={0:"nom",1:"type",2:"expect"},inplace=True)
    nb_ech = FT_Length_tab[FT_Length_tab.type.str.contains('Max_Like')].nom.shape[0]
    
    #recup des FT
    X = range(6) #lenght, nb_obs, nb_pred_maxlike, nb_pred_maxpost, nb_pred_maxexpected, info
    Y = range(200)
    echantillon = range(nb_ech)

    data_FT_Lenght = DataArray(
        data=numpy.full((len(echantillon),len(Y),len(X)), numpy.nan, dtype=object),
        coords={'X': X, 'Y': Y, 'echantillon': echantillon},
        dims=('echantillon','Y', 'X')
    )

    for n in range(data_FT_Lenght.shape[0]):
        data_FT_Lenght[n,:,0]=numpy.arange(0,20, step=0.1)

    n=0
    
    
    #retriver observerd LFT and name #(n correspond to the sample number)
    for index, row in  FT_Length_tab[FT_Length_tab.type.str.contains('Max_Like')].iterrows():
        a = index
        
        obs_LFT = data[a - 20 : a - 2] #don't take the 20 as it is not present in the main matrix (0 to 19.9)
        obs_LFT = obs_LFT.squeeze()
        obs_LFT = obs_LFT.str.split(n=-1, expand=True)
        obs_LFT.rename(columns={0:"lenght",1:"curve",2:"bar"},inplace=True)
        
        #upscaling the table from 10 to 100 rows to fit all data in the same matrix (pred at 200 rows)  
        all_row = numpy.empty((20,10,))
        all_row[:,:] = numpy.nan
        all_row[1:19,0] = obs_LFT.bar #put the row 1 to 19 because the 0 is not there
        data_FT_Lenght[n,:,1] = all_row.ravel()
        data_FT_Lenght[n,0,5] = FT_Length_tab.loc[a].nom
        n=n+1
    
    n=0
    for index, row in  FT_Length_tab[FT_Length_tab.type.str.contains('Max_Like')].iterrows():
        a = index
        pred_LFT = data[a + 1 - LFT_shift  : a + 1 + 200 - LFT_shift]
        pred_LFT = pred_LFT.squeeze()
        pred_LFT = pred_LFT.str.split(n=-1, expand=True)
        pred_LFT.rename(columns={0:"number", 1:"lenght", 2:"curve"},inplace=True)
        data_FT_Lenght[n,:,2]=pred_LFT.curve
        n=n+1

    n=0
    for index, row in  FT_Length_tab[FT_Length_tab.type.str.contains('Max_Post')].iterrows():
        a = index
        pred_LFT = data[a + 1 - LFT_shift  : a + 1 + 200 - LFT_shift]
        pred_LFT = pred_LFT.squeeze()
        pred_LFT = pred_LFT.str.split(n=-1, expand=True)
        pred_LFT.rename(columns={0:"number", 1:"lenght", 2:"curve"},inplace=True)
        data_FT_Lenght[n,:,3]=pred_LFT.curve
        n=n+1

    n=0
    for index, row in FT_Length_tab[FT_Length_tab.expect.str.contains('1')].iterrows():   
        a = index
        pred_LFT = data[a + 1 - LFT_shift  : a + 1 + 200 - LFT_shift]
        pred_LFT = pred_LFT.squeeze()
        pred_LFT = pred_LFT.str.split(n=-1, expand=True)
        pred_LFT.rename(columns={0:"number", 1:"lenght", 2:"curve"},inplace=True)
        data_FT_Lenght[n,:,4]=pred_LFT.curve
        n=n+1
    
    return data_FT_Lenght



# === RESAMPLES PARAMETERS === # def extract_resample(data)

def extract_resample(data):

    nb_sample = int(data.iloc[0])
    nb_iteration= int(data.iloc[1 + nb_sample])

    # retriver sample information ("header" of the file)
    tab_info = data.iloc[1:1 + nb_sample]
    tab_info = tab_info[0].str.split('\t', n=-1, expand=True)
    tab_info.rename(columns={0:"Sample_nb",1:"obs_FT_age",2:"obs_MLT",3:"obs_kin",4:"obs_kin_error",5:"nb_He"},inplace=True)
    nb_max_he = int(tab_info['nb_He'].astype(int).max())
    
    # put samples information in a first xarray as usual for data explotation
    X = range(6 + nb_max_he * 2) #Sample_nb, obs_FT_age, obs_MLT, obs_FT_kin, obs_kin_error, nb_he, + he + he_error
    Y = range(nb_sample) #
    data_init = DataArray(
        data=numpy.full((len(Y),len(X)), numpy.nan),
        coords={'data': X, 'sample': Y},
        dims=('sample', 'data')
    )
    data_init = DataArray(tab_info)   

    # retriver sampling data
    tab_data = data.iloc[1 + nb_sample + 1 : 1 + nb_sample + 1  + (nb_iteration*nb_sample)]
    step_iteration = int(tab_data.iloc[0].str.split(' ', n=-1, expand=True)[0])
    split_data = tab_data[0].str.split(' ', n=-1, expand=True)
    tab_data[0] = numpy.where(split_data[1].astype(float) < 0,tab_data[0],"it like " + tab_data[0])
    tab_data = tab_data[0].str.split(' ', expand=True, n=-1)
    tab_data.rename(columns={0:"iteration",1:"likelihood",2:"sample",4:"FT kin",5:"nb_He"},inplace=True)

    # put samples information in a second xarray as usual for data explotation
    Iteration = range(nb_iteration)
    Donne = range(nb_max_he + 3) #iteration,like,FT kin + He kin 
    Sample = range(nb_sample)
    data_resample = DataArray(
        data=numpy.full((len(Sample),len(Donne),len(Iteration)), numpy.nan, dtype=object),
        coords={'X': Iteration, 'Y': Donne, 'Sample': Sample},
        dims=('Sample','Y', 'X')
    )

    tab_data_base = tab_data[tab_data['sample'] == "0"]
    
    for i in range(nb_sample):
        sample_tab_data = tab_data[tab_data['sample'] == str(i)]

        data_resample[i,0,:] = tab_data_base['iteration'].astype(int)
        data_resample[i,1,:] = tab_data_base['likelihood'].astype(float)
        data_resample[i,2,:] = sample_tab_data['FT kin'].astype(float)
        #handle the strange distribution
        for j in range(int(sample_tab_data['nb_He'].iloc[0])):
            if j == 0: 
                data_resample[i,3+j,:] = sample_tab_data.iloc[:,5+2].astype(float)
            else:
                data_resample[i,3+j,:] = sample_tab_data.iloc[:,5+4+(2*j)].astype(float)
    
    return data_init, data_resample

