import helper as h
import re

path_to_load_shape = h.path_to_load_shape
path_to_load_scripts_2_check = h.path_to_load_scripts_2_check

# Здесь вписываются параметры фаски, полученные исходя из мл модели
r, l = 2.938228798088884, 16.19596210921747

with open(path_to_load_scripts_2_check + rf'\test_shape.comi', mode='w', encoding='utf-8', newline='') as file:
    # Здесь образец скрипта из файла check.comi
    s = h.comi_script
    s = re.sub('LEFTCHAMFER=5 RIGHTCHAMFER=7', f'LEFTCHAMFER={l} RIGHTCHAMFER={r}', s)
    file.write(s)
