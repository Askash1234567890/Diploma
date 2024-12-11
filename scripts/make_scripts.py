import csv
import helper as h
import numpy as np
import re

ind = 0
path_to_load_shape = h.path_to_load_shape
path_to_load_scripts = h.path_to_load_scripts
path_to_load_scripts_2_check = h.path_to_load_scripts_2_check

with open(path_to_load_shape, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'RIGHTCHAMFER'.capitalize(), 'LEFTCHAMFER'.capitalize()])


for r in np.linspace(0.0001, 10, 32):
    for l in np.linspace(0.0001, 20, 32):
        # Создает .csv файл с формой
        with open(path_to_load_shape, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([ind, r, l])

        with open(path_to_load_scripts_2_check + rf'\shape_{ind}.comi', mode='w', encoding='utf-8', newline='') as file:
            # Здесь образец скрипта из файла check.comi
            s = h.comi_script
            s = re.sub('LEFTCHAMFER=5 RIGHTCHAMFER=7', f'LEFTCHAMFER={l} RIGHTCHAMFER={r}', s)
            file.write(s)
        ind += 1