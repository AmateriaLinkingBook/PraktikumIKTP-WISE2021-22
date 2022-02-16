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
                  "LEMass40-85pos173KY13STUDPract2.asc"])
intensity_unit = np.array(["%",  # minimum height peak has to have, in amounts used in files (y-coordinate (intensity)), for finding peaks
                           "A",
                           "A",
                           "A"])
intensity_factor = np.array([1,
                             -1/100,  # Weil in % angegeben
                             -1/100,  # Weil in % angegeben
                             -1/100]) # Weil in % angegeben
current_unit = "A"
min_peak_height = np.array([1.0e-3,  # minimum height peak has to have, in amounts used in files (y-coordinate (intensity)), for finding peaks
                            5.0e-9,
                            5.0e-9,
                            5.0e-9])
peak_width = 1.0 # approximate width peak can have, in amounts used in files (x-coordinate (mass)), for fitting peaks

# %%

def gaussian(x, scale, mu, sigma):
    sigma2 = sigma**2
    return scale*(1.0/(np.sqrt(2.0*np.pi*sigma2)) * np.exp(-(x-mu)**2)/(2*sigma2))

def cauchy(x, scale, x_0, gamma):
    return scale*(1/(np.pi*gamma*(1+((x-x_0)/gamma)**2)))

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
    peaks[i] = find_peaks(data[i]["intensity"], height = min_peak_height[i])[0]
    print(i, "- peak amount:", peaks[i].size)

"""
print("Fitting peaks...")

peak_fits = np.empty(N, dtype=np.ndarray)
for i in np.arange(0, N, 1):
    peak_fits[i] = np.empty(peaks[i].size, dtype=np.ndarray)
    for j in np.arange(0, peaks[i].size, 1):
        scale_fac = data[i]["channel"].size/(np.max(data[i]["channel"])-np.min(data[i]["channel"]))
        lower_idx = int(np.floor(peaks[i][j] - peak_width*scale_fac))
        upper_idx = int(np.ceil(peaks[i][j] + peak_width*scale_fac))
        peak_fits[i][j] = curve_fit(cauchy,
                          data[i]["channel"].iloc[lower_idx:upper_idx],
                          data[i]["intensity"].iloc[lower_idx:upper_idx],
                          p0 = [min_peak_height, data[i]["channel"].iloc[peaks[i][j]], peak_width/5],
                          bounds = ([-np.inf, data[i]["channel"].iloc[lower_idx], 0],[np.inf, data[i]["channel"].iloc[upper_idx], peak_width*2]))[0]
        print(peak_fits[i][j])
"""

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

# %%

"""

# calculate ratios for peak combinations

N_recommend = 10

N_ratio = int((N_ions*(N_ions-1))/2)
ratios = [[]]*N_ratio
for i in np.arange(0, N_ions-1, 1):
    for j in np.arange(1, N_ions-i, 1):
        ratios[int(i*(N_ions-1)-i*(i-1)/2+(j-1))] = [i,
                                                     i+j,
                                                     np.sqrt(possible_ions[i+j][1]/possible_ions[i][1])/(possible_ions[i+j][2]/possible_ions[i][2])]

N_peak_ratio = int((N_peak*(N_peak-1))/2)
peak_ratios = [[]]*N_peak_ratio
for i in np.arange(0, N_peak-1, 1):
    for j in np.arange(1, N_peak-i, 1):
        peak_ratios[int(i*(N_peak-1)-i*(i-1)/2+(j-1))] = [i,
                                                          i+j,
                                                          peak_avg[identify_num][i]/peak_avg[identify_num][i+j]]

# ratio print

best_ratio_sorters = np.empty(N_peak_ratio, dtype=np.ndarray)
for i in np.arange(0, N_peak_ratio, 1):
    diff_arr = np.abs(np.array([ratios[i][2] for i in np.arange(0, N_ratio, 1)]) - peak_ratios[i][2])
    best_ratio_sorters[i] = np.argsort(diff_arr)

if N_recommend > N_ratio:
    N_recommend = N_ratio

for i in np.arange(0, N_peak_ratio, 1):
    print("--- peaks @", np.round(peak_avg[identify_num][peak_ratios[i][0]], 1), current_unit, "and", np.round(peak_avg[identify_num][peak_ratios[i][1]], 1), current_unit, "---")
    print("peak ratio:", np.round(peak_ratios[i][2], 4))
    print("nearest ratios:")
    print("Ion 1 (@" + str(np.round(peak_avg[identify_num][peak_ratios[i][1]], 1)) + " " + current_unit + ")\t\tIon 2 (@" + str(np.round(peak_avg[identify_num][peak_ratios[i][0]], 1)) + " " + current_unit + ")\t\tratio")
    for j in np.arange(0, N_recommend, 1):
        temp = [ratios[l] for l in best_ratio_sorters[i]]
        print(possible_ions[temp[j][0]][0], "\t\t", possible_ions[temp[j][1]][0], "\t\t", np.round(temp[j][2], 4))

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

# %%

plot_num = identify_num
fsize = 16

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot()

ax.plot(data[plot_num]["channel"], data[plot_num]["intensity"])
ax.plot(peak_avg[plot_num], data[plot_num]["intensity"].iloc[peaks[plot_num]], ".")
for i in np.arange(0, peaks[plot_num].size, 1):
    ax.text(peak_avg[plot_num][i]+0.5,
            data[plot_num]["intensity"].iloc[peaks[plot_num][i]],
            np.round(peak_avg[plot_num][i], 1),
            fontsize=fsize)
# beautiful_x = np.linspace(np.min(data[plot_num]["channel"]), np.max(data[plot_num]["channel"]), 2000)
# for j in np.arange(0, peaks[plot_num].size, 1):
#     ax.plot(beautiful_x, cauchy(beautiful_x, peak_fits[plot_num][j][0], peak_fits[plot_num][j][1], peak_fits[plot_num][j][2]))
ax.set_yscale('log')
ax.set_ylim(1.0e-10, np.max(data[plot_num]["intensity"])*1.5)
ax.set_xlabel("Strom durch Magneten / " + current_unit, fontsize = fsize)
ax.set_ylabel("Intensität / " + intensity_unit[plot_num], fontsize = fsize)
ax.tick_params(axis='both', labelsize = fsize)
fig.tight_layout()

# fig.savefig("../Protokoll/Pictures/new_figure.pdf", format="pdf")

plt.show()

# %%
