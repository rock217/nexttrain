
import urllib
import json
import time

class predict:
    json = {}
    last_fetch = 0.0

    def getDataForStop(self, place):
        data = None
        try:
            connection = urllib.urlopen('http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key=wX9NwuHnZU2ToO7GmGR9uw&stop='+place+'&format=json')
            data = json.loads(connection.read())
            connection.close()

        finally:
            return data

    def gettraintimes(self):
        place = 'place-grnst'
        place = 'place-sstat'
        currentTime = time.time()
        data = {}
        if (not bool(self.json) or currentTime - self.last_fetch > 15):
            print "fetching data"
            self.json = self.getDataForStop(place)
            self.last_fetch = currentTime

        for mode in self.json["mode"]:
            if mode["mode_name"] == "Subway":
                for route in mode["route"]:
                    for direction in route["direction"]:
                        for trip in direction["trip"]:
                            if "trip_headsign" in trip and trip["trip_headsign"] == 'Alewife':
                                if trip["trip_headsign"] not in data:
                                    data[trip["trip_headsign"]] = []
                                data[trip["trip_headsign"]].append(float(trip["pre_away"]))


        return data
