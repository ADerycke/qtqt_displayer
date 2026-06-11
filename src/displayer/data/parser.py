# IMPORT LIBRARY

#basic librairy
import numpy
from xarray import DataArray
from pandas import DataFrame
from pandas import to_numeric, concat
from pandas import Series


#internal lib
from . import utils
from .datatypes import SampleList

# === GET SAMPLES color and name ===

def get_samples(data, summary_name, *, tab_color=None, tab_sample=None):

    if tab_sample is None:
        tab_sample = SampleList(summary_name)
    else:
        #update the summary name to avoid duplicate ID
        tab_sample.summary_name_ = summary_name
        
    if tab_color is None:
        tab_color = utils.init_color_table()

    # --- Nombre de fichiers ---
    nb_file = int(data.iloc[0, 0])

    # --- Extraction des noms ---
    filespaths = data.iloc[1: nb_file + 1, 0].astype(str)
    
    filespaths = (
        filespaths
        # split information
        .str.split(' : ')
        .str[0]
        )
    

    # built or complete the samples list 
    for i, filepath in enumerate(filespaths):
        tab_sample.add_sample(filepath, i, tab_color)

    return tab_color, tab_sample

# === GET INFO ===

def get_inversion_info(data):
    """
    Parameters
    ----------
    data : dataframe of the full summary file

    Returns
    -------
    info_list : list of the data inversion parameters and statistiques

    """
    
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
        info_9 = DataFrame(empty_dataframe)
    else:
        info_4 = data[info_loc3.index[0]+1 : info_loc3.index[0]+2]
        info_4 = info_4.squeeze()
        info_4 = info_4.replace(' =', '_=').replace('  ', ' ')
        info_4 = info_4.split(' ')
        info_5 = data[info_loc3.index[0]+2 : info_loc3.index[0]+3]
        info_5 = info_5.squeeze()
        info_5 = info_5.replace(' =', '_=').replace('  ', ' ')
        info_5 = info_5.split(' ')
        info_9 = info_loc3.squeeze()
        info_9 = info_9.split(' ')
    
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
    
    if int(info_3[6]) == 0:
        info_list['allow reheating'] = 'yes'
    else:
        info_list['allow reheating'] = 'no'
        
    info_list['offset gaussian'] = float(info_2[5])
    info_list['time gaussian'] = float(info_2[1])
    info_list['temperature gaussian'] = float(info_2[3])
        
    info_list['Max allowable dTdt'] = float(info_3[3])
    info_list['Rate tolerance'] = float(info_3[9])
    
    if int(info_9[1]) == 1 :
        info_list['Adaptive time step'] = 'no'
    else:
        info_list['Adaptive time step'] = 'yes'
        
    info_list['Temperature steps diffusion Ap'] = float(info_4[5])
    info_list['Temperature steps diffusion Other'] = float(info_4[8])
    info_list['Temperature steps radi dam Ap'] = float(info_5[6])
    info_list['Temperature steps radi dam Other'] = float(info_5[9])
    
    info_list['time burnin'] = float(info_6[0])
    info_list['time total'] = float(info_7[0])

    info_list['Acceptance time'] = float(info_8.ratio_accep.iloc[0])
    info_list['Acceptance temperature'] = float(info_8.ratio_accep.iloc[1])
    
    if '#' in info_8.ratio_accep.iloc[2]:
        info_list['Acceptance offset'] = 0
    else:
        info_list['Acceptance offset'] = float(info_8.ratio_accep.iloc[2])
    
    info_list['Acceptance Birth'] = float(info_8.ratio_accep.iloc[3])
    info_list['Acceptance Death'] = float(info_8.ratio_accep.iloc[4])
    
    info_list['FT resample'] = float(info_2[16])
    info_list['He resample'] = float(info_2[19])
    info_list['VR resample'] = float(info_2[22])
    
    info_list['Acceptance FT'] = float(info_8.ratio_accep.iloc[5])
    info_list['Acceptance He'] = float(info_8.ratio_accep.iloc[6])
    info_list['Acceptance VR'] = float(info_8.ratio_accep.iloc[7])
    
    # edit the dict to rend it easely understandable
    if info_list['Acceptance FT'] == 0 : info_list['FT resample'] = 0
    if info_list['Acceptance He'] == 0 : info_list['He resample'] = 0
    if info_list['Acceptance VR'] == 0 : info_list['VR resample'] = 0
    if info_list['Acceptance offset'] == 0 : info_list['offset gaussian'] = 0
    
    # if info_list['FT resample'] == 'no': info_list['Acceptance FT'] = ''
    # if info_list['He resample'] == 'no': info_list['Acceptance He'] = ''
    # if info_list['offset gaussian'] == 'no': info_list['Acceptance offset'] = ''
    # if info_list['VR resample'] == 'no': info_list['Acceptance VR'] = ''
        
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
    nb_ech = data.iloc[0,0]#.values
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

    # --- Identifier les samples ---
    first_col = data.iloc[:, 0].astype(str)
    sample_indices = data[first_col.str.contains('Sample', na=False)].index
    nb_sample = len(sample_indices)

    # --- PASS 1 : récupérer les métadonnées et tailles max ---
    meta_per_sample = []
    max_time = 0
    max_tempe = 0

    for index in sample_indices:
        tab = data.iloc[index + 1].astype(str).str.split(expand=True).to_numpy()[0]

        nb_time = int(tab[0])
        nb_tempe = int(tab[1])
        time_step = float(tab[2])
        max_temp_sample = int(tab[3])

        meta_per_sample.append((nb_time, nb_tempe, time_step, max_temp_sample))

        max_time = max(max_time, nb_time)
        max_tempe = max(max_tempe, nb_tempe)

    # --- Initialisation xarray avec padding ---
    data_stat = DataArray(
        data=numpy.full((nb_sample, max_tempe, max_time), numpy.nan),
        coords={
            'Sample': range(nb_sample),
            'Y': range(max_tempe),
            'X': range(max_time)
        },
        dims=('Sample', 'Y', 'X')
    )

    enveloppes = []
    infos = []

    # --- PASS 2 : traitement des données ---
    for n, (index, meta) in enumerate(zip(sample_indices, meta_per_sample)):

        nb_time, nb_tempe, time_step, max_temp_sample = meta

        # --- enveloppe pour ce sample ---
        enveloppe = {
            'Y_068_min': numpy.empty(nb_time),
            'Y_068_max': numpy.empty(nb_time),
            'Y_096_min': numpy.empty(nb_time),
            'Y_096_max': numpy.empty(nb_time),
            'Y_100_min': numpy.empty(nb_time),
            'Y_100_max': numpy.empty(nb_time)
        }

        info = {
                "nb_time": nb_time,
                "nb_tempe": nb_tempe,
                "time_step": time_step,
                "max_tempe": max_temp_sample
                }

        # --- lecture bloc ---
        block = data.iloc[index + 2:index + 2 + nb_time]

        block = (
            block.iloc[:, 0]
            .astype(str)
            .str.split(expand=True)
        )

        num_path = block.iloc[:, -1].astype(int)
        values = block.iloc[:, :-1].astype(int)

        # normalisation
        values = values.div(num_path, axis=0)

        # orientation correcte
        values = values.T

        # --- calcul enveloppe ---
        for m, col in enumerate(values.columns):
            v = values[col]
            enveloppe['Y_068_min'][m], enveloppe['Y_068_max'][m] = utils.find_envelop(v, 0.6827)
            enveloppe['Y_096_min'][m], enveloppe['Y_096_max'][m] = utils.find_envelop(v, 0.9545)
            enveloppe['Y_100_min'][m], enveloppe['Y_100_max'][m] = utils.find_envelop(v, 0.9973)

        # correction température
        for key in enveloppe:
            enveloppe[key] -= max_temp_sample

        # stockage enveloppe + info
        enveloppes.append(enveloppe)
        infos.append(info)

        # --- stockage données ---
        values *= 100
        data_stat[n, :nb_tempe, :nb_time] = values.to_numpy()

    return data_stat, enveloppes, infos

# === CONSTRAIN === # def extract_constrain(data)

def extract_constrain(data):
    col = data.columns[0]

    # =========================
    # CONTRAINTES PRINCIPALES
    # =========================
    constrain_loc = data[data[col].str.contains('Setting tt points 1 =', na=False)]

    if constrain_loc.empty:
        constrain_tab = DataFrame(columns=["Time", "dTime", "Temp", "dTemp", "?"])
    else:
        test = constrain_loc.iloc[0, 0]
        constrain_nb = int(test.split()[5])

        raw_constrain = data.iloc[
            constrain_loc.index[0] + 1 :
            constrain_loc.index[0] + 1 + constrain_nb
        ].squeeze() 
        
        if isinstance(raw_constrain, str):
            parts = raw_constrain.split()
            constrain_tab = DataFrame(
                [parts],
                columns=["Time", "dTime", "Temp", "dTemp", "?"]
            )
        else:
            constrain_tab = (
                raw_constrain
                .str.split(' ', expand=True)
                #.iloc[:, :5]
            )
            constrain_tab.columns = ["Time", "dTime", "Temp", "dTemp", "?"]

    # =========================
    # SAMPLE CONSTRAINTS Not usable by now
    # =========================
    # sample_constrain_tab = data[data[col].str.contains('Setting tt points', na=False) &
    #                            ~data[col].str.contains('Setting tt points = 1', na=False)].squeeze()
    
    sample_constrain_tab = data[data[col].str.contains('an impossible charatere suit', na=False)]
    
    
    if isinstance(sample_constrain_tab, Series):
        sample_constrain_tab = sample_constrain_tab.to_frame().T

    sample_constrain_list = []
    for _, row in sample_constrain_tab.iterrows():
        test = row.iloc[0]
        try:
            constrain_nb = int(test.split()[5])
        except (IndexError, ValueError):
            continue

        tempo_data = data.iloc[
            constrain_loc.index[0] + 1 + 1 : #ignorer the first row that is the explo box
            constrain_loc.index[0] + 1 + constrain_nb
        ].squeeze()

        if isinstance(tempo_data, str):
            parts = tempo_data.split()
            df = DataFrame(
                [parts],
                columns=["Time", "dTime", "Temp", "dTemp", "?"]
            )
        else:
            df = (
                tempo_data
                .str.split(' ', expand=True)
                #.iloc[:, :4]
            )
            df.columns = ["Time", "dTime", "Temp", "dTemp", "?"]

        sample_constrain_list.append(df)

    if sample_constrain_list:
        sample_constrain_tab = concat(sample_constrain_list, ignore_index=True)
    else:
        sample_constrain_tab = DataFrame(columns=["Time", "dTime", "Temp", "dTemp", "?"])

    # =========================
    # CONCAT LOGIQUE
    # =========================
    def to_records(df, label_first=None, label_other=None):
        records = []
        for i, row in enumerate(df.itertuples(index=False)):
            records.append([
                row.Time,
                row.dTime,
                row.Temp,
                row.dTemp,
                label_first if i == 0 else label_other
            ])
        return records

    all_rows = []
    if not constrain_tab.empty:
        all_rows += to_records(
            constrain_tab,
            label_first="explo_box",
            label_other="external_contraint"
        )

    if not sample_constrain_tab.empty:
        all_rows += to_records(
            sample_constrain_tab,
            label_first="sample_contraint",
            label_other="sample_contraint"
        )

    # =========================
    # DATAARRAY FINAL
    # =========================
    if not all_rows:
        X = range(5)
        Y = range(1)
        data_constrain = DataArray(
            data=numpy.full((len(Y), len(X)), numpy.nan, dtype=object),
            coords={'data': X, 'constrain_n': Y},
            dims=('constrain_n', 'data')
        )
    else:
        X = range(5)
        Y = range(len(all_rows))
        data_constrain = DataArray(
            data=numpy.full((len(Y), len(X)), numpy.nan, dtype=object),
            coords={'data': X, 'constrain_n': Y},
            dims=('constrain_n', 'data')
        )
        data_constrain[:, :] = all_rows

    return data_constrain


# === PREDICTED t(T) === # def extract_tT_pred_vertical(data, sample_list):

def extract_tT_pred_samples(data, sample_list):

    col = data.columns[0]

    # =========================
    # FILTRAGE
    # =========================
    mask = data[col].str.contains(
        'Max Like|Max Post|EXPECTED|Sample ID|MODE',
        na=False
    )

    df = data.loc[mask].copy().reset_index(drop=False)

    nb_ech = int(data.iloc[0, 0])

    # =========================
    # DETECT MAX POINT
    # =========================
    max_point = 0
    mem_type = ""
    mode = False

    for _, row in df.iterrows():

        text = str(row[col])
        idx = row["index"]

        if 'Max Like' in text:
            mem_type = "Max Like"

        elif 'Max Post' in text:
            mem_type = "Max Post"

        elif 'EXPECTED' in text:
            mem_type = "EXPECTED"

        elif 'MODE' in text:
            mode = "END" not in text

        elif 'Sample ID' in text:

            if 'Sample ID =' not in text:

                if mem_type != "EXPECTED":
                    nb_constrain = int(data.iloc[idx + 1, 0])
                    nb_point = int(data.iloc[idx + 2 + nb_constrain, 0]) + 1

                    max_point = max(max_point, nb_point)

            else:

                if not mode:

                    nb_point = int(str(data.iloc[idx + 1, 0]).split()[0])
                    max_point = max(max_point, nb_point)

    # =========================
    # XARRAY INIT
    # =========================
    X = range(3)
    Y = range(max_point)
    Chemin = range(nb_ech * 6) # 6x for Max like, Max Post, Max Mode, Expected, env inf, env sup

    data_Chemin = DataArray(
        data=numpy.full((len(Chemin), len(Y), len(X)), numpy.nan, dtype=object),
        coords={'X': X, 'Y': Y, 'Chemin': Chemin},
        dims=('Chemin', 'Y', 'X')
    )

    # =========================
    # FILL LOGIC
    # =========================
    mem_type = ""
    mode = False
    n = 0

    for _, row in df.iterrows():

        text = str(row[col])
        idx = row["index"]

        if 'Max Like' in text:
            mem_type = "Max Like"

        elif 'Max Post' in text:
            mem_type = "Max Post"

        elif 'EXPECTED' in text:
            mem_type = "EXPECTED"

        elif 'MODE' in text:
            mode = "END" not in text

        elif 'Sample ID' in text:

            # =========================
            # CASE STANDARD (Like/Post)
            # =========================
            if 'Sample ID =' not in text:

                if mem_type != "EXPECTED":

                    data_tempo = text.split()
                    sample_ID = int(data_tempo[2])

                    nb_constrain = int(data.iloc[idx + 1, 0])
                    nb_point = int(data.iloc[idx + 2 + nb_constrain, 0]) + 1

                    start = idx + 3

                    block = data.iloc[start:start + nb_point, 0]
                    block = block.str.split(expand=True)
                    if len(block.columns)> 2 :
                        block.columns = ["Time", "Temp", "Gradient", "?"]
                    else :
                        block.columns = ["Time", "Temp"]
                        
                    sample = sample_list.get_sample_by_id(sample_ID)
                        
                    data_Chemin[n, 0, 2] = sample
                    data_Chemin[n, 1, 2] = mem_type

                    data_Chemin[n, :nb_point, 0] = block["Time"]
                    data_Chemin[n, :nb_point, 1] = block["Temp"]

                    data_Chemin[n, nb_point:, 0] = numpy.nan
                    data_Chemin[n, nb_point:, 1] = numpy.nan

                    n += 1

            # =========================
            # EXPECTED CASE
            # =========================
            else:

                if not mode:

                    data_tempo = text.split()
                    sample_ID = int(data_tempo[3])

                    nb_point = int(str(data.iloc[idx + 1, 0]).split()[0])
                    start = idx + 2

                    block = data.iloc[start:start + nb_point, 0]
                    block = block.str.split(expand=True)
                    
                    # garder uniquement les colonnes utiles
                    block = block.iloc[:, :5].copy()
                    block.columns = [
                        "Time", "T_Expected", "T_Mode",
                        "T_env_sup", "T_env_inf"
                    ]
                    
                    sample = sample_list.get_sample_by_id(sample_ID)
                    block['Time'] = to_numeric(block['Time'])
                    sample.max_time_ = block['Time'].max()

                    data_Chemin[n, 0, 2] = sample
                    data_Chemin[n, 1, 2] = "EXPECTED"
                    data_Chemin[n, :nb_point, 0] = block["Time"]
                    data_Chemin[n, :nb_point, 1] = block["T_Expected"]
                    data_Chemin[n, nb_point:, 0] = numpy.nan
                    data_Chemin[n, nb_point:, 1] = numpy.nan
                    
                    n += 1
                    
                    data_Chemin[n, 0, 2] = sample
                    data_Chemin[n, 1, 2] = "Max Mode"
                    data_Chemin[n, :nb_point, 0] = block["Time"]
                    data_Chemin[n, :nb_point, 1] = block["T_Mode"]
                    data_Chemin[n, nb_point:, 0] = numpy.nan
                    data_Chemin[n, nb_point:, 1] = numpy.nan
                    
                    n += 1
                    
                    data_Chemin[n, 0, 2] = sample
                    data_Chemin[n, 1, 2] = "Envelope sup."
                    data_Chemin[n, :nb_point, 0] = block["Time"]
                    data_Chemin[n, :nb_point, 1] = block["T_env_sup"]
                    data_Chemin[n, nb_point:, 0] = numpy.nan
                    data_Chemin[n, nb_point:, 1] = numpy.nan
                    
                    n += 1
                    
                    data_Chemin[n, 0, 2] = sample
                    data_Chemin[n, 1, 2] = "Envelope inf."
                    data_Chemin[n, :nb_point, 0] = block["Time"]
                    data_Chemin[n, :nb_point, 1] = block["T_env_inf"]
                    data_Chemin[n, nb_point:, 0] = numpy.nan
                    data_Chemin[n, nb_point:, 1] = numpy.nan
                    
                    n += 1

    return data_Chemin

# === He AGES === # def extract_He_Ages(data, data_He_Maxlike, data_He_MaxPost, data_He_Expect):

def extract_He_Ages(data):

    col = data.columns[0]

    # --- Filtrage ---
    mask = data[col].str.contains(
        'Max Like|Max Post|EXPECTED|File Name|He =|HeR',
        na=False
    )

    df = data.loc[mask].copy().reset_index(drop=False)

    nb_ech = int(data.iloc[0, 0])

    results = []

    # mémoire
    mem_type = ""
    mem_expected = 1
    Expected = False
    nom_ech = ""
    nb_He = 0

    last_valid_idx = None  # remplace "mem"

    # =========================
    # PARSING
    # =========================
    for _, row in df.iterrows():

        text = str(row[col])
        idx = row["index"]

        # --- TYPE ---
        if 'Max Like' in text:
            mem_type = text
            continue

        elif 'Max Post' in text:
            mem_type = text
            continue

        elif 'EXPECTED' in text:
            mem_type = text
            Expected = True
            mem_expected = 0
            continue

        # --- FILE NAME ---
        elif 'File Name =' in text:

            if Expected:
                mem_expected += 1
                if mem_expected > 2:
                    mem_expected = 1

            parts = text.split('/')
            nom_ech = parts[-1]
            
            #clean file name to avoid bug after during filter:
            nom_ech = utils.clean_name(nom_ech)

            results.append(f"{nom_ech} t {mem_type} {mem_expected}")
            continue

        # --- HeR ---
        elif 'HeR =' in text:

            new_text = text.replace("HeR =", f"He_{nom_ech}")
            new_text = new_text.replace("Pred Age", f"{mem_type} {mem_expected}")

            results.append(new_text)
            continue

        # --- He ---
        elif 'NFT =' in text:
            continue

        elif 'He =' in text:

            parts = text.split()

            try:
                val = int(parts[2])
                
            except:
                continue

            if val == 0:
                # supprimer la ligne précédente (équivalent mem)
                if last_valid_idx is not None and len(results) > 0:
                    results.pop()
                continue
            else:
                nb_He = max(nb_He, val)
                continue

        

        # --- fallback ---
        last_valid_idx = idx

    # =========================
    # CONSTRUCTION DF
    # =========================
    if nb_He == 0:
        return '', '', ''

    He_Age = (
        Series(results)
        .str.replace("Max ", "Max-")
        .str.split(expand=True)
    )
    
    He_Age.rename(columns={
        0: "Nom",
        1: "Rs",
        2: "type",
        3: "type_bis",
        5: "Pred_ages",
        9: "Obs_age",
        12: "Error",
        18: "Tc",
        19: "Crystal",
        22: "eU",
        25: "Ft",
        28: "Cor_Pred_age"
    }, inplace=True)    
    
    # =========================
    # DIMENSIONS
    # =========================
    nb_ech = He_Age[
        He_Age.Rs.str.contains('t', na=False) &
        He_Age.type.str.contains('Max-Like', na=False)
    ].shape[0]
    
    X = range(10)    
    
    if nb_He == 1:
        Y = range(nb_He + 1)
    else:
        Y = range(nb_He)

    echantillon = range(nb_ech)

    def init_array():
        return DataArray(
            data=numpy.full((len(echantillon), len(Y), len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon', 'Y', 'X')
        )

    data_He_Maxlike = init_array()
    data_He_MaxPost = init_array()
    data_He_Expect = init_array()

    # =========================
    # INITIALISATION NOMS
    # =========================
    like = He_Age[
        He_Age.Rs.str.contains('t', na=False) &
        He_Age.type.str.contains('Max-Like', na=False)
    ]

    post = He_Age[
        He_Age.Rs.str.contains('t', na=False) &
        He_Age.type.str.contains('Max-Post', na=False)
    ]

    expect = He_Age[
        He_Age.Rs.str.contains('t', na=False) &
        He_Age.type.str.contains('EXPECTED', na=False) &
        He_Age.type_bis.astype(str).str.contains('1', na=False)
    ]

    data_He_Maxlike[:, 0, 8] = like.Nom.values
    data_He_Maxlike[:, 1, 8] = like.type.values

    data_He_MaxPost[:, 0, 8] = post.Nom.values
    data_He_MaxPost[:, 1, 8] = post.type.values

    data_He_Expect[:, 0, 8] = expect.Nom.values
    data_He_Expect[:, 1, 8] = expect.type.values

    # =========================
    # REMPLISSAGE VIA UTIL
    # =========================
    for n in echantillon:

        ech = data_He_Maxlike[n, 0, 8].values

        utils.get_He(n, ech, nb_He, data_He_Maxlike, He_Age, 'Max-Like')
        utils.get_He(n, ech, nb_He, data_He_MaxPost, He_Age, 'Max-Post')
        utils.get_He(n, ech, nb_He, data_He_Expect, He_Age, 'EXPECTED')

    # =========================
    # CALCUL ERREURS
    # =========================
    for n in echantillon:

        data_He_Maxlike[n,:,1] = (
            data_He_Maxlike[n,:,3].astype(float) /
            data_He_Maxlike[n,:,2].astype(float) *
            data_He_Maxlike[n,:,0].astype(float)
        )

        data_He_MaxPost[n,:,1] = (
            data_He_MaxPost[n,:,3].astype(float) /
            data_He_MaxPost[n,:,2].astype(float) *
            data_He_MaxPost[n,:,0].astype(float)
        )

        data_He_Expect[n,:,1] = (
            data_He_Expect[n,:,3].astype(float) /
            data_He_Expect[n,:,2].astype(float) *
            data_He_Expect[n,:,0].astype(float)
        )

    return data_He_Maxlike, data_He_MaxPost, data_He_Expect

# === FT AGES === # def extract_He_Ages(data, data_He_Maxlike, data_He_MaxPost, data_He_Expect)

def extract_FT_Ages(data):

    col = data.columns[0]

    # =========================
    # FILTRAGE + INDEX SAFE
    # =========================
    mask = data[col].str.contains(
        'Max Like|Max Post|EXPECTED|File Name|Pred FT age',
        na=False
    )

    df = data.loc[mask].copy().reset_index(drop=False)

    # =========================
    # PARSING (STATE MACHINE)
    # =========================
    mem_type = ""
    mem_nom = ""
    mem_expected = 0
    expected_flag = False

    rows_out = []

    for _, row in df.iterrows():

        text = str(row[col])
        idx = row["index"]

        # -------- TYPE --------
        if 'Max Like' in text:
            mem_type = "Max_Like"
            continue

        elif 'Max Post' in text:
            mem_type = "Max_Post"
            continue

        elif 'EXPECTED' in text:
            mem_type = "EXPECTED"
            expected_flag = True
            continue

        # -------- FILE NAME --------
        elif 'File Name =' in text:

            if expected_flag:
                mem_expected += 1
                if mem_expected > 2:
                    mem_expected = 1

            name = text.split('/')[-1]
            name = utils.clean_name(name)
            mem_nom = name

            continue

        # -------- MAIN DATA --------
        elif 'Pred FT age =' in text:

            parts = text.split()

            # sécurité parsing
            try:
                if float(parts[5]) == -1:
                    continue
            except:
                continue

            # ⚠️ récupération robuste
            tempo = str(data.iloc[idx + 4, 0])

            new_line = text.replace(
                "Pred FT",
                f"{mem_nom} {mem_type} {mem_expected}"
            )

            full_line = f"{new_line} {tempo}"

            rows_out.append(full_line)

    # =========================
    # PAS DE DATA
    # =========================
    if not rows_out:
        return '', '', ''

    # =========================
    # TABLE
    # =========================
    FT_Age_tab = (
        Series(rows_out)
        .str.split(expand=True)
    )

    FT_Age_tab = FT_Age_tab.rename(columns={
        0: "nom",
        1: "type",
        2: "expect",
        5: "Pred_ages",
        6: "Obs_ages",
        20: "Obs_ages_error",
        39: "Pred_kin",
        40: "Obs_kin",
        41: "Obs_kin_error"
    })
    
    FT_Age_tab["Obs_ages_error"] = FT_Age_tab["Obs_ages_error"].replace("-1.#IND00", "0")

    
    # =========================
    # NB
    # =========================
    nb_FT = FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')].shape[0]

    # =========================
    # XARRAY INIT (INCHANGÉ)
    # =========================
    X = range(10)
    Y = range(1)
    echantillon = range(nb_FT)

    def make_array():
        return DataArray(
            data=numpy.full((len(echantillon), len(Y), len(X)), numpy.nan, dtype=object),
            coords={'X': X, 'Y': Y, 'echantillon': echantillon},
            dims=('echantillon', 'Y', 'X')
        )

    data_FT_like = make_array()
    data_FT_post = make_array()
    data_FT_expect = make_array()

    # =========================
    # FILL FUNCTION
    # =========================
    def fill(arr, df):
        arr[:, 0, 0] = df.Pred_ages
        arr[:, 0, 1] = df.Obs_ages
        arr[:, 0, 2] = df.Obs_ages_error
        arr[:, 0, 4] = df.nom
        arr[:, 0, 5] = df.type
        arr[:, 0, 6] = df.Pred_kin
        arr[:, 0, 8] = df.Obs_kin
        arr[:, 0, 9] = df.Obs_kin_error

    # =========================
    # SPLIT DATA
    # =========================
    df_like = FT_Age_tab[FT_Age_tab.type.str.contains('Max_Like')]
    df_post = FT_Age_tab[FT_Age_tab.type.str.contains('Max_Post')]
    df_expect = FT_Age_tab[
        (FT_Age_tab.type.str.contains('EXPECTED')) &
        (FT_Age_tab.expect.str.contains('1'))
    ]

    fill(data_FT_like, df_like)
    fill(data_FT_post, df_post)
    fill(data_FT_expect, df_expect)

    # =========================
    # CALCULS (inchangés)
    # =========================
    def compute(arr):
        arr[:, 0, 3] = (
            arr[:, 0, 2].astype(float) /
            arr[:, 0, 1].astype(float) *
            arr[:, 0, 0].astype(float)
        )
        arr[:, 0, 7] = (
            arr[:, 0, 9].astype(float) /
            arr[:, 0, 8].astype(float) *
            arr[:, 0, 6].astype(float)
        )

    compute(data_FT_like)
    compute(data_FT_post)
    compute(data_FT_expect)

    return data_FT_like, data_FT_post, data_FT_expect


# === FT LENGTH === # def extract_He_Ages(data, data_He_Maxlike, data_He_MaxPost, data_He_Expect)

def extract_FT_Length(data):

    col = data.columns[0]

    # --- Détection du format ---
    has_lc0 = data[col].str.contains('Lc0', na=False).any()

    if has_lc0:
        LFT_marker = 'Lc0 '
        LFT_shift = 0
    else:
        LFT_marker = '1 0.100000 0.000000 0.000000 0.000000'
        LFT_shift = 1

    # --- Filtrage utile ---
    mask = data[col].str.contains(
        f'Max Like|Max Post|EXPECTED|File Name|{LFT_marker}',
        na=False
    )

    df = data.loc[mask].copy().reset_index(drop=False)

    results = []

    # mémoire
    mem_type = ""
    mem_nom = ""
    mem_expected = 0
    Expected = False

    # --- Parsing propre ---
    for _, row in df.iterrows():

        text = str(row[col])
        original_idx = row["index"]

        if 'Max Like' in text:
            mem_type = text.replace(" ", "_")
            continue

        elif 'Max Post' in text:
            mem_type = text.replace(" ", "_")
            continue

        elif 'EXPECTED' in text:
            mem_type = text.replace(" ", "_")
            Expected = True
            continue

        elif 'File Name =' in text:

            if Expected:
                mem_expected += 1
                if mem_expected > 2:
                    mem_expected = 1

            nom = text.split('/')[-1]         
            nom = utils.clean_name(nom)
            mem_nom = nom

            continue

        elif LFT_marker in text:

            results.append({
                "nom": mem_nom,
                "type": mem_type,
                "expect": mem_expected,
                "idx": original_idx
            })

    if not results:
        return None

    FT_Length_tab = DataFrame(results)

    # --- Dimensions ---
    nb_ech = FT_Length_tab[FT_Length_tab.type.str.contains('Max_Like', na=False)].shape[0]

    X = range(6)
    Y = range(200)
    echantillon = range(nb_ech)

    data_FT_Lenght = DataArray(
        data=numpy.full((len(echantillon), len(Y), len(X)), numpy.nan, dtype=object),
        coords={'X': X, 'Y': Y, 'echantillon': echantillon},
        dims=('echantillon', 'Y', 'X')
    )

    # --- Axe longueur ---
    for n in range(len(echantillon)):
        data_FT_Lenght[n, :, 0] = numpy.arange(0, 20, step=0.1)

    # =========================
    # OBSERVED (Max Like)
    # =========================
    subset = FT_Length_tab[FT_Length_tab.type.str.contains('Max_Like', na=False)].reset_index(drop=True)

    for n, row in subset.iterrows():

        a = row["idx"]

        obs = data.iloc[a - 20 : a - 2, 0]
        obs = obs.str.split(expand=True)
        obs.columns = ["lenght", "curve", "bar"]

        arr = numpy.full((20, 10), numpy.nan)
        arr[1:19, 0] = obs["bar"].astype(float)

        data_FT_Lenght[n, :, 1] = arr.ravel()
        data_FT_Lenght[n, 0, 5] = row["nom"]

    # =========================
    # PREDICTIONS
    # =========================
    def fill_pred(column_idx, subset):

        subset = subset.reset_index(drop=True)

        for n, row in subset.iterrows():

            a = row["idx"]

            pred = data.iloc[a + 1 - LFT_shift : a + 201 - LFT_shift, 0]
            pred = pred.str.split(expand=True)

            # garder uniquement les colonnes utiles
            pred = pred.iloc[:, :3].copy()
            pred.columns = ["number", "lenght", "curve"]

            data_FT_Lenght[n, :, column_idx] = pred["curve"].astype(float)

    fill_pred(2, FT_Length_tab[FT_Length_tab.type.str.contains('Max_Like', na=False)])
    fill_pred(3, FT_Length_tab[FT_Length_tab.type.str.contains('Max_Post', na=False)])
    fill_pred(4, FT_Length_tab[FT_Length_tab.expect.astype(str).str.contains('1', na=False)])

    return data_FT_Lenght


# === RESAMPLES PARAMETERS === # def extract_resample(data)

def extract_resample(data):

    nb_sample = int(data.iloc[0,0])
    nb_iteration= int(data.iloc[1 + nb_sample, 0])

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
    #step_iteration = int(tab_data.iloc[0].str.split(' ', n=-1, expand=True)[0])
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

