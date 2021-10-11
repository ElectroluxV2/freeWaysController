import time
from pyray import *
import numpy as np
from pynput.mouse import Button, Controller
from pynput import keyboard

set_config_flags(FLAG_WINDOW_TRANSPARENT | FLAG_WINDOW_RESIZABLE)
init_window(800, 600, b'Transparency Test')
mouse = Controller()
break_loop = False


def on_activate(key):
    if key == keyboard.Key.f7:
        global break_loop
        break_loop = True


def lin_equ(start, end):
    if start.x == end.x:
        return lambda x: x

    left = np.array([[start.x, 1], [end.x, 1]])
    right = np.array([start.y, end.y])
    result = np.linalg.solve(left, right)

    a = result[0]
    b = result[1]

    return lambda x: a * x + b


def simulate(start, end, window):
    global mouse
    global break_loop
    real_start = Vector2(start.x + window.x, start.y + window.y)
    real_end = Vector2(end.x + window.x, end.y + window.y)
    lin_func = lin_equ(real_start, real_end)

    print('start')

    minimize_window()
    time.sleep(0.1)
    mouse.position = (real_start.x, real_start.y)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)

    total_steps = abs(real_end.x - real_start.x)
    total_time = 1
    sleep_time = total_time / (total_steps if total_time != 0 else 5)

    start_x = real_start.x
    end_x = real_end.x

    for x in range(int(start_x), int(end_x) + 1, -1 if start_x > end_x else 1):
        if break_loop:
            print('break')
            break_loop = False
            restore_window()
            maximize_window()
            break

        mouse.position = (x, lin_func(x))
        time.sleep(sleep_time)

    time.sleep(0.1)
    mouse.release(Button.left)
    time.sleep(0.1)
    restore_window()
    maximize_window()

    print('done')


def main():
    start = Vector2(200, 200)
    end = Vector2(500, 500)
    line = lin_equ(start, end)

    while not window_should_close():
        begin_drawing()
        clear_background([0, 0, 0, 1])

        draw_line_v(start, end, [255, 0, 0, 255]);

        # draw_pixel(int(start.x), int(line(start.x)), [255, 0, 0, 255])
        # draw_pixel(int(end.x), int(line(end.x)), [255, 0, 0, 255])
        #
        # for x in range(int(min(start.x, end.x)), int(max(start.x, end.x))):
        #     draw_pixel(x, int(line(x)), [0, 255, 0, 255])

        mouse_position = get_mouse_position()
        window_position = get_window_position()

        if is_mouse_button_down(MOUSE_LEFT_BUTTON):
            start = mouse_position
            line = lin_equ(start, end)
        elif is_mouse_button_down(MOUSE_RIGHT_BUTTON):
            end = mouse_position
            line = lin_equ(start, end)

        if is_key_pressed(KEY_SPACE):
            simulate(start, end, window_position)

        end_drawing()


keyboard.Listener(on_press=on_activate).start()
main()
