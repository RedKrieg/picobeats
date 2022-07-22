import buffer
import chirp
import game
import picounicorn

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

width = picounicorn.get_width()
height = picounicorn.get_height()

# render to a buffer so the leds don't flicker
buf = buffer.Buffer(width, height)

# y coordinates of the lanes we use
lanes = (1, 4)

while True:
    g = game.Game(voices, buttons, lanes, buf, colors)
    winner = g.play()
