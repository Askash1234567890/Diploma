import re
import helper as h

reg = r'Opera-3d > '

def get_logs(flag: bool) -> None:
    '''
    :param flag:
    :return:
    Функция парсит сырые логи и записывает их в .comi файл.
    Есть два режима работы - определяется параметром flag:
    1) flag = True - парсинг логов построения модели (.comi файла для opera_modeler)
    2) flag = False - парсинг логов для рассчета гармоник (.comi файла для opera_post_processor)

    Перед использованием измените ваши пути (path) к файлам
    '''
    path = h.path
    path_load = h.path_load

    path_post = h.path_post
    path_post_load = h.path_post_load

    if flag:
        with open(path, encoding='utf-8') as f:
            res = []
            for c in f.readlines():
                if c[0] == '#':
                    res.append('')
                elif c and c != '\n':
                    res.append(re.sub(reg, '', c).strip())

        with open(path_load, 'w', encoding='utf-8') as file:
            for i, row in enumerate(res):
                file.write(row + '\n')
    else:
        with open(path_post, encoding='utf-8') as f:
            res = []
            for c in f.readlines():
                if c[0] == '#':
                    res.append('')
                elif c and c != '\n':
                    res.append(re.sub(reg, '', c).strip())

        with open(path_post_load, 'w', encoding='utf-8') as file:
            for i, row in enumerate(res):
                file.write(row + '\n')

get_logs(flag=0)