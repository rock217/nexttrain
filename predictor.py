
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
            print('fetching data')
            url = 'https://api-v3.mbta.com/predictions?filter[stop]=place-grnst&filter[direction_id]=0'
            connection = urllib.request.urlopen(url)
            data = json.loads(connection.read())
            connection.close()
        except:
            print("error fetching feed")
        finally:
            if data is None:
                raise ValueError('Network Error')
            return data

    def get_train_times(self):
        currentTime = time.time()
        if currentTime - self.__last_fetch > 15:
            self.__data = self.__get_data()
            self.__last_fetch = currentTime

        ret = {
            "alert":"",
            "trains":[],
            "time":0
        }
        for train in self.__data["data"]:

            traindatetime = train["attributes"]["departure_time"]
            traintimestamp = time.mktime(datetime.datetime.strptime(traindatetime, "%Y-%m-%dT%H:%M:%S%z").timetuple())

            ret["trains"].append(int(traintimestamp - currentTime))

        ret["time"] = currentTime
        return ret
