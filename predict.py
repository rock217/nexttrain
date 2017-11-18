
import urllib
import json

def getDataForStop(place):
    raw = None
    try:
        connection = urllib.urlopen('http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key=wX9NwuHnZU2ToO7GmGR9uw&stop='+place+'&format=json')
        raw = json.loads(connection.read())
        connection.close()

    finally:
        return raw

def getTrainTimes():
    place = 'place-grnst'
    place = 'place-sstat'
    json = getDataForStop(place)

    data = {}
    for mode in json["mode"]:
        if mode["mode_name"] == "Subway":
            for route in mode["route"]:
                for direction in route["direction"]:
                    for trip in direction["trip"]:
                        if "trip_headsign" in trip and trip["trip_headsign"] == 'Alewife':
                            if trip["trip_headsign"] not in data:
                                data[trip["trip_headsign"]] = []
                            data[trip["trip_headsign"]].append(int(trip["pre_away"]))


    return data