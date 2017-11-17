import atexit
import Image
import ImageDraw
import ImageFont
import math
import os
import time

from rgbmatrix import Adafruit_RGBmatrix

width          = 64  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.
matrix         = Adafruit_RGBmatrix(32, 2) # rows, chain length

orangeLineOrange     = (255, 130, 0) # Color for route labels (usu. numbers)
font           = ImageFont.load(os.path.dirname(os.path.realpath(__file__))
                   + '/helvR08.pil')

# Main application -----------------------------------------------------------

# Drawing takes place in offscreen buffer to prevent flicker
image       = Image.new('RGB', (width, height))
draw        = ImageDraw.Draw(image)
currentTime = 0.0
prevTime    = 0.0

# Clear matrix on exit.  Otherwise it's annoying if you need to break and
# fiddle with some code while LEDs are blinding you.
def clearOnExit():
	matrix.Clear()

atexit.register(clearOnExit)

# Clear background
draw.rectangle((0, 0, width, height), fill=(0, 0, 0))

draw.text((10, 10), "Exodus Bagels", font=font,
          fill=orangeLineOrange)

# Offscreen buffer is copied to screen
matrix.SetImage(image.im.id, 0, 0)

text = raw_input("press any key to exit...")