import atexit
import math
import os
import time

import resource

from predictor import predictor

# Configuration
api_key = '9ChpTppjokGjY-FGPKhmSA'
place = 'place-grnst'
filter = 'Oak Grove'
station_label = " Green to Oak G."

train_stop_predictor = predictor(api_key, place, filter)
fps            = 1
currentTime     = 0.0
prevTime        = 0.0
prevSaveTime    = 0.0
error           = None

# Event loop

while True:
	data = {}
	try:
		data = train_stop_predictor.get_train_times()
	except ValueError as e:
		if(error != None):
			error = str(e)
			print error
	# Draw Stuff
	output = ''
	if bool(error) :
		output+= "No Train Data.  "+error
	else:
		for label, times in data.items():
			times.sort()
			times = [x / 60 for x in times[0:3]]
			redminutes = []
			whiteminutes = []
			for duration in times:
				duration = int(duration)

				if(duration < 5):
					redminutes.append(duration)
				else:
					whiteminutes.append(duration)

			redminuteslabel = ", ".join(map(str, redminutes))
			if(redminuteslabel):
				redminuteslabel = redminuteslabel+", "
			whiteminuteslabel = ", ".join(map(str, whiteminutes))+" mins "
			output+=redminuteslabel+whiteminuteslabel
	output = station_label + "\n"+output

	separator = ":" if int(time.time()) % 2 == 0 else " "
	time_label = time.strftime("%b %d %-I"+separator+"%M%p")
	output+= "\n"+time_label

	# Timing
	currentTime = time.time()
	timeDelta = (1.0 / fps) - (currentTime - prevTime)
	if (timeDelta > 0.0):
		time.sleep(timeDelta)
	prevTime = currentTime
	#print output
	print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss