import atexit
import resource
import os
import time
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from predictor import predictor

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Configuration
station_label = " Green to Oak G."

fps            = 10
width          = 64  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.

green          = (0, 132, 69)
yellow         = (232, 175, 125)
red            = (225, 39, 38)
orange         = (232, 116, 36)
blue           = (15, 75, 145)
silver         = (125, 134,140)
plum           = (194, 147, 181)
aqua           = (216, 240, 252)
white          = (200, 200, 200)
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

train_stop_predictor = predictor()

def drawBox():
    draw.line((0, 0, width, 0), fill=themecolor)  # top
    draw.line((0, 10, width, 10), fill=themecolor)  # middle

    draw.line((0, height - 1, width, height - 1), fill=themecolor)  # bottom
    draw.line((0, 0, 0, height), fill=themecolor)  # left
    draw.line((width - 1, 0, width - 1, height), fill=themecolor)  # right


# Splash Screen'

draw.text((1, 0),  "nexttrain v0.2", font=font, fill=yellow)
draw.text((1, 10), "rock217@gh", font=font, fill=white)
draw.text((1, 20), "loading data...", font=font, fill=green)
matrix.SetImage(image)

time.sleep(3)

prevTime        = 0.0
prevLogTime    = 0.0

# Event loop
def loop():
    global prevTime, prevLogTime
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
        datex = 31 + ((31 - float(font.getsize(date_label)[0])) / 2)
        draw.text((datex, 20), date_label, font=font, fill=green)

        separator = ":" if int(time.time()) % 2 == 0 else " "
        time_label = time.strftime("%-I" + separator + "%M")
        timex = 0 + ((30 - float(font.getsize(time_label)[0])) / 2)
        draw.text((timex, 20), time_label, font=font, fill=green)

        data["trains"].sort()
        times = [x for x in data["trains"][0:3]]
        redminutes = []
        whiteminutes = []
        if times:
            for thetime in times:

                if (thetime < 5*60):
                    redminutes.append(int(thetime/60))

                else:
                    whiteminutes.append(int(thetime/60))

            redminuteslabel = ", ".join(map(str, redminutes))
            if(redminuteslabel):
                redminuteslabel = redminuteslabel+", "
            whiteminuteslabel = ", ".join(map(str, whiteminutes))+" mins "

            xoff = 1 + ((62 - (font.getsize(redminuteslabel)[0] + font.getsize(whiteminuteslabel)[0]))/2)
            draw.text((xoff, 10), redminuteslabel , font=font, fill=red)
            draw.text((xoff+font.getsize(redminuteslabel)[0], 10), whiteminuteslabel, font=font, fill=white)
        else:
            whiteminuteslabel = "What trains?"
            xoff = 1 + ((62 - (font.getsize(whiteminuteslabel)[0]))/2)
            draw.text((xoff, 10), whiteminuteslabel, font=font, fill=white)


    # Timing
    timeDelta = (1.0 / fps) - (currentTime - prevTime)
    if (timeDelta > 0.0):
        time.sleep(timeDelta)
    prevTime = currentTime

    # Offscreen buffer is copied to screen
    matrix.SetImage(image)

    if(currentTime - prevLogTime > 60):
        prevLogTime = currentTime
        memory_info = 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(memory_info)


while True:
    loop()