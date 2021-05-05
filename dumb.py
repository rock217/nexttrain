import atexit
import math
import os
import time

import resource

from predictor import predictor

train_stop_predictor = predictor()
fps = 1
currentTime = 0.0
prevTime = 0.0
prevSaveTime = 0.0
error = None
station_label = "Green Street"
# Event loop

while True:
    data = {}
    try:
        data = train_stop_predictor.get_train_times()
    except ValueError as e:
        if (error != None):
            error = str(e)
            print(error)
    # Draw Stuff
    output = ''
    if bool(error):
        output += "No Train Data.  " + error
    else:
        data["trains"].sort()
        times = [x for x in data["trains"][0:3]]
        redminutes = []
        whiteminutes = []
        for minutes in times:
            if (minutes < 5):
                redminutes.append(int(minutes/60))
            else:
                whiteminutes.append(int(minutes/60))

        redminuteslabel = ", ".join(map(str, redminutes))
        if (redminuteslabel):
            redminuteslabel = redminuteslabel + ", "
        whiteminuteslabel = ", ".join(map(str, whiteminutes)) + " mins "
        output += redminuteslabel + whiteminuteslabel
    output = station_label + "\n" + output

    separator = ":" if int(time.time()) % 2 == 0 else " "
    time_label = time.strftime("%b %d %-I" + separator + "%M%p")
    output += "\n" + time_label

    # Timing
    currentTime = time.time()
    timeDelta = (1.0 / fps) - (currentTime - prevTime)
    if (timeDelta > 0.0):
        time.sleep(timeDelta)
    prevTime = currentTime
    print(output)
    print('Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
