import atexit
import resource
import os
import time

import Image
import ImageDraw
import ImageFont
from rgbmatrix import Adafruit_RGBmatrix

from predictor import predictor

# Configuration
api_key = '9ChpTppjokGjY-FGPKhmSA'
place = 'place-grnst'
filter = 'Oak Grove'
station_label = " Green to Oak G."

fps            = 10
width          = 64  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.
matrix         = Adafruit_RGBmatrix(32, 2) # rows, chain length

green          = (0, 132, 69)
yellow         = (232, 175, 125)
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

def drawBox():
	draw.line((0, 0, width, 0), fill=themecolor)  # top
	draw.line((0, 10, width, 10), fill=themecolor)  # middle

	draw.line((0, height - 1, width, height - 1), fill=themecolor)  # bottom
	draw.line((0, 0, 0, height), fill=themecolor)  # left
	draw.line((width - 1, 0, width - 1, height), fill=themecolor)  # right


# Splash Screen'

draw.text((1, 0), "NextTrain v0.1", font=font, fill=yellow)
draw.text((1, 10), "Made by Rock!", font=font, fill=white)
draw.text((1, 20), "Loading Data...", font=font, fill=green)
matrix.SetImage(image.im.id, 0, 0)

time.sleep(3)

prevTime        = 0.0
prevSaveTime    = 0.0

# Event loop
def loop():
	global prevTime, prevSaveTime
	currentTime = time.time()
	data = {}
	error = None

	try:
		data = train_stop_predictor.get_train_times()
	except ValueError as e:
		error = str(e)

	# Draw Stuff
	draw.rectangle((0, 0, width, height), fill=black)

	if bool(error):
		draw.text((6, 10), "No Train Data.", font=font, fill=white)
		draw.text((1, 20), error, font=font, fill=red)

	else:
		drawBox()
		draw.text((1, 0), station_label, font=font, fill=yellow)

		date_label = time.strftime("%b %d")
		datex = 32 + ((31 - float(font.getsize(date_label)[0])) / 2)
		draw.text((datex, 21), date_label, font=font, fill=green)

		separator = ":" if int(time.time()) % 2 == 0 else " "
		time_label = time.strftime("%-I" + separator + "%M")
		timex = 1 + ((31 - float(font.getsize(time_label)[0])) / 2)
		draw.text((timex, 21), time_label, font=font, fill=green)

		for label, times in data["trains"].items():
			times.sort()
			times = [x / 60 for x in times[0:3]]
			redminutes = []
			whiteminutes = []
			for duration in times:
				if(duration < 5):
					if duration <= .25:
						duration="A"
					else:
						duration = int(duration)
					redminutes.append(duration)
				else:
					whiteminutes.append(int(duration))

			redminuteslabel = ", ".join(map(str, redminutes))
			if(redminuteslabel):
				redminuteslabel = redminuteslabel+", "
			whiteminuteslabel = ", ".join(map(str, whiteminutes))+" mins "

			xoff = 1 + ((62 - (font.getsize(redminuteslabel)[0] + font.getsize(whiteminuteslabel)[0]))/2)

			draw.text((xoff, 10), redminuteslabel , font=font, fill=red)
			draw.text((xoff+font.getsize(redminuteslabel)[0], 10), whiteminuteslabel, font=font, fill=white)

	# Timing
	timeDelta = (1.0 / fps) - (currentTime - prevTime)
	if (timeDelta > 0.0):
		time.sleep(timeDelta)
	prevTime = currentTime
	# Offscreen buffer is copied to screen
	matrix.SetImage(image.im.id, 0, 0)
	if(currentTime - prevSaveTime > 60):
		image.save("/var/www/html/train.png")
		prevSaveTime = currentTime
		print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

while True:
	loop()