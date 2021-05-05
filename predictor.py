
import urllib.request
import json
import time
import datetime
class predictor:

    __data = None
    __last_fetch = 0.0

    def __get_data(self):
        data = None
        try:
            url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-grnst&filter[direction_id]=0'
            connection = urllib.request.urlopen(url)
            data = json.loads(connection.read())
            connection.close()
        except:
            print("rrer")
        finally:
            if data is None:
                raise ValueError('Network Error')
            return data

    def get_train_times(self):
        currentTime = time.time()
        ret = {
            "alert":"",
            "trains":[],
            "time":0
        }

        if currentTime - self.__last_fetch > 15:
            self.__data = self.__get_data()
            self.__last_fetch = currentTime


        for train in self.__data["data"]:

            traindatetime = train["attributes"]["departure_time"]
            traintimestamp = time.mktime(datetime.datetime.strptime(traindatetime, "%Y-%m-%dT%H:%M:%S%z").timetuple())

            ret["trains"].append(int(traintimestamp - currentTime))

        ret["time"] = currentTime
        return ret
