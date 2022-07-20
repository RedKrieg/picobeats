from machine import Pin
from time import sleep_ms
from chirp import Chirper

# just a demo, blink a couple times to indicate startup
led = machine.Pin("LED", machine.Pin.OUT)
for i in range(4):
    led.toggle()
    sleep_ms(500)

# we have 4 voices on pio 4-7 tied to gpio 2-5
voices = [ Chirper(i+4, i+2, 96000) for i in range(4) ]
buttons = [ Pin(i+12, Pin.IN, Pin.PULL_UP) for i in range(4) ]
button_states = [ False for i in range(4) ]

while True:
    for i, button in enumerate(buttons):
        val = button.value()
        if not val and not button_states[i]:
            button_states[i] = True
            voices[i].play(25*(i+4))
        elif button_states[i] and val:
            button_states[i] = False
    if all(button_states):
        break
    sleep_ms(5)