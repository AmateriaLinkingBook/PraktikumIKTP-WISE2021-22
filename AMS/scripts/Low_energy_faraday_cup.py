import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from itertools import combinations

prefix = "../Daten/"
names = np.array(["HEMass60-140pos153BeOTUDPract.asc",
                  "LEMass40-85pos153BeOTUDPract.asc",
                  "LEMass40-85pos173KY13STUDPract.asc",
                  "LEMass40-85pos173KY13STUDPract2.asc",
                  "LEMass40-85pos174KY14TUDPract.asc",
                  "LEMass40-85pos175KY16TUDPract.asc",
                  "LEMass40-85pos176KY17TUDPract.asc"])

intensity_unit = np.array(["%",  # intensity unit
                           "A",
                           "A",
                           "A",
                           "A",
                           "A",
                           "A"])
intensity_factor = np.array([1,
                             -1/100,  # Weil in % angegeben
                             -1/100,  # Weil in % angegeben
                             -1/100,  # Weil in % angegeben
                             -1/100,  # Weil in % angegeben
                             -1/100,  # Weil in % angegeben
                             -1/100]) # Weil in % angegeben
current_unit = "A"
min_peak_height = np.array([1.0e-3,  # minimum height peak has to have, in amounts used in files (y-coordinate (intensity)), for finding peaks
                            1.0e-10,
                            1.0e-10,
                            1.0e-10,
                            1.0e-10,
                            1.0e-10,
                            1.0e-10])
peak_width = 0.5 # approximate width peak can have, in amounts used in files (x-coordinate (mass)), for fitting peaks

# %%

N = names.size

print("aquire Data...\nShapes:")

data = np.empty(N, dtype=pd.DataFrame)
for i in np.arange(0, N, 1):
    data[i] = pd.DataFrame(np.loadtxt(prefix + names[i], delimiter=' ', skiprows=21, usecols = (0,1)),
              columns=["channel", "intensity"])
    print(i, "-", data[i].shape)

print("----------\nShapes after filter:")

for i in np.arange(0, N, 1):
    data[i] = data[i][data[i]["intensity"] != 9.990e+002]
    data[i]["intensity"] *= intensity_factor[i]
    print(i, "-", data[i].shape)

print("Intensity should now be in given units")
print("Finding Peaks...")

peaks = np.empty(N, dtype=np.ndarray)
for i in np.arange(0, N, 1):
    scale_fac = data[i]["channel"].size/(np.max(data[i]["channel"])-np.min(data[i]["channel"]))
    peaks[i] = find_peaks(data[i]["intensity"], height = min_peak_height[i], distance = int(peak_width*scale_fac))[0]
    print(i, "- peak amount:", peaks[i].size)

peak_avg = np.empty(N, dtype=np.ndarray)
for i in np.arange(0, N, 1):
    peak_avg[i] = np.empty(peaks[i].size)
    for j in np.arange(0, peaks[i].size, 1):
        scale_fac = data[i]["channel"].size/(np.max(data[i]["channel"])-np.min(data[i]["channel"]))
        lower_idx = int(np.max([np.floor(peaks[i][j] - peak_width*scale_fac), 0]))
        upper_idx = int(np.min([np.ceil(peaks[i][j] + peak_width*scale_fac), data[i].size-1]))
        peak_avg[i][j] = np.sum(data[i]["channel"].iloc[lower_idx:upper_idx]*data[i]["intensity"].iloc[lower_idx:upper_idx])/np.sum(data[i]["intensity"].iloc[lower_idx:upper_idx])

# %%

# IDENTIFICATION

identify_num = 1

possible_ions = [["16_O_1+", 16, 1],
                 ["16_O_2+", 16, 2],
                 ["16_O_3+", 16, 3],
                 ["16_O_4+", 16, 4],
#                 ["18_O_1+", 18, 1], # rare isotope
#                 ["18_O_2+", 18, 2], # rare isotope
#                 ["18_O_3+", 18, 3], # rare isotope
#                 ["18_O_4+", 18, 4], # rare isotope
                 ["9_Be_1+", 9, 1],
                 ["9_Be_2+", 9, 2],
                 ["9_Be_3+", 9, 3],
                 ["9_Be_4+", 9, 4],
                 ["10_Be_1+", 10, 1],
                 ["10_Be_2+", 10, 2],
                 ["10_Be_3+", 10, 3],
                 ["10_Be_4+", 10, 4],
                 ["26_Al_1+", 26, 1],
                 ["26_Al_2+", 26, 2],
                 ["26_Al_3+", 26, 3],
                 ["26_Al_4+", 26, 4],
                 ]

N_ions = len(possible_ions)
N_peak = len(peak_avg[identify_num])

sorter = np.array([np.sqrt(possible_ions[i][1])/possible_ions[i][2] for i in np.arange(0, N_ions, 1)])
possible_ions_sorted = [possible_ions[i] for i in np.argsort(sorter)]

# for i in np.arange(0, N_ions, 1):
#     print(possible_ions_sorted[i])
"""
# %%
N_overall_recomend = 10

# find best overall combinations

def err_norm(poss_ratio, peak_ratio):
    return(np.sqrt(np.sum(np.square(np.array(poss_ratio)-np.array(peak_ratio)))))

#def err_norm(poss_ratio, peak_ratio):
#    return(np.sum(np.array(poss_ratio)-np.array(peak_ratio)))

all_combinations = list(combinations(possible_ions_sorted, N_peak))
all_combinations_err = np.empty(len(all_combinations))
for i in np.arange(0, len(all_combinations), 1):
    ratio_combs_idx = list(combinations(np.arange(0, N_peak, 1), 2))
    ratio_combs = [[all_combinations[i][n], all_combinations[i][m]] for n,m in ratio_combs_idx]
    all_combinations_err[i] = err_norm(
            [np.sqrt(ratio_combs[l][0][1]/ratio_combs[l][1][1])/(ratio_combs[l][0][2]/ratio_combs[l][1][2]) for l in np.arange(0, len(ratio_combs), 1)],
            [peak_avg[identify_num][ratio_combs_idx[l][0]]/peak_avg[identify_num][ratio_combs_idx[l][1]] for l in np.arange(0, len(ratio_combs), 1)])

best_overall_sorters = np.argsort(all_combinations_err)
sorted_all_combinations = [all_combinations[i] for i in best_overall_sorters]
sorted_all_combinations_err = all_combinations_err[best_overall_sorters]

if N_overall_recomend > len(all_combinations):
    N_overall_recomend = len(all_combinations)

# print best overall combinations

print("----- best overall combinations -----")
print("Top {show:<2} out of {all:<10}".format(show = N_overall_recomend, all = len(all_combinations)))
print("(uncertainty is peak position found-expected difference by norm)")
print("(any norm will do)")

for i in np.arange(0, N_overall_recomend, 1):
    print("--- #" + str(i+1) + " ---")
    for j in np.arange(0, N_peak-1, 1):
        print("@ {item:<12}   ".format(item = str(np.round(peak_avg[identify_num][j], 1)) + " " + current_unit), sep="", end="")
    print("@ {item:<12}   ".format(item = str(np.round(peak_avg[identify_num][N_peak-1], 1)) + " " + current_unit), sep="", end="\n")
    for j in np.arange(0, N_peak-1, 1):
        print("Int. {item:<12}".format(item = str(data[identify_num]["intensity"].iloc[peaks[identify_num][j]]) + " " + intensity_unit[identify_num]), sep="", end="")
    print("@ {item:<12}   ".format(item = str(data[identify_num]["intensity"].iloc[peaks[identify_num][N_peak-1]]) + " " + intensity_unit[identify_num]), sep="", end="\n")
    for j in np.arange(0, N_peak-1, 1):
        print("{item:<12}     ".format(item = sorted_all_combinations[i][j][0]), sep="", end="")
    print("{item:<12}   ".format(item = sorted_all_combinations[i][N_peak-1][0]), sep="", end="\n\n")
    print("uncertainty:", np.round(sorted_all_combinations_err[i], 4), end="\n\n")
"""
# %%

plot_num = 1
fsize = 16

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot()

ax.plot(data[plot_num]["channel"], data[plot_num]["intensity"])
ax.plot(peak_avg[plot_num], data[plot_num]["intensity"].iloc[peaks[plot_num]], ".")
for i in np.arange(0, peaks[plot_num].size, 1):
    ax.text(peak_avg[plot_num][i]+0.5,
            data[plot_num]["intensity"].iloc[peaks[plot_num][i]],
            np.round(peak_avg[plot_num][i], 2),
            fontsize=fsize)

ax.set_yscale('log')
ax.set_ylim(1.0e-10, np.max(data[plot_num]["intensity"])*2.0)
ax.set_xlabel("Strom durch Magneten / " + current_unit, fontsize = fsize)
ax.set_ylabel("Intensität / " + intensity_unit[plot_num], fontsize = fsize)
ax.tick_params(axis='both', labelsize = fsize)
fig.tight_layout()

fig.savefig("../Protokoll/Pictures/" + names[plot_num][:-4] +".pdf", format="pdf")

plt.show()

# %%
