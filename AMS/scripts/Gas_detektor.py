import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

# Einstellungen

prefix = "../Daten/"

names = np.array(["3.mpa",
                  "19.mpa",
                  "22.mpa"])    # Dateien = prefix + names[i]

name_AB = "NAME=AxB"    # Identifizierung für A-B-Spektren
name_CD = "NAME=CxD"    # Identifizierung für C-D-Spektren
name_begin = "[DATA]"   # Zeile/Zeichen vor Beginn der Daten
name_end = "["          # Zeile/Zeichen vor Beginn der Daten
data_len = 256

# %%

def get_file_block_idx(filepath, search_str, start_str, end_str): # Ermittelt Index von Start und Ende der Daten im File. Gibt 0, 0 zurück wenn nicht gefunden.
    with open(filepath) as temp_f:
        all_lines = temp_f.readlines()
    for i in np.arange(0, len(all_lines), 1):
        if all_lines[i].startswith(search_str):
            for j in np.arange(i+1, len(all_lines), 1):
                if all_lines[j].startswith(start_str):
                    for l in np.arange(j+1, len(all_lines), 1):
                        if all_lines[l].startswith(end_str):
                            return j+1, l
    return 0, 0

# --- Daten einlesen ---

N_names = names.size # Anzahl Dateien

data_file_idx_AB = np.empty((N_names, 2), dtype = int)  # Array für Index (Anfang & Ende) der Zeilen
data_file_idx_CD = np.empty((N_names, 2), dtype = int)  # Array für Index (Anfang & Ende) der Zeilen
for i in np.arange(0, N_names, 1):
    data_file_idx_AB[i] = get_file_block_idx(prefix + names[i], name_AB, name_begin, name_end)
    data_file_idx_CD[i] = get_file_block_idx(prefix + names[i], name_CD, name_begin, name_end)

data_raw = np.empty((N_names, 2), dtype=np.ndarray) # dim 0: für jede Datei, dim 1: AB / CD
for i in np.arange(0, N_names, 1):
    data_raw[i, 0] = np.loadtxt(prefix + names[i],
                                dtype = int,
                                skiprows = data_file_idx_AB[i, 0],
                                max_rows = data_file_idx_AB[i, 1] - data_file_idx_AB[i, 0])
    data_raw[i, 1] = np.loadtxt(prefix + names[i],
                                dtype = int,
                                skiprows = data_file_idx_CD[i, 0],
                                max_rows = data_file_idx_CD[i, 1] - data_file_idx_CD[i, 0])

data_fill = np.zeros((N_names, 2, data_len, data_len)) # Umwandlung in sinnvollen Datentyp, von Indizes zu gefülltem Array
for i in np.arange(0, N_names, 1):
    data_fill[i, 0, np.transpose(data_raw[i, 0])[1], np.transpose(data_raw[i, 0])[0]] = np.transpose(data_raw[i, 0])[2]
    data_fill[i, 1, np.transpose(data_raw[i, 1])[1], np.transpose(data_raw[i, 1])[0]] = np.transpose(data_raw[i, 1])[2]

# %%

# --- Plotten ---

# Plot-Einstellungen

plot_num = 2 # Nummer der Datei in names, die geplottet wird
max_xy = 160 # Maximum der x/y-Achse

fsize = 16 # Schriftgröße
colormap_name = "YlOrBr" # Farbschema

# Plotten

fig = plt.figure(figsize=(16, 8))
axAB = fig.add_subplot(1, 2, 1)
axCD = fig.add_subplot(1, 2, 2)

axAB.imshow(data_fill[plot_num, 0, 0:max_xy+1, 0:max_xy+1],
            origin = "lower",
            cmap = colormap_name,
            aspect = "equal",
            interpolation = "none")
axCD.imshow(data_fill[plot_num, 1, 0:max_xy+1, 0:max_xy+1],
            origin = "lower",
            cmap = colormap_name,
            aspect = "equal",
            interpolation = "none")

axAB.set_xlabel("Anode A", fontsize = fsize)
axAB.set_ylabel("Anode B", fontsize = fsize)
axAB.tick_params(axis='both', labelsize = fsize)

axCD.set_xlabel("Anode C", fontsize = fsize)
axCD.set_ylabel("Anode D", fontsize = fsize)
axCD.tick_params(axis='both', labelsize = fsize)

fig.tight_layout()

plt.show()
