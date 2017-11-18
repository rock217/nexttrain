import atexit
import Image
import ImageDraw
import ImageFont
import os
import time
import math
from predict import predict

from rgbmatrix import Adafruit_RGBmatrix


# Configuration
fps            = 5
width          = 64  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.
matrix         = Adafruit_RGBmatrix(32, 2) # rows, chain length

orangeLineOrange     = (255, 130, 0) # Color for route labels (usu. numbers)
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
greenLineGreen = (66, 134, 8)
font           = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')

# Main application -----------------------------------------------------------

# Drawing takes place in offscreen buffer to prevent flicker
image       = Image.new('RGB', (width, height))
draw        = ImageDraw.Draw(image)

# Clear matrix on exit.  Otherwise it's annoying if you need to break and
# fiddle with some code while LEDs are blinding you.
def clearOnExit():
	matrix.Clear()

atexit.register(clearOnExit)

train_stop = predict()

currentTime = 0.0
prevTime    = 0.0
# Event loop
while True:
	data = train_stop.gettraintimes()
	print data
	# Draw Stuff
	draw.rectangle((0, 0, width, height), fill=orangeLineOrange)
	draw.rectangle((1, 1, width-2, height-2), fill=black)
	#draw.rectangle((1, 1, width-2, 10), fill=white)

	draw.line((0, 10, width, 10), fill=orangeLineOrange)

	for label, times in data.items():
		times.sort()
		times = [x / 60 for x in times[0:3]]
		minutes = []
		for duration in times:
			minutes.append(int(math.ceil((duration))))

		print minutes
		draw.text((2, 0), "To:  "+label, font=font, fill=orangeLineOrange)
		draw.text((2, 10), ", ".join(map(str, minutes)) +" mins. ", font=font, fill=white)

	draw.text((5, 20), "   No Delays! ", font=font, fill=greenLineGreen)


	# Timing
	currentTime = time.time()
	timeDelta = (1.0 / fps) - (currentTime - prevTime)
	if (timeDelta > 0.0):
		time.sleep(timeDelta)
	prevTime = currentTime

	# Offscreen buffer is copied to screen
	matrix.SetImage(image.im.id, 0, 0)


text = raw_input("Press enter to exit...")