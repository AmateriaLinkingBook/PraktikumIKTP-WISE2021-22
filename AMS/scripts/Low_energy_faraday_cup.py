import numpy as np
import pandas as pd
import scipy
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

prefix = "../Daten/"
names = np.array(["LEMass40-85pos153BeOTUDPract.asc",
                  "LEMass40-85pos173KY13STUDPract.asc",
                  "LEMass40-85pos173KY13STUDPract2.asc"])
intensity_unit = "A"
intensity_factor = 1/100 # Weil in % angegeben

# %%

N = names.size

print("aquire Data.\nShapes:")

data = np.empty(N, dtype=pd.DataFrame)
for i in np.arange(0, N, 1):
    data[i] = pd.DataFrame(np.loadtxt(prefix + names[i], delimiter=' ', skiprows=21, usecols = (0,1)),
              columns=["channel", "intensity"])
    print(data[i].shape)

print("----------\nShapes after filter:")

for i in np.arange(0, N, 1):
    data[i] = -data[i][data[i]["intensity"] != 9.990e+002]
    data[i]["intensity"] *= intensity_factor
    print(data[i].shape)

print("Intensity should now be in given units")

# %%

plot_num = 0

fig = plt.figure(figsize=(8, 4.5))
ax = fig.add_subplot()

ax.plot(data[plot_num]["channel"], data[plot_num]["intensity"])
ax.set_yscale('log')
ax.set_ylim(1.0e-10, np.max(data[plot_num]["intensity"])*1.5)
ax.set_ylabel("Intensität / " + intensity_unit)

plt.show()
