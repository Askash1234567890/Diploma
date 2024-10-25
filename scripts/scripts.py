import re

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
    path = r"C:\Users\Mi\Desktop\opera_proj\образец скриптов\логи_моделер.txt"
    path_load = r"C:\Users\Mi\Desktop\opera_proj\образец скриптов\check.comi"

    path_post = r"C:\Users\Mi\Desktop\opera_proj\образец скриптов\логи_пост_процессор.txt"
    path_post_load = r"C:\Users\Mi\Desktop\opera_proj\образец скриптов\check_post.comi"

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

get_logs(flag=1)