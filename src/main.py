import buffer
import chirp
import game
import scroll
import picounicorn
import time

picounicorn.init()

# we have 4 voices on pio 4-7 tied to gpio 2-5
voice_count = 4
voice_hz = 96000
voice_pio_offset = 4
voice_gpio_offset = 2
voices = [ chirp.Chirper(i+voice_pio_offset, i+voice_gpio_offset, voice_hz) for i in range(voice_count) ]

# each player has a buttons tuple and a colors tuple
buttons = ((picounicorn.BUTTON_A, picounicorn.BUTTON_B), (picounicorn.BUTTON_X, picounicorn.BUTTON_Y))
colors = ((255, 0, 0), (0, 0, 255))
color_names = ("Red", "Blue")
win_counts = [0, 0]

width = picounicorn.get_width()
height = picounicorn.get_height()

# render to a buffer so the leds don't flicker
buf = buffer.Buffer(width, height)
s = scroll.Scroller(buf, framerate=30)

# y coordinates of the lanes we use
lanes = (1, 4)

s.scroll("PicoBeats", (64, 128, 64))

while True:
    g = game.Game(voices, buttons, lanes, buf, colors, debug=False)
    winner = 0 if g.play() else 1
    win_counts[winner] += 1
    for voice in voices:
        voice.play(200)
        time.sleep_ms(50)
    s.scroll(f"{color_names[winner]} Wins!", colors[winner])
    for i in range(2):
        s.scroll(f"{color_names[i]}: {win_counts[i]}", colors[i])
