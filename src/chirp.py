from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

@asm_pio(sideset_init=PIO.OUT_LOW)
def chirp_prog():
    pull(block).side(0)
    mov(x, osr)
    label("startloop")
    mov(y, x).side(1)
    label("waithigh")
    jmp(y_dec, "waithigh")
    mov(y, x).side(0)
    label("waitlow")
    jmp(y_dec, "waitlow")
    jmp(x_dec, "startloop")
    
    
class Chirper:
    def __init__(self, sm_id, pin, base_freq=96000):
        self._sm = StateMachine(sm_id, chirp_prog, freq=base_freq, sideset_base=Pin(pin))
        self._sm.active(1)
    
    def play(self, value):
        self._sm.exec("set(x, 0)") # immediately short-circuit loop
        self._sm.put(value)
