import atexit
import math
import os
import time

import Image
import ImageDraw
import ImageFont

from predictor import predictor
from rgbmatrix import Adafruit_RGBmatrix

# Configuration
api_key = 'wX9NwuHnZU2ToO7GmGR9uw'
place = 'place-grnst'
filter = 'Oak Grove'
station_label = " To Oak Grove"

fps            = 4
width          = 64  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.
matrix         = Adafruit_RGBmatrix(32, 2) # rows, chain length

green          = (0, 132, 69)
red            = (225, 39, 38)
orange         = (232, 116, 36)
blue           = (15, 75, 145)
silver         = (125, 134,140)
plum           = (194, 147, 181)
aqua           = (216, 240, 252)
white          = (255, 255, 255)
black          = (0, 0, 0)
themecolor     = orange
font           = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')

# Custom Settings
if 1==0 :
	place = 'place-sstat'
	filter = 'Alewife'
	station_label = "North to Alewife"
	themecolor = red

# Main application -----------------------------------------------------------

# Drawing takes place in offscreen buffer to prevent flicker
image       = Image.new('RGB', (width, height))
draw        = ImageDraw.Draw(image)

# Clear matrix on exit.  Otherwise it's annoying if you need to break and
# fiddle with some code while LEDs are blinding you.
def clearOnExit():
	matrix.Clear()
atexit.register(clearOnExit)
train_stop_predictor = predictor(api_key, place, filter)

# Splash Screen



currentTime = 0.0
prevTime    = 0.0
error = None
errlen = 0
# Event loop
while True:
	data = {}
	try:
		data = train_stop_predictor.get_train_times()
	except ValueError as e:
		error = str(e)
		if errlen <= 0:
			errlen = float(font.getsize(error)[0])
			errlen2 = errlen
			errlen += 64
	# Draw Stuff
	draw.rectangle((0, 0, width, height), fill=black)

	if bool(error) and errlen > 0:
		draw.text((6, 10), "No Train Data.", font=font, fill=white)
		draw.text((1 - (errlen2 - errlen), 20), error, font=font, fill=red)
		errlen = errlen - .75

	else:

		for label, times in data.items():
			times.sort()
			times = [x / 60 for x in times[0:4]]
			minutes = []
			for duration in times:
				minutes.append(int(math.ceil((duration))))
			draw.text((2, 10), ",".join(map(str, minutes)) +" mins. ", font=font, fill=white)
 
	draw.text((1, 0), station_label, font=font, fill=themecolor)

	draw.line((0, 0, width, 0), fill=themecolor)                   # top
	draw.line((0, 10, width, 10), fill=themecolor)                 # middle
	draw.line((0, height-1, width, height-1), fill=themecolor)     # bottom
	draw.line((0, 0, 0, height), fill=themecolor)                  # left
	draw.line((width - 1, 0, width - 1, height), fill=themecolor)  # right


	separator = ":" if int(time.time()) % 2 == 0 else " "
	time_label = time.strftime("%b %d %H"+separator+"%M")
	draw.text((5, 20), time_label, font=font, fill=green)
	# Timing
	currentTime = time.time()
	timeDelta = (1.0 / fps) - (currentTime - prevTime)
	if (timeDelta > 0.0):
		time.sleep(timeDelta)
	prevTime = currentTime

	# Offscreen buffer is copied to screen
	matrix.SetImage(image.im.id, 0, 0)
	print "tick"