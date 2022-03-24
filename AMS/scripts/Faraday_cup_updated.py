%matplotlib qt5

import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.colors
from scipy.signal import find_peaks

# %%
# function definitions

def mass_calib_LE(I):
    #return 25.0*(I/61.17)**2 - 0.012*I + 0.55
    return 25.0*(I/61.05)**2

def list_shallow_flatten(list_of_lists):
    ret_list = []
    for list in list_of_lists:
        for element in list:
            ret_list.append(element)
    return ret_list

def closest_nuclide(nuclide_list, val):
    masses = np.array([nuclide_list[i][0] for i in range(0, len(nuclide_list), 1)])
    diffs = np.abs(masses - val)
    return nuclide_list[diffs.argmin()][1]

# %%
# data information declaration

prefix = "../Daten/"

#             File Name --- sample name --- intensity scale --- intensity unit --- minimum peak height --- minimum horizontal peak distance (in x-unit)
data_info = [["LEMass40-85pos153BeOTUDPract.asc",    "LE BeO", -1/100, "A", 1.0e-12, 0.7],
             ["LEMass40-85pos173KY13STUDPract.asc",  "KY13_1", -1/100, "A", 1.0e-12, 0.7],
             ["LEMass40-85pos173KY13STUDPract2.asc", "KY13_2", -1/100, "A", 1.0e-12, 0.7],
             ["LEMass40-85pos174KY14TUDPract.asc",   "KY14",   -1/100, "A", 1.0e-12, 0.7],
             ["LEMass40-85pos175KY16TUDPract.asc",   "KY16",   -1/100, "A", 1.0e-12, 0.7],
             ["LEMass40-85pos176KY17TUDPract.asc",   "KY17",   -1/100, "A", 1.0e-12, 0.7]
            ]

#             Mass --- Name
nuclide_list = [[9, r"$^{9}Be^{1-}$"],
                [12, r"$^{12}C^{1-}$"],
                [13, r"$^{13}C^{1-}$"],
                [14, r"$^{14}N^{1-}$"],
                [16, r"$^{16}O^{1-}$"],
                [17, r"$^{16}O^{1}H^{1-}$"],
                [18, r"$^{9}Be_{2}^{1-}$" + "\n" + r"$^{18}O^{1-}$"],
                [19, r"$^{18}O^{1}H^{1-}$"],
                [21, r"$^{9}Be^{12}C^{1-}$"],
                [23, r"$^{9}Be^{14}N^{1-}$"],
                [24, r"$^{12}C_{2}^{1-}$"],
                [25, r"$^{9}Be^{16}O^{1-}$"],
                [26, r"$^{9}Be^{16}O^{1}H^{1-}$" + "\n" + r"$^{10}B^{16}O^{1-}$"],
                [27, r"$^{27}Al^{1-}$"],
                [28, r"$^{12}C^{16}O^{1-}$" + "\n" + r"$^{28}Si^{1-}$"],
                [29, r"$^{29}Si^{1-}$"],
                [30, r"$^{30}Si^{1-}$"],
                [31, r"$^{31}P^{1-}$"],
                [32, r"$^{32}S^{1-}$" + "\n" + r"$^{16}O_{2}^{1-}$"],
                [33, r"$^{33}S^{1-}$"],
                [34, r"$^{34}S^{1-}$"],
                [35, r""]
               ]

# %%
#

data_loaded = []
for i in range(0, len(data_info), 1):
    data_loaded.append(np.loadtxt(prefix + data_info[i][0], delimiter=' ', skiprows=21, usecols = (0,1)).transpose())
    data_loaded[i][1] *= data_info[i][2]

data_peaks_found = []
data_peaks_values = []
for i in range(0, len(data_info), 1):
    scale_fac = data_loaded[i].shape[1]/(np.max(data_loaded[i][0]) - np.min(data_loaded[i][0]))
    min_dist = int(data_info[i][5]*scale_fac) # minimum horizontal distance between peaks
    data_peaks.append(find_peaks(np.abs(data_loaded[i][1]), height = data_info[i][4], distance = min_dist)[0])
    data_peaks_values.append([])
# peak correction
    for j in range(0, len(data_peaks[i]), 1): # for each found peak
        left_idx = data_peaks[i][j]
        right_idx = data_peaks[i][j]
        for l in range(1, min_dist+1, 1): # shift up to peak width to left
            if (data_peaks[i][j] - l >= 0):
                if np.abs(data_loaded[i][1][data_peaks[i][j] - l]) >= data_info[i][4]:
                    left_idx = data_peaks[i][j] - l
                else:
                    break
            else:
                break

        for l in range(1, min_dist+1, 1): # shift up to peak width to right
            if (data_peaks[i][j] + l < len(data_loaded[i][1])):
                if np.abs(data_loaded[i][1][data_peaks[i][j] + l]) >= data_info[i][4]:
                    right_idx = data_peaks[i][j] + l
                else:
                    break
            else:
                break
        data_peaks[i][j] = (np.sum(np.arange(left_idx, right_idx+1, 1) * data_loaded[i][1, left_idx:right_idx+1]) / np.sum(data_loaded[i][1, left_idx:right_idx+1])) + 1
        data_peaks_values[i].append(mass_calib_LE(np.sum(data_loaded[i][0, left_idx:right_idx+1] * data_loaded[i][1, left_idx:right_idx+1]) / np.sum(data_loaded[i][1, left_idx:right_idx+1])))

data_filtered = []
for i in range(0, len(data_info), 1):
    data_filtered.append(data_loaded[i][:, data_loaded[i][1] != data_info[i][2] * 9.990e+002])

# %%

plot_nums = [0, 1, 2]
color_cycle = ["olivedrab", "mediumblue", "firebrick", "grey"]
label_x_offset = 0.2
spectra_alpha = 0.4
font_size = 14
font_alpha = 0.75

fig = plt.figure(figsize=(22, 11))
ax = fig.add_subplot()

for i in range(0, len(plot_nums), 1):
    ax.plot(mass_calib_LE(data_loaded[plot_nums[i]][0]),                             # spectra
            np.abs(data_loaded[plot_nums[i]][1]),
            label = data_info[plot_nums[i]][1],
            color = color_cycle[i % len(color_cycle)],
            alpha = spectra_alpha)

    peak_plot_y = np.where(np.abs(data_loaded[plot_nums[i]][1][data_peaks[plot_nums[i]]]) < np.max(data_filtered[plot_nums[i]][1]), data_loaded[plot_nums[i]][1][data_peaks[plot_nums[i]]], np.max(data_filtered[plot_nums[i]][1]))

    ax.plot(data_peaks_values[plot_nums[i]],     # peaks
            peak_plot_y,
            "x",
            color = color_cycle[i % len(color_cycle)])

    for j in range(0, len(data_peaks[plot_nums[i]]), 1):                    # peak labels
        ax.text(mass_calib_LE(data_loaded[plot_nums[i]][0][data_peaks[plot_nums[i]]][j]) + label_x_offset,
                peak_plot_y[j],
                closest_nuclide(nuclide_list, data_peaks_values[plot_nums[i]][j]) + "\n" + str(np.round(data_peaks_values[plot_nums[i]][j], 1)),
                fontsize = font_size,
                alpha =font_alpha)

ax.set_yscale('log')
ax.set_ylim(np.min([data_info[num][4] for num in plot_nums]) * 0.5, np.max(list_shallow_flatten([data_filtered[plot_nums[i]][1] for i in range(0, len(plot_nums), 1)])) * 3)
ax.legend(fontsize=font_size)
ax.tick_params(axis='both', labelsize = font_size)
ax.set_xlabel(r"Ionenmasse $[u]$", fontsize = font_size)
ax.set_ylabel(r"Intensität $[A]$", fontsize = font_size)
fig.subplots_adjust(bottom=0.06, top=0.95, left=0.05, right=0.98)
plt.show()
