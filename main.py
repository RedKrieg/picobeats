import ball
import chirp
import picounicorn
import time

target_fps = 30

ticks_per_frame = 1000 // target_fps # rough, but err faster than slower

print("init")
picounicorn.init()

# for some reason this crashes thonny
#led = Pin("LED", Pin.OUT)
#print("led defined")
#for i in range(4):
#    print("toggling")
#    led.toggle()
#    sleep_ms(500)

# we have 4 voices on pio 4-7 tied to gpio 2-5
voices = [ chirp.Chirper(i+4, i+2, 96000) for i in range(4) ]
buttons = [ picounicorn.BUTTON_A, picounicorn.BUTTON_B, picounicorn.BUTTON_X, picounicorn.BUTTON_Y ]
button_states = [ False for i in range(4) ]

b = ball.Ball(picounicorn.get_width(), 1)

def clear_leds(color=(0, 0, 0)):
    for x in range(picounicorn.get_width()):
        for y in range(picounicorn.get_height()):
            picounicorn.set_pixel(x, y, *color)

while True:
    start = time.ticks_ms()
    for i, button in enumerate(buttons):
        val = picounicorn.is_pressed(button)
        if val and not button_states[i]:
            button_states[i] = True
            voices[i].play(25*(i+4))
        elif button_states[i] and not val:
            button_states[i] = False
    if all(button_states):
        break
    clear_leds()
    b.move()
    b.render()
    end = time.ticks_ms()
    time.sleep_ms(ticks_per_frame + time.ticks_diff(start, end))