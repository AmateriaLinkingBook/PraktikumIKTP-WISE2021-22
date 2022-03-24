import numpy as np
import matplotlib
matplotlib.use('QT5Agg')
import matplotlib.pyplot as plt

# Isotope = isobare = 10_Be, 10_B

e_charge = 1.602176634e-19
u = 1.66053906660e-27 # atomare Masseneinheit

U_ion_source = 29.0e3
U_acc = 5.2479e6

Masse_Be_und_B = 10
Masse_Molekuel_minus = Masse_Be_und_B+16 # BeO^- / BO^-

Z_nach_Beschleuniger = np.array([1, 2, 3, 4])

E_vor_Beschleuniger = e_charge * U_ion_source
print("Energie vor Beschleuniger:", E_vor_Beschleuniger/e_charge/1.0e6, "MeV")

print("Ladungszustände:", Z_nach_Beschleuniger)
E_nach_Beschleuniger = (e_charge * (U_ion_source + U_acc) * (Masse_Be_und_B / Masse_Molekuel_minus)) + (U_acc * (Z_nach_Beschleuniger  * e_charge))
E_nach_Beschleuniger = E_nach_Beschleuniger/e_charge/1.0e6 # in MeV
print("Energie nach Beschleuniger:", E_nach_Beschleuniger, "MeV")

dE_dx_Be_elec_Folie = np.array([1.052e3, 8.502e2, 7.134e2, 6.205e2]) # in keV / micrometer
dE_dx_Be_nuc_Folie = np.array([1.062e0, 6.642e-1, 4.895e-1, 3.901e-1]) # in keV / micrometer
dE_dx_B_elec_Folie = np.array([1.447e3, 1.226e3, 1.051e3, 9.249e2])  # in keV / micrometer
dE_dx_B_nuc_Folie = np.array([1.602e0, 1.004e0, 7.413e-1, 5.914e-1])  # in keV / micrometer

dE_dx_Be_Folie = dE_dx_Be_elec_Folie + dE_dx_Be_nuc_Folie
dE_dx_B_Folie = dE_dx_B_elec_Folie + dE_dx_B_nuc_Folie

print(dE_dx_Be_Folie)
print(dE_dx_B_Folie)
Energieverlust_Be_Folie = dE_dx_Be_Folie * 1 # in keV
Energieverlust_B_Folie = dE_dx_B_Folie * 1 # in keV

E_Be_nach_Folie = E_nach_Beschleuniger - (dE_dx_Be_Folie/1.0e3)
E_B_nach_Folie = E_nach_Beschleuniger - (dE_dx_B_Folie/1.0e3)

print("Energie Be nach Folie:", E_Be_nach_Folie, "MeV")
print("Energie B nach Folie:", E_B_nach_Folie, "MeV")
print("Energie B nach Folie:", E_B_nach_Folie, "MeV")

d_plate = 0.036 # meter
Z_nach_Folie = 4
Ablenk_r_nach_Folie = 2.6 # meter

U_anleg = ((E_Be_nach_Folie*1.0e6)*e_charge)*d_plate/(Z_nach_Folie*e_charge*Ablenk_r_nach_Folie)
print(U_anleg)

# ---

dE_dx_Be_neun = 8.507e2 + 6.588e-1
print(E_nach_Beschleuniger[1]*(9/10))
E_Be_neun_aus_BeOH = E_nach_Beschleuniger[1]*(9/10) - (dE_dx_Be_neun/1.0e3)
print(E_Be_neun_aus_BeOH)
