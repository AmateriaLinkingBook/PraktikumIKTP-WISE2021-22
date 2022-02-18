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
Masse_Molekuel_minus = 10+16 # BeO^- / BO^-

Z_nach_Beschleuniger = np.array([1, 2, 3, 4])


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

d_plate = 0.036 # meter
Z_nach_Folie = 4
Ablenk_r_nach_Folie = 2.6 # meter

U_anleg = ((E_Be_nach_Folie*1.0e6)*e_charge)*d_plate/(Z_nach_Folie*e_charge*Ablenk_r_nach_Folie)
print(U_anleg)

dE_dx_Be_elec_Gas = np.array([4.644e-2, 3.392e-2, 2.623e-2, 2.138e-2])  # in MeV / mm
dE_dx_Be_nuc_Gas = np.array([4.229e-5, 2.445e-5, 1.751e-5, 1.376e-5])  # in MeV / mm
dE_dx_B_elec_Gas = np.array([6.406e-2, 4.949e-2, 3.912e-2, 3.217e-2])  # in MeV / mm
dE_dx_B_nuc_Gas = np.array([6.758e-5, 3.809e-5, 2.703e-5, 2.115e-5])  # in MeV / mm

dE_dx_Be_Gas = dE_dx_Be_elec_Gas + dE_dx_Be_nuc_Gas
dE_dx_B_Gas = dE_dx_B_elec_Gas + dE_dx_B_nuc_Gas

print(dE_dx_Be_Gas)
print(dE_dx_B_Gas)

Flugweite_Be_gas = (E_Be_nach_Folie / dE_dx_Be_Gas)
Flugweite_B_gas = (E_B_nach_Folie / dE_dx_B_Gas)
print("Flugweite Be im Detektor:", Flugweite_Be_gas, "mm")
print("Flugweite B im Detektor:", Flugweite_B_gas, "mm")
