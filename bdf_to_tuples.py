import bdfparser

# this generates the font.py we actually send to the rpi pico

font = bdfparser.Font('5x7.bdf')

font_data = {}

for glyph in font.iterglyphs(r=[(0x0, 0x7F)]):
    font_data[glyph.cp()] = tuple(tuple(int(x) for x in y) for y in glyph.draw().bindata)

font_tuples = tuple(font_data[i] if i in font_data else () for i in range(128))

with open("src/font.py", 'w') as f:
    print("from micropython import const", file=f)
    print("font=const((", file=f)
    for tup in font_tuples:
        print("    (", file=f)
        for line in tup:
            print(f"        {line},", file=f)
        print("    ),", file=f)
    print("))", file=f)
