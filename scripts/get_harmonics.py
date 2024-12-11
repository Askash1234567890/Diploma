import csv
import datetime
import glob
import os
import re
import shutil

import helper as h


def get_harmonics():
    # Использование пути для удаления файла логов работы оперы
    path_pattern = h.path_pattern
    path_grad_csv = h.path_grad_csv
    path_local_dir = h.path_local_dir
    path_to_opera_logs = h.path_to_opera_logs

    try:
        path = glob.glob(path_pattern)[0]
    except IndexError:
        print('Не существует файла с таким шаблоном пути')
        return True

    try:
        file_name = os.listdir(path_local_dir)[0]
    except IndexError:
        return True

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

    # with open(path_grad_csv, mode='w', newline='', encoding='utf-8') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['ts', 'id'] + [f'h{i}' for i in range(len(harmonics))])

    with open(path_grad_csv, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), ind] + harmonics)

    # Удалить все содержимое файла в логах работы после чтения

    folder_paths = [path_to_opera_logs, path_local_dir]

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
                    return True
        else:
            print(f'Папка {folder_path} не найдена.')
            return True
    return False

get_harmonics()