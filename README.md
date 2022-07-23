Picobeats
====

This is a [SEGA Flashbeats](https://www.arcade-museum.com/game_detail.php?game_id=17932) inspired minigame for the [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/), [Pimoroni Pico Unicorn Pack](https://pimoroni.com/picounicorn), and optionally something to make some sound.

Requirements
----

You'll need Pimoroni's picounicorn module to run this.  As of this writing, the easiest way is to flash their micropython .uf2 file for your Pico.

Gameplay
----

Push the center line to your opponent's end of the board to win.

Installation
----

Game files are in the src/ directory.  Make sure you have the latest Pimoroni [release](https://github.com/pimoroni/pimoroni-pico/releases/latest) of micropython for your board, then put all of the files in the src/ directory on to the device's root filesystem using one of [Thonny](https://thonny.org/), [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html), [ampy](https://github.com/scientifichackers/ampy), [mpfshell](https://github.com/wendlers/mpfshell), or another tool of your choosing.

Sound
----

Right now the sounds are limited to chirps emitted by four PIO "voices".  Each one goes to its own GPIO pin and I have them tied together as input to a passive piezo speaker.  There is no "music" currently and the sounds are only emitted when a ball is launched and at the end of each game.  Right now you're not missing much if you don't wire up sound hardware.

Font Info
----

The font used here is 5x7.bdf, a public domain font by [Dr Markus Kuhn](https://www.cl.cam.ac.uk/~mgk25/) that is included in the fonts-misc-misc bundle from [x.org's font releases](https://www.x.org/releases/individual/font/font-misc-misc-1.1.2.tar.gz).  I wrote a small script to use the [bdfparser](https://font.tomchen.org/bdfparser_py/) library to render this font to nested tuples of boolean values.  This gained a tiny amount of performance over a more naiive method, but in the long run I probably need to move the buffer code to C.
