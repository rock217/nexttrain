
import urllib
import json
import time

class predictor:
    __api_key = None
    __place = None
    __filter = None

    __data = None
    __last_fetch = 0.0

    def __init__(self, api_key, place, filter = None):
        self.__api_key = api_key
        self.__place = place
        self.__filter = filter

    def __get_data(self):
        data = None
        try:
            url = 'http://realtime.mbta.com/developer/api/v2/predictionsbystop?api_key='+self.__api_key +'&stop='+self.__place+'&format=json'
            print url
            connection = urllib.urlopen(url)
            data = json.loads(connection.read())
            #print data
            connection.close()

        finally:
            if data is None:
                raise ValueError('Network Error')
            return data

    def get_train_times(self):
        currentTime = time.time()
        ret = {
            "alert":"",
            "trains":{},
            "time":0
        }

        if currentTime - self.__last_fetch > 15:
            self.__data = self.__get_data()
            self.__last_fetch = currentTime

        if "alert_headers" in self.__data and len(self.__data["alert_headers"]) > 0:
            message = ""
            for alert in self.__data["alert_headers"]:
                message += alert["header_text"]+"  "
            ret["alert"]=message
        for mode in self.__data["mode"]:
            if mode["mode_name"] == "Subway":
                for route in mode["route"]:
                    for direction in route["direction"]:
                        for trip in direction["trip"]:
                            if "trip_headsign" in trip:
                                if(bool(self.__filter) and self.__filter != trip["trip_headsign"]):
                                    continue
                                if trip["trip_headsign"] not in ret["trains"]:
                                    ret["trains"][trip["trip_headsign"]] = []
                                ret["trains"][trip["trip_headsign"]].append(float(trip["pre_away"]))
        ret["time"]=time.time()
        return ret
