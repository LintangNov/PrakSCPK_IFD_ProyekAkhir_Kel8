import numpy as np
import skfuzzy as fuzz
import itertools
from skfuzzy import control as ctrl

gpa = ctrl.Antecedent(np.arange(1.9, 4.01, 0.01), 'gpa') 
ekskul = ctrl.Antecedent(np.arange(0, 12.5, 0.1), 'ekskul')
olahraga = ctrl.Antecedent(np.arange(0, 10.5, 0.1), 'olahraga')
screen_time = ctrl.Antecedent(np.arange(1, 12.5, 0.1), 'screen_time')
stress = ctrl.Antecedent(np.arange(1, 9.5, 0.1), 'stress')

skor_teladan = ctrl.Consequent(np.arange(0, 101, 1), 'skor_teladan')

# GPA (segitiga): 3 kat
gpa['Rendah'] = fuzz.trimf(gpa.universe, [1.9, 1.9, 2.8]) 
gpa['Sedang'] = fuzz.trimf(gpa.universe, [2.5, 3.2, 3.7]) 
gpa['Tinggi'] = fuzz.trimf(gpa.universe, [3.5, 4.0, 4.0])

# Ekskul (segitiga): 3 kat
ekskul['Pasif'] = fuzz.trimf(ekskul.universe, [0, 0, 4])
ekskul['Sedang'] = fuzz.trimf(ekskul.universe, [2, 6, 9]) 
ekskul['Aktif'] = fuzz.trimf(ekskul.universe, [7, 12, 12])

# Exercise (segitiga): 3 kat
olahraga['Kurang'] = fuzz.trimf(olahraga.universe, [0, 0, 4])
olahraga['Cukup'] = fuzz.trimf(olahraga.universe, [2, 5, 7]) 
olahraga['Sangat Aktif'] = fuzz.trimf(olahraga.universe, [6, 10, 10]) 

# Screen Time (trapesium): 2 kat
screen_time['Ideal'] = fuzz.trapmf(screen_time.universe, [1, 1, 3, 5]) 
screen_time['Berlebih'] = fuzz.trapmf(screen_time.universe, [4, 6, 12, 12]) 

# Stress Level (segitiga): 3 kat
stress['Rendah'] = fuzz.trimf(stress.universe, [1, 1, 4]) 
stress['Sedang'] = fuzz.trimf(stress.universe, [2.5, 5, 7])
stress['Tinggi'] = fuzz.trimf(stress.universe, [6, 9, 9]) 

skor_teladan['Kurang'] = fuzz.trimf(skor_teladan.universe, [0, 0, 40]) 
skor_teladan['Layak'] = fuzz.trimf(skor_teladan.universe, [30, 50, 70]) 
skor_teladan['Sangat Layak'] = fuzz.trimf(skor_teladan.universe, [60, 100, 100])


# rule

bobot_gpa = {'Rendah': 1, 'Sedang': 2, 'Tinggi': 3}
bobot_ekskul = {'Pasif': 1, 'Sedang': 2, 'Aktif': 3}
bobot_olahraga = {'Kurang': 1, 'Cukup': 2, 'Sangat Aktif': 3}
bobot_screen = {'Berlebih': 1, 'Ideal': 2}
bobot_stress = {'Tinggi': 1, 'Sedang': 2, 'Rendah': 3}

rules = []

combination = itertools.product(
    bobot_gpa.keys(),
    bobot_ekskul.keys(),
    bobot_olahraga.keys(),
    bobot_screen.keys(),
    bobot_stress.keys(),
)

for g, e, o, sc, st in combination:
    point_tot = bobot_ekskul[e] + bobot_gpa[g] + bobot_olahraga[o] + bobot_screen[sc] + bobot_stress[st]
    output_kategori=''

    if point_tot >= 11:
        output_kategori = 'Sangat Layak'
    elif 8 <= point_tot <= 10:
        output_kategori = 'Layak'
    else:
        output_kategori = 'Kurang'
    
    rule = ctrl.Rule(
        gpa[g] & ekskul[e] & screen_time[sc] & stress[st] & olahraga[o], skor_teladan[output_kategori]
    )

    rules.append(rule)

teladan_ctrl = ctrl.ControlSystem(rules)

teladan_sim = ctrl.ControlSystemSimulation(teladan_ctrl)

def single_inference(gpa_input, ekskul_input, olahraga_input, screen_time_input, stress_input):
    teladan_sim.input['gpa'] = gpa_input
    teladan_sim.input['ekskul'] = ekskul_input
    teladan_sim.input['olahraga'] = olahraga_input
    teladan_sim.input['screen_time'] = screen_time_input
    teladan_sim.input['stress'] = stress_input
    
    teladan_sim.compute()
    
    return teladan_sim.output['skor_teladan']

def rank(df):
    scores = []

    for index, row in df.iterrows():
        try:
            score = single_inference(
                row['GPA'],                              
                row['extracurricular_hours_per_week'],   
                row['exercise_hours_per_week'],          
                row['screen_time_hours'],                
                row['mental_stress_level']
            )
            scores.append(score)
        except Exception as e:
            scores.append(0)
    
    df['skor_teladan'] = scores
    df_sorted = df.sort_values(by='skor_teladan', ascending=False).reset_index(drop=True)
    return df_sorted
