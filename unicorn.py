import picounicorn

picounicorn.init()

w = picounicorn.get_width()
h = picounicorn.get_height()

for x in range(w):
    for y in range(h):
        picounicorn.set_pixel(x, y, 255, 0, 0)
        
