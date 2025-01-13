import get_harmonics
import pyautogui
import time

from datetime import datetime

def start_clicker():
    for i in range(0):
        result = True
        start = datetime.now()

        # Тут главное не сбивать положение папок
        start_x, start_y = 2800, 500  # Координаты начального положения файла
        end_x, end_y = 1700, 500  # Координаты конечного положения (куда нужно перенести файл)
        pyautogui.moveTo(start_x, start_y)  # Переходим к начальной позиции файла
        pyautogui.mouseDown()  # Нажимаем и удерживаем левую кнопку мыши
        time.sleep(0.5)  # Небольшая задержка для естественности (опционально)

        pyautogui.dragTo(end_x, end_y, duration=0.5)  # Перетаскиваем .comi из одной папки в другую. duration - время
        pyautogui.mouseUp()  # Отпускаем левую кнопку мыши
        time.sleep(0.5)  # Небольшая задержка для естественности (опционально)


        # Запускаем оперу
        x_opera_open, y_opera_open = 500, 1220  # координаты местоположения ярлыка запуска оперы
        pyautogui.moveTo(x_opera_open, y_opera_open)  # перемещение курсора в это место
        pyautogui.click()  # двойной клик
        pyautogui.click()
        time.sleep(7)  # ждем пока опера запустится и прогрузится


        # Запускаем comi файл
        x_file_open, y_file_open = 40, 60  # координаты выбора окна File в опере
        pyautogui.moveTo(x_file_open, y_file_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 80, 390  # координаты места, необоходимого для загрузки файл
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 600, 560  # выбираем папку 'локальная папка' из списка
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 600, 350  # выбираем конкретный .comi файл из списка - вообще он 1
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        pyautogui.click()


        # Задержка на время построения и вычислений. В среднем это 90 сек, но можно сделать больше (например 140)
        time.sleep(105)


        # Тут тапаем на значок расчетчика, чтобы он открылся поверх всех остальных окон.
        # ВАЖНО - ЗАКРОЙТЕ ВСЕ ОКНА КРОМЕ PYCHARM, иначе вылезет ошибка
        x_comi_open, y_comi_open = 1970, 1950  # координаты места снизу на панели, где находится окно с расчетчиком
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()

        time.sleep(0.5)

        x_comi_open, y_comi_open = 1950, 1800  # тыкаем по окну с вычислениями
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 1750, 1180  # нажимаем на post processor
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(6) # время на открытие пост процессора


        # Итак, работаем с пост процессором
        x_file_open, y_file_open = 40, 60  # открываем File для загрузки скрипта
        pyautogui.moveTo(x_file_open, y_file_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 80, 500  # нажимаем на окно загрузки скрипта
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 500, 350  # выбираем скрипт .comi из папки
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        pyautogui.click()
        time.sleep(1)

        x_comi_open, y_comi_open = 3150, 20  # закрываем приложение пост процессора для удаления логов
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 1600, 1030  # подтверждаем закрытие
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 3150, 20  # закрываем приложение моделера для удаления логов
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        x_comi_open, y_comi_open = 1600, 1030  # подтверждаем закрытие
        pyautogui.moveTo(x_comi_open, y_comi_open)
        pyautogui.click()
        time.sleep(0.5)

        # result = subprocess.run(["python", "get_harmonics.py"],
        #                         capture_output=True)  # запускаем файл, который удаляет логи и пишет в таблицу расчет

        result = get_harmonics.get_harmonics()  # запускаем файл, который удаляет логи и пишет в таблицу расчет
        time.sleep(0.1)

        end = datetime.now()
        print(f'{i}) время выполнения {(end - start).seconds}')

        if result:
            print('Ошибка выполнения')
            return

start_clicker()