import numpy as np
import scipy
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

prefix = "../Daten/"
names = np.array(["LEMass40-85pos153BeOTUDPract.asc",
                  "LEMass40-85pos173KY13STUDPract.asc",
                  "LEMass40-85pos173KY13STUDPract2.asc"])

data = []
for name in names:
    data.append(np.loadtxt(prefix + name, delimiter=' ', skiprows=21, usecols = (0,1)))

data = np.array(data)

for i in range(0, data.size[0]):
    print()

filter = data[:, :, 1] != 9.99e2
print(filter.shape, data.shape)
data = np.compress(filter, data)
print(data, data.shape)

fig = plt.figure(figsize=(8, 4.5))
ax = fig.add_subplot()

ax.scatter(data[0, :, 0], data[0, :, 1], s=1)
ax.set_yscale('log')

plt.show()
