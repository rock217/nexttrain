
import urllib
import json
import time

class predictor:
    __api_key = None
    __json = None
    __last_fetch = 0.0
    __place = None
    __filter = None

    def __init__(self, api_key, place, filter = None):
        self.__api_key = api_key
        self.__place = place
        self.__filter = filter

    def __get_data(self):
        data = None
        try:
            connection = urllib.urlopen('http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key='+self.__api_key +'&stop='+self.__place+'&format=json')
            data = json.loads(connection.read())
            connection.close()

        finally:
            return data

    def get_train_times(self):
        currentTime = time.time()
        if (not bool(self.__json) or currentTime - self.__last_fetch > 15):
            self.__json = self.__get_data()
            self.__last_fetch = currentTime
        if self.__json is None:
            message = 'Cannot process data feed from MBTA.'
            raise ValueError(message)
        elif "alert_headers" in self.__json and len(self.__json["alert_headers"]) > 0:
            message = ""
            for alert in self.__json["alert_headers"]:
                message += alert["header_text"]+"  "
        data = {}
        for mode in self.__json["mode"]:
            if mode["mode_name"] == "Subway":
                for route in mode["route"]:
                    for direction in route["direction"]:
                        for trip in direction["trip"]:
                            if "trip_headsign" in trip:
                                if(bool(self.__filter) and self.__filter != trip["trip_headsign"]):
                                    continue
                                if trip["trip_headsign"] not in data:
                                    data[trip["trip_headsign"]] = []
                                data[trip["trip_headsign"]].append(float(trip["pre_away"]))
        return data
