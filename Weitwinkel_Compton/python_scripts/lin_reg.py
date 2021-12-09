from fit_bivariate import bivariate_fit
import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

def linear_f(x, m, n):
    return (m*x) + n

energies = np.array([511.00, 1274.54, 356.02])
channels = np.array([346, 906, 229])
del_channels = np.array([14, 15, 9])

res = bivariate_fit(channels, energies, del_channels, 1e-8 * np.ones((len(energies))))
print(res)
print("m: " + str(res[1]) + "   n: " + str(res[0]) + "   sigma m: " + str(np.sqrt(res[3][0, 0])) + "   sigma n: " + str(np.sqrt(res[3][1, 1])))
