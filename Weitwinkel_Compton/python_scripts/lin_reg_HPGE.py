from fit_bivariate import bivariate_fit

%matplotlib qt5

import numpy as np
import matplotlib.pyplot as plt

E_gamma = np.array([81.0, 276.4, 302.89, 356.02, 383.85])
mu = np.array([89.0, 299.9, 328.4, 386.4, 416.8])
err_x = 2.0 * np.sqrt(2.0 * np.log(2)) * np.array([3.1, 3.6, 3.7, 3.7, 3.7])
err_y = 1e-8 * np.ones((len(E_gamma)))

res = bivariate_fit(mu, E_gamma, err_x, err_y)
print("result: E(K) = ({slope:.3f} +/- {slopePM:.3f}) * K + ({intersect:.3f} +/- {intersectPM:.3f})".format(slope = res[1], intersect = res[0], slopePM = np.sqrt(res[3][0, 0]), intersectPM = np.sqrt(res[3][1, 1])))

# %%

fsize = 16

fig = plt.figure(figsize = (12.0, 9.0))
ax = fig.add_subplot()
ax.errorbar(mu, E_gamma, xerr=err_x, fmt="b.")
ax.plot([mu[0], mu[-1]], [res[1]*mu[0] + res[0], res[1]*mu[-1] + res[0]], color = "black")

ax.grid(True)
ax.set_xlabel("Kanal", fontsize=fsize)
ax.set_ylabel("Energie [keV]", fontsize=fsize)
ax.set_title("HPGe-Detektor Kalibriergerade", fontsize=fsize)

plt.yticks(fontsize=fsize)
plt.xticks(fontsize=fsize)
plt.show()
