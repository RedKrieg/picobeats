import ball
import bat
import buffer
import chirp
import scoreboard
import picounicorn
import time

target_fps = 60

ticks_per_frame = 1000 // target_fps # rough, but err faster than slower

picounicorn.init()

# we have 4 voices on pio 4-7 tied to gpio 2-5
voices = [ chirp.Chirper(i+4, i+2, 96000) for i in range(4) ]
buttons = [ picounicorn.BUTTON_A, picounicorn.BUTTON_B, picounicorn.BUTTON_X, picounicorn.BUTTON_Y ]

width = picounicorn.get_width()
height = picounicorn.get_height()

# render to a buffer so the leds don't flicker
buf = buffer.Buffer(width, height)

# y coordinates of the lanes we use
lanes = [1, 4]

balls = [
    ball.Ball(width, lanes[0], width=2),
    ball.Ball(width, lanes[1], position=width - 1, speed=-1, width=2)
    ]

bats = [
    bat.Bat(buttons[0], balls[0], voices[0], 0, lanes[0], width=2),
    bat.Bat(buttons[2], balls[0], voices[1], width - 1, lanes[0], width=2),
    bat.Bat(buttons[1], balls[1], voices[2], 0, lanes[1], width=2),
    bat.Bat(buttons[3], balls[1], voices[3], width - 1, lanes[1], width=2)
    ]

sb = scoreboard.ScoreBoard(0, width - 1, width, height)

while True:
    start = time.ticks_ms()

    # update bat before ball to allow for hits
    for bt in bats:
        bt.update()
    for bl in balls:
        point=bl.update()
        if point is not None:
            sb.update(point)

    # start rendering
    buf.clear()
    sb.render(buf)
    for bt in bats:
        bt.render(buf)
    for bl in balls:
        bl.render(buf)

    # write to led array
    buf.render()

    # wait for next frame
    end = time.ticks_ms()
    wait_for = ticks_per_frame + time.ticks_diff(start, end)
    print(f"Waiting for {wait_for:>3}ms")
    time.sleep_ms(wait_for)
