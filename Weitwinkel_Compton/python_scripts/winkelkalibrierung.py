from scipy.stats import linregress
import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

prefix = "../Daten/"
"""
names = np.array(["Na22_(-33, 10, 7)_60min.txt", "Na22_(-33, 4, 15)_30min.txt", "Na22_(-33, 6, 20)_30min.txt", "Na22_(-33, 9, 24)_30min.txt", "Na22_(-33, 20, 27)_30min.txt"])
"""
names = np.array(["Ba133_2.5h.txt", "Ba133_2h.txt"])
"""
names = np.array(["Na22_2h.txt", "Na22_(-33, 10, 7)_60min.txt", "Na22_(-33, 4, 15)_30min.txt", "Na22_(-33, 6, 20)_30min.txt", "Na22_(-33, 9, 24)_30min.txt", "Na22_(-33, 20, 27)_30min.txt"])
"""
data = []
for name in names:
    data.append(np.transpose(np.loadtxt(prefix + name, delimiter=';', skiprows=2)[:, 2:]))


temp = data[0]
for i in range(1, len(data)):
    temp = np.concatenate((temp, data[i]), axis = 1)

data = [temp]

# 0 - HPGermanium, 1 - Szintillator

coords = np.array([[-33, 10, 7],
                   [-33, 4, 15],
                   [-33, 6, 20],
                   [-33, 9, 24],
                   [-33, 20, 27],
                   ])

# %%
# Data manipulation

channel_max_Germanium = 1800
channel_max_Szintillator = 1000

for i in range(0, len(data)):
    data[i] = data[i][:, data[i][0] <= channel_max_Germanium]
    data[i] = data[i][:, data[i][1] <= channel_max_Szintillator]

# Filter the linear area

### FILTER SETTINGS
data_filter_m = -233.0/383.0  # delta y / delta x
data_filter_n_low = 212
data_filter_n_high = 260
### END FILTER SETTINGS

filtered_data = [None] * len(data)

for i in range(0, len(data)):
    line_part = data[i][1] - (data_filter_m * data[i][0])  # y - m*x = n
    filter = np.logical_and(line_part > data_filter_n_low, line_part < data_filter_n_high)
    filtered_data[i] = data[i][:, filter]


# linear regression
reg_results = [None] * len(data)

for i in range(0, len(data)):
    reg_results[i] = linregress(filtered_data[i])

# find error

### ERROR FILTER SETTINGS
margin = 0.68   # fraction of the data points inside error boundaries
initial_n_shift = 50.0
max_error = 10e-3  # max. allowed difference from margin
### END ERROR FILTER SETTINGS

# assuming error boundaries are parallel to regression line and same distance from it.

n_shift_array = []

for i in range(0, len(data)):
    n_shift = initial_n_shift
    n_shift_shift = initial_n_shift
    error = np.inf
    line_part_err = filtered_data[i][1] - (reg_results[i].slope * filtered_data[i][0])

    while True:
        filter_err = np.logical_and(line_part_err > reg_results[i].intercept-n_shift, line_part_err < reg_results[i].intercept+n_shift)
        error = margin - (np.sum(filter_err) / len(filtered_data[i][0]))
        if (np.abs(error) <= max_error):
            n_shift_array.append(n_shift)
            break
        else:
            if np.sign(error) != np.sign(n_shift_shift):
                n_shift_shift *= -0.5
            n_shift += n_shift_shift

# %%
# angles
detector_x_y_z = [-33, 30, 0]
angles = 90 - np.arctan2(np.abs(coords[:, 2] - detector_x_y_z[2]), np.abs(coords[:, 1] - detector_x_y_z[1]))*(180/np.pi)  # 90° arctan(|del_z| / |del_y|)
print(angles)

# Plot

fontsize = 24
binfactor = 1/2

plot_single = -1

u = int(np.ceil(np.sqrt(len(data))))   # Find subplot x and y amount
w = int(np.ceil(len(data)/u))
print(u, w)

if (plot_single < 0):
    fig, axes = plt.subplots(w, u, squeeze = False)
    fig.set_figheight(9.0)
    fig.set_figwidth(11.0)

    for i in range(0, len(data)):
        x_idx = int(np.floor(i / u))
        y_idx = int(i % u)
        helper = axes[x_idx][y_idx].hist2d(data[i][0], data[i][1],
            bins=[np.linspace(0, channel_max_Germanium, int(channel_max_Germanium*binfactor)), np.linspace(0, channel_max_Szintillator, int(channel_max_Szintillator*binfactor))],
            range=[[30, channel_max_Germanium], [20, channel_max_Szintillator]])
        colorbar_helper = fig.colorbar(helper[3], ax=axes[x_idx][y_idx])
        colorbar_helper.ax.tick_params(labelsize = fontsize)
        axes[x_idx][y_idx].set_title(r"Streuwinkel: ${wink:.1f}°$".format(wink=angles[i]), fontsize = fontsize)
else:
    fig, axes = plt.subplots(1, 1, squeeze = False)
    fig.set_figheight(9.0)
    fig.set_figwidth(11.0)

    helper = axes[0][0].hist2d(data[plot_single][0], data[plot_single][1], \
        bins = [np.linspace(0, channel_max_Germanium, int(channel_max_Germanium*binfactor)), np.linspace(0, channel_max_Szintillator, int(channel_max_Szintillator*binfactor))], \
        range=[[30, channel_max_Germanium], [20, channel_max_Szintillator]])
    colorbar_helper = fig.colorbar(helper[3], ax=axes[0][0])
    colorbar_helper.ax.tick_params(labelsize = fontsize)
    #axes[0][0].plot([0, -(reg_results[plot_single].intercept / reg_results[plot_single].slope)], [reg_results[plot_single].intercept, 0], color="greenyellow", label="linear fit", alpha = 0.3)
    axes[0][0].set_title(r"Streuwinkel: ${wink:.1f}°$".format(wink=angles[plot_single]), fontsize = fontsize)

plt.yticks(fontsize=fontsize)
plt.xticks(fontsize=fontsize)
fig.tight_layout()
plt.show()

# %%


# filtered data

x_max = 1800

plot_single = -1

if (plot_single < 0):

    fig, axes = plt.subplots(w, u, squeeze = False)
    fig.set_figwidth(16.0)
    fig.set_figheight(9.0)

    for i in range(0, len(data)):
        x_idx = int(np.floor(i / u))
        y_idx = int(i % u)
        helper = axes[x_idx][y_idx].hist2d(filtered_data[i][0], filtered_data[i][1], \
            bins = [np.linspace(0, channel_max_Germanium, int(channel_max_Germanium*binfactor)), np.linspace(0, channel_max_Szintillator, int(channel_max_Szintillator*binfactor))], \
            range=[[30, channel_max_Germanium], [20, channel_max_Szintillator]])
        colorbar_helper = fig.colorbar(helper[3], ax=axes[x_idx][y_idx])
        colorbar_helper.ax.tick_params(labelsize = fontsize)
        axes[x_idx][y_idx].plot([0, -(data_filter_n_low/data_filter_m)], [data_filter_n_low, 0], color="plum", label="filter lower bound")
        axes[x_idx][y_idx].plot([0, -(data_filter_n_high/data_filter_m)], [data_filter_n_high, 0], color="thistle", label="filter upper bound")
        axes[x_idx][y_idx].plot([0, -(reg_results[i].intercept / reg_results[i].slope)], [reg_results[i].intercept, 0], color="greenyellow", label="linear fit")
        axes[x_idx][y_idx].plot([0, -((reg_results[i].intercept+n_shift_array[i]) / reg_results[i].slope)], [(reg_results[i].intercept+n_shift_array[i]), 0], color="lime", label="error range")
        axes[x_idx][y_idx].plot([0, -((reg_results[i].intercept-n_shift_array[i]) / reg_results[i].slope)], [(reg_results[i].intercept-n_shift_array[i]), 0], color="lime")
        axes[x_idx][y_idx].set_xlim(20, x_max)
        axes[x_idx][y_idx].set_title(r"$x = 0$ intercept: ${inter:.3f}$, error: $\pm{err:.3f}$".format(inter=reg_results[i].intercept, err=n_shift_array[i]), fontsize=fontsize)
        axes[x_idx][y_idx].legend(loc="best", fontsize=fontsize)

else:
    fig, axes = plt.subplots(1, 1, squeeze = False)
    fig.set_figheight(9.0)
    fig.set_figwidth(11.0)

    helper = axes[0][0].hist2d(filtered_data[plot_single][0], filtered_data[plot_single][1], \
        bins = [np.linspace(0, channel_max_Germanium, int(channel_max_Germanium*binfactor)), np.linspace(0, channel_max_Szintillator, int(channel_max_Szintillator*binfactor))], \
        range=[[30, channel_max_Germanium], [20, channel_max_Szintillator]])
    colorbar_helper = fig.colorbar(helper[3], ax=axes[0][0])
    colorbar_helper.ax.tick_params(labelsize = fontsize)
    axes[0][0].plot([0, -(data_filter_n_low/data_filter_m)], [data_filter_n_low, 0], color="plum", label="filter lower bound")
    axes[0][0].plot([0, -(data_filter_n_high/data_filter_m)], [data_filter_n_high, 0], color="thistle", label="filter upper bound")
    axes[0][0].plot([0, -(reg_results[plot_single].intercept / reg_results[plot_single].slope)], [reg_results[plot_single].intercept, 0], color="greenyellow", label="linear fit")
    axes[0][0].plot([0, -((reg_results[plot_single].intercept+n_shift_array[plot_single]) / reg_results[plot_single].slope)], [(reg_results[plot_single].intercept+n_shift_array[plot_single]), 0], color="lime", label="error range")
    axes[0][0].plot([0, -((reg_results[plot_single].intercept-n_shift_array[plot_single]) / reg_results[plot_single].slope)], [(reg_results[plot_single].intercept-n_shift_array[plot_single]), 0], color="lime")
    axes[0][0].set_xlim(20, x_max)
    axes[0][0].legend(loc="best", fontsize=fontsize)

plt.yticks(fontsize=fontsize)
plt.xticks(fontsize=fontsize)
fig.tight_layout()
plt.show()
