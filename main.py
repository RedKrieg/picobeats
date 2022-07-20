import ball
import bat
import chirp
import picounicorn
import time

target_fps = 60

ticks_per_frame = 1000 // target_fps # rough, but err faster than slower

print("init")
picounicorn.init()

# we have 4 voices on pio 4-7 tied to gpio 2-5
voices = [ chirp.Chirper(i+4, i+2, 96000) for i in range(4) ]
buttons = [ picounicorn.BUTTON_A, picounicorn.BUTTON_B, picounicorn.BUTTON_X, picounicorn.BUTTON_Y ]

width = picounicorn.get_width()
height = picounicorn.get_height()

lanes = [1, 5]

balls = [
    ball.Ball(width, lanes[0]),
    ball.Ball(width, lanes[1], position=width - 1)
    ]

bats = [
    bat.Bat(buttons[0], balls[0], voices[0], 0, lanes[0]),
    bat.Bat(buttons[2], balls[0], voices[1], width - 1, lanes[0]),
    bat.Bat(buttons[1], balls[1], voices[2], 0, lanes[1]),
    bat.Bat(buttons[3], balls[1], voices[3], width - 1, lanes[1])
    ]

def clear_leds(color=(0, 0, 0)):
    for x in range(picounicorn.get_width()):
        for y in range(picounicorn.get_height()):
            picounicorn.set_pixel(x, y, *color)

while True:
    start = time.ticks_ms()

    # update bat before ball to allow for hits
    for bt in bats:
        bt.update()
    for bl in balls:
        bl.update()

    # start rendering
    clear_leds()
    for bt in bats:
        bt.render()
    for bl in balls:
        bl.render()

    # wait for next frame
    end = time.ticks_ms()
    time.sleep_ms(ticks_per_frame + time.ticks_diff(start, end))
