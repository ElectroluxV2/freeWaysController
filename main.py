import time
from pyray import *
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

    # 2 points line
    if start.x == end.x:
        return {
            'x': lambda x: x,
            'y': lambda y: y
        }

    slope = (end.y - start.y) / (end.x - start.x)
    intercept = start.y - slope * start.x

    print(f'')

    if slope == 0:
        return {
            'x': lambda x: x + intercept,
            'y': lambda y: y
        }

    return {
        'x': lambda x: slope * x + intercept,
        'y': lambda y: (y - intercept) / slope
    }

def simulate(start, end, window):
    global mouse
    global break_loop
    real_start = Vector2(start.x + window.x, start.y + window.y)
    real_end = Vector2(end.x + window.x, end.y + window.y)
    lin_func = lin_equ(real_start, real_end)

    start_x = int(real_start.x)
    end_x = int(real_end.x)

    start_y = int(real_start.y)
    end_y = int(real_end.y)

    points_based_on_x_axis = abs(start_x - end_x)
    points_based_on_y_axis = abs(start_y - end_y)

    print(f'points_based_on_x_axis: {points_based_on_x_axis}')
    print(f'points_based_on_y_axis: {points_based_on_y_axis}')

    minimize_window()
    time.sleep(0.1)
    mouse.position = (real_start.x, real_start.y)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(0.1)

    total_steps = points_based_on_x_axis if points_based_on_x_axis >= points_based_on_y_axis else points_based_on_y_axis
    total_time = 1
    sleep_time = total_time / (total_steps if total_time != 0 else 5)


    if points_based_on_x_axis >= points_based_on_y_axis:
        for x in range(start_x, end_x + 1, -1 if start_x > end_x else 1):
            if break_loop:
                print('break')
                break_loop = False
                restore_window()
                maximize_window()
                break
            y = lin_func['x'](x)

            mouse.position = (x, y)
            time.sleep(sleep_time) 
    else:
        for y in range(start_y, end_y + 1, -1 if start_y > end_y else 1):
            if break_loop:
                print('break')
                break_loop = False
                restore_window()
                maximize_window()
                break
            x = lin_func['y'](y)

            mouse.position = (x, y)
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

        draw_line_v(start, end, [255, 0, 0, 255])

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
