import re
import shutil
import csv
import os
import glob
import pandas as pd
import datetime

reg = r'Opera-3d > '
path_pattern = r"C:\Users\Mi\Desktop\opera_proj\opera_logs\Post_*.lp"

try:
    path = glob.glob(path_pattern)[0]
except IndexError:
    raise FileExistsError('Не существует файла с таким шаблоном пути')

path_csv = r'C:\Users\Mi\Desktop\opera_proj\info.csv'
path_local_dir = r'C:\Users\Mi\Desktop\opera_proj\локальная_папка'

file_name = os.listdir(path_local_dir)[0]
ind = int(re.search(r'(\d+)', file_name).group(1))

harmonics = []
with open(path) as file:
    while True:
        try:
            data = file.readline().split()
            if data[0].isdigit():
                harmonics.append(data[3])
        except IndexError:
            break

print(pd.DataFrame([ind] + harmonics, index = ['id'] + list(range(len(harmonics))), columns=[datetime.datetime.now()]).T)

# Удалить все содержимое файла в логах работы после чтения

folder_paths = [r"C:\Users\Mi\Desktop\opera_proj\opera_logs", path_local_dir]

for folder_path in folder_paths:
    # Проверяем, существует ли папка
    if os.path.exists(folder_path):
        # Удаляем все содержимое папки
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Удалить файл или ссылку
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Удалить папку рекурсивно
            except Exception as e:
                print(f'Ошибка при удалении {file_path}. Причина: {e}')
    else:
        print(f'Папка {folder_path} не найдена.')

# тут дописать, чтобы эта гармоника сразу писалась в файл info.csv

# with open(path_csv, mode='a', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['5th_B'])