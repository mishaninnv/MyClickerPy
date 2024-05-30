import tkinter
from tkinter import *
import pyautogui
import time
import keyboard
import threading
from pynput import keyboard as nputkeyboard
from pynput import mouse as nputmouse
import datetime


## Получаем время между событиями
def get_time():
    global time_start
    if time_start == 0:
        time_start = datetime.datetime.now()

    time_finish = datetime.datetime.now()
    delta_time = (time_finish - time_start).microseconds / 1000000
    time_start = time_finish
    return delta_time


## Отбираем полученные клавиши и приводим их к валидному значению
def validation_key(key):
    valid_key = str(key).replace('\'', '').replace('<', '').replace('>', '')
    if 'ctrl' in str(key):
        return 'ctrl'
    elif 'alt' in str(key):
        return 'alt'
    elif 'shift' in str(key):
        return 'shift'
    elif 'right' in str(key):
        return 'right'
    elif 'left' in str(key):
        return 'left'
    elif 'down' in str(key):
        return 'down'
    elif 'up' in str(key):
        return 'up'
    elif 'space' in str(key):
        return 'space'
    elif valid_key in hotkeys_symbols:
        return hotkeys_symbols[valid_key]
    else:
        return valid_key


## Добавляем событие клика мышкой в список
def on_click(x, y, button, pressed):
    if pressed:
        delta_time = get_time()
        mouse_key = str(button).replace('Button.', '')
        actions.append(['mouse', delta_time, x, y, mouse_key])


## Добавляем событие нажатия кнопки в список
def on_press(key):
    press_key = validation_key(key)
    last_pressed_key = actions[-1][3] if len(actions) > 0 else ''
    mode_key = actions[-1][4] if len(actions) > 0 else ''
    if last_pressed_key == press_key and mode_key == 'pressed':
        return

    delta_time = get_time()
    actions.append(['keyboard', delta_time, 'key', press_key, 'pressed'])
    print(f'Нажатая кнопка - {key}. Валидное значение - {press_key}.')


## Добавляем событие отжатия кнопки в список
def on_release(key):
    if validation_key(key) in special_keys:
        delta_time = get_time()
        actions.append(['keyboard', delta_time, 'key', validation_key(key), 'release'])
        print(f'Отжатая кнопка {key}')


## Классификация произошедшего события по группам
def validation_action(action):
    print(f'Валидируем событие - {action[0]}, {action[1]}, {action[2]}, {action[3]}')
    time.sleep(action[1] / int(increase_time.get()))
    if action[0] == 'mouse':
        pyautogui.click(action[2], action[3], button=action[4])
    elif action[3] in special_keys:
        if action[4] == 'pressed':
            pyautogui.keyDown(action[3])
        else:
            pyautogui.keyUp(action[3])
    else:
        pyautogui.press(action[3])


## Включение режима записи действий пользователя
def write_script():
    key_listener.start()
    mouse_listener.start()


## Отключение режима записи действий пользователя
def stop_listener():
    global key_listener, mouse_listener
    key_listener.stop()
    mouse_listener.stop()
    key_listener = nputkeyboard.Listener(on_press=on_press)
    mouse_listener = nputmouse.Listener(on_click=on_click)
    if actions[0][3] == 'alt' or actions[0][3] == 'r' or actions[0][3] == 'к': del actions[0]
    if actions[0][3] == 'alt' or actions[0][3] == 'r' or actions[0][3] == 'к': del actions[0]
    if actions[-1][3] == 'alt' or actions[0][3] == 's' or actions[0][3] == 'ы': del actions[-1]
    if actions[-1][3] == 'alt' or actions[0][3] == 's' or actions[0][3] == 'ы': del actions[-1]
    print('\n'.join(str(value) for value in actions))  # потом убрать


## Очистка ранее записанных событий
def clear_script():
    global time_start, time_finish, actions
    actions = []
    time_start = 0
    time_finish = 0


## Запуск повторения событий содержащихся в списке
def start_script():
    global count, run_my_script
    counter = int(count.get())
    while counter > 0 and run_my_script:
        for action in actions:
            if run_my_script:
                validation_action(action)
        counter -= 1


def start_script_thread():
    global run_my_script
    run_my_script = True
    thread = threading.Thread(target=start_script)
    thread.start()


def stop_script():
    global run_my_script
    run_my_script = False


#increase_time = int(input('Во сколько раз ускорить: '))
#count = int(input('Сколько раз повторить: '))
run_my_script = True
special_keys = ['shift', 'ctrl', 'alt', 'left', 'right', 'up', 'down', 'space']
hotkeys_symbols = {'\\x01': 'a', '\\x03': 'c', '\\x16': 'v'}
actions = []
time_start = 0
time_finish = 0
key_listener = nputkeyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = nputmouse.Listener(on_click=on_click)

keyboard.add_hotkey('alt+r', write_script)
keyboard.add_hotkey('alt+d', clear_script)
keyboard.add_hotkey('alt+a', start_script_thread)
keyboard.add_hotkey('alt+s', stop_listener)
keyboard.add_hotkey('alt+x', stop_script)

window = Tk()

## Глобальные переменные которые будут отображаться в интерфейсе
##count_var = StringVar()
##count_var.set(count)

window.title("Добро пожаловать")
##window.geometry('400x250')

lbl = Label(window, text="Во сколько ускорить: ")
lbl.grid(column=0, row=0, sticky=W)
increase_time = Entry(window, width=10)
increase_time.insert(0, 1)
increase_time.grid(column=1, row=0)

lbl = Label(window, text="Сколько раз повторить: ")
lbl.grid(column=0, row=1, sticky=W)
count = Entry(window, width=10)
count.insert(0, 1)
count.grid(column=1, row=1)

lbl = Label(window, text="")
lbl.grid(column=0, row=2, columnspan=2, sticky=W)

lbl = Label(window, text="Начать запись - alt+r")
lbl.grid(column=0, row=3, columnspan=2, sticky=W)
lbl = Label(window, text="Закончить запись - alt+s")
lbl.grid(column=0, row=4, columnspan=2, sticky=W)
lbl = Label(window, text="Сбросить записанные данные - alt+d")
lbl.grid(column=0, row=5, columnspan=2, sticky=W)
lbl = Label(window, text="Начать выполнение - alt+a")
lbl.grid(column=0, row=6, columnspan=2, sticky=W)
lbl = Label(window, text="Остановить выполнение - alt+x")
lbl.grid(column=0, row=7, columnspan=2, sticky=W)

window.resizable(False, False)
window.mainloop()