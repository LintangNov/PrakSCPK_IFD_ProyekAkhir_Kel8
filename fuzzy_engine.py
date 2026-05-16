import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

gpa = ctrl.Antecedent(np.arange(1.9, 4.01, 0.01), 'gpa') 
ekskul = ctrl.Antecedent(np.arange(0, 12.5, 0.1), 'ekskul')
olahraga = ctrl.Antecedent(np.arange(0, 10.5, 0.1), 'olahraga')
screen_time = ctrl.Antecedent(np.arange(1, 12.5, 0.1), 'screen_time')
stress = ctrl.Antecedent(np.arange(1, 9.5, 0.1), 'stress')

skor_teladan = ctrl.Consequent(np.arange(0, 101, 1), 'skor_teladan')

# GPA (segitiga)
gpa['Rendah'] = fuzz.trimf(gpa.universe, [1.9, 1.9, 2.8]) 
gpa['Sedang'] = fuzz.trimf(gpa.universe, [2.5, 3.2, 3.7]) 
gpa['Tinggi'] = fuzz.trimf(gpa.universe, [3.5, 4.0, 4.0])

# Ekskul (segitiga)
ekskul['Pasif'] = fuzz.trimf(ekskul.universe, [0, 0, 4])
ekskul['Sedang'] = fuzz.trimf(ekskul.universe, [2, 6, 9]) 
ekskul['Aktif'] = fuzz.trimf(ekskul.universe, [7, 12, 12])

# Exercise (segitiga)
olahraga['Kurang'] = fuzz.trimf(olahraga.universe, [0, 0, 4])
olahraga['Cukup'] = fuzz.trimf(olahraga.universe, [2, 5, 7]) 
olahraga['Sangat Aktif'] = fuzz.trimf(olahraga.universe, [6, 10, 10]) 

# Screen Time (trapesium)
screen_time['Ideal'] = fuzz.trapmf(screen_time.universe, [1, 1, 3, 5]) 
screen_time['Berlebih'] = fuzz.trapmf(screen_time.universe, [4, 6, 12, 12]) 

# Stress Level (segitiga)
stress['Rendah'] = fuzz.trimf(stress.universe, [1, 1, 4]) 
stress['Sedang'] = fuzz.trimf(stress.universe, [2.5, 5, 7])
stress['Tinggi'] = fuzz.trimf(stress.universe, [6, 9, 9]) 

skor_teladan['Kurang'] = fuzz.trimf(skor_teladan.universe, [0, 0, 40]) 
skor_teladan['Layak'] = fuzz.trimf(skor_teladan.universe, [30, 50, 70]) 
skor_teladan['Sangat Layak'] = fuzz.trimf(skor_teladan.universe, [60, 100, 100])