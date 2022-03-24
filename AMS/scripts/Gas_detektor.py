import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

# Einstellungen

prefix = "../Daten/"

names = np.array(["3.mpa",
                  "19.mpa",
                  "22.mpa"])    # Dateien = prefix + names[i]

live_times = np.array([1245.252,
                       845.399,
                       474.138])


name_AB = "NAME=AxB"    # Identifizierung für A-B-Spektren
name_CD = "NAME=CxD"    # Identifizierung für C-D-Spektren
name_AC = "NAME=AxC"    # Identifizierung für C-D-Spektren
name_begin = "[DATA]"   # Zeile/Zeichen vor Beginn der Daten
name_end = "["          # Zeile/Zeichen vor Ende der Daten
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
data_file_idx_AC = np.empty((N_names, 2), dtype = int)  # Array für Index (Anfang & Ende) der Zeilen
for i in np.arange(0, N_names, 1):
    data_file_idx_AB[i] = get_file_block_idx(prefix + names[i], name_AB, name_begin, name_end)
    data_file_idx_CD[i] = get_file_block_idx(prefix + names[i], name_CD, name_begin, name_end)
    data_file_idx_AC[i] = get_file_block_idx(prefix + names[i], name_AC, name_begin, name_end)

data_raw = np.empty((N_names, 3), dtype=np.ndarray) # dim 0: für jede Datei, dim 1: AB / CD / ...
for i in np.arange(0, N_names, 1):
    data_raw[i, 0] = np.loadtxt(prefix + names[i],
                                dtype = int,
                                skiprows = data_file_idx_AB[i, 0],
                                max_rows = data_file_idx_AB[i, 1] - data_file_idx_AB[i, 0])
    data_raw[i, 1] = np.loadtxt(prefix + names[i],
                                dtype = int,
                                skiprows = data_file_idx_CD[i, 0],
                                max_rows = data_file_idx_CD[i, 1] - data_file_idx_CD[i, 0])
    data_raw[i, 2] = np.loadtxt(prefix + names[i],
                                dtype = int,
                                skiprows = data_file_idx_AC[i, 0],
                                max_rows = data_file_idx_AC[i, 1] - data_file_idx_AC[i, 0])

data_fill = np.zeros((N_names, 3, data_len, data_len)) # Umwandlung in sinnvollen Datentyp, von Indizes zu gefülltem Array
for i in np.arange(0, N_names, 1):
    data_fill[i, 0, np.transpose(data_raw[i, 0])[1], np.transpose(data_raw[i, 0])[0]] = np.transpose(data_raw[i, 0])[2]
    data_fill[i, 1, np.transpose(data_raw[i, 1])[1], np.transpose(data_raw[i, 1])[0]] = np.transpose(data_raw[i, 1])[2]
    data_fill[i, 2, np.transpose(data_raw[i, 2])[1], np.transpose(data_raw[i, 2])[0]] = np.transpose(data_raw[i, 2])[2]

# %%

# --- Plotten ---

# Plot-Einstellungen

plot_num = 0 # Nummer der Datei in names, die geplottet wird
ref_num = 2 # Nummer der Referenzdatei
max_xy = 160 # Maximum der x/y-Achse

color_scale = 0.5 # Skalierung um Farben an den Rändern interessanter Bereiche schöner zu machen
fsize = 16 # Schriftgröße
colormap_name_one = "YlOrBr"
colormap_name_ref = "RdGy" # Farbschema

# %%

# Plotten einzelne Spektren

AB_plot_data = data_fill[plot_num, 0, 0:max_xy+1, 0:max_xy+1]/live_times[plot_num]
CD_plot_data = data_fill[plot_num, 1, 0:max_xy+1, 0:max_xy+1]/live_times[plot_num]
AC_plot_data = data_fill[plot_num, 2, 0:max_xy+1, 0:max_xy+1]/live_times[plot_num]

scale = np.max(np.abs([AB_plot_data, CD_plot_data, AC_plot_data]))*color_scale

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot()

im = ax.imshow(AB_plot_data,
               origin = "lower",
               cmap = colormap_name_one,
               aspect = "equal",
               interpolation = "none",
               vmin = 0, vmax=scale)

ax.set_xlabel("Anode A", fontsize = fsize)
ax.set_ylabel("Anode B", fontsize = fsize)
ax.tick_params(axis='both', labelsize = fsize)
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=fsize)
cbar.set_label(r"#Kanal / $t_{live}\ [1/s]$", fontsize=fsize)

plt.subplots_adjust(left=0.1, right=0.88, top=0.99, bottom=0.05)

# fig.savefig("../Protokoll/Pictures/Gasdetektor/Gasdetektor_2DSpektrum_" + names[plot_num][:-4] +".png", format="png")

plt.show()

# --------

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot()

im = ax.imshow(CD_plot_data,
               origin = "lower",
               cmap = colormap_name_one,
               aspect = "equal",
               interpolation = "none",
               vmin = 0, vmax=scale)

ax.set_xlabel("Anode C", fontsize = fsize)
ax.set_ylabel("Anode D", fontsize = fsize)
ax.tick_params(axis='both', labelsize = fsize)
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=fsize)
cbar.set_label(r"#Kanal / $t_{live}\ [1/s]$", fontsize=fsize)

plt.subplots_adjust(left=0.1, right=0.88, top=0.99, bottom=0.05)

# fig.savefig("../Protokoll/Pictures/Gasdetektor/Gasdetektor_2DSpektrum_" + names[plot_num][:-4] +".png", format="png")

plt.show()

# --------

fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot()

im = ax.imshow(AC_plot_data,
               origin = "lower",
               cmap = colormap_name_one,
               aspect = "equal",
               interpolation = "none",
               vmin = 0, vmax=scale)

ax.set_xlabel("Anode A", fontsize = fsize)
ax.set_ylabel("Anode C", fontsize = fsize)
ax.tick_params(axis='both', labelsize = fsize)
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=fsize)
cbar.set_label(r"#Kanal / $t_{live}\ [1/s]$", fontsize=fsize)

plt.subplots_adjust(left=0.1, right=0.88, top=0.99, bottom=0.05)

# fig.savefig("../Protokoll/Pictures/Gasdetektor/Gasdetektor_2DSpektrum_" + names[plot_num][:-4] +".png", format="png")

plt.show()

# %%

# Plotten Abweichung

AB_plot_data = data_fill[plot_num, 0, 0:max_xy+1, 0:max_xy+1]/live_times[plot_num] - data_fill[ref_num, 0, 0:max_xy+1, 0:max_xy+1]/live_times[ref_num]
CD_plot_data = data_fill[plot_num, 1, 0:max_xy+1, 0:max_xy+1]/live_times[plot_num] - data_fill[ref_num, 1, 0:max_xy+1, 0:max_xy+1]/live_times[ref_num]

scale = np.max(np.abs([AB_plot_data, CD_plot_data]))*color_scale

if (ref_num != plot_num):

    fig = plt.figure(figsize=(16, 8))

    grid = ImageGrid(fig, 111,
                    nrows_ncols=(1,2),
                    axes_pad=1.0,
                    share_all=False,
                    label_mode = "all",
                    cbar_location="right",
                    cbar_mode="single",
                    cbar_size="7%",
                    cbar_pad=0.15)

    # Add data to image grid

    im = grid[0].imshow(AB_plot_data,
                        origin = "lower",
                        cmap = colormap_name_ref,
                        aspect = "equal",
                        interpolation = "none",
                        vmin = -scale, vmax=scale)
    im = grid[1].imshow(CD_plot_data,
                        origin = "lower",
                        cmap = colormap_name_ref,
                        aspect = "equal",
                        interpolation = "none",
                        vmin = -scale, vmax=scale)

    # Colorbar

    grid[0].set_xlabel("Anode A", fontsize = fsize)
    grid[0].set_ylabel("Anode B", fontsize = fsize)
    grid[0].tick_params(axis='both', labelsize = fsize)

    grid[1].set_xlabel("Anode C", fontsize = fsize)
    grid[1].set_ylabel("Anode D", fontsize = fsize)
    grid[1].tick_params(axis='both', labelsize = fsize)

    cbar = grid[1].cax.colorbar(im)
    cbar.ax.tick_params(labelsize=fsize)
    grid[1].cax.toggle_label(True)

    plt.tight_layout()    # Works, but may still require rect paramater to keep colorbar labels visible

#    fig.savefig("../Protokoll/Pictures/Gasdetektor/Gasdetektor_2DSpektrum_" + names[plot_num][:-4] + "_relativ_zu_" + names[ref_num][:-4] + ".png", format="png")

    plt.show()

else:
    print("Err.: reference is equal to sample.")
