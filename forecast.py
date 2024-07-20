import urllib.request
import urllib.error
import json


class WebAPI():
    def __init__(self):
        self.apikey = None
    
    def set_apikey(self, apikey):
        self.apikey = apikey

    def download_url(self, url):      
        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)
            
            if response is not None:
                response.close()
            
            return r_obj
        
        except urllib.error.HTTPError as e:
            error_code = format(e.code)
            
            if error_code == "404":
                print("Error 404: Page not found")
            
            elif error_code == "503":
                print("Error 503: Server unavailable")
            
            else:
                print(f"Unexpected error occurred: Error {error_code}")
        
        except urllib.error.HTTPError:
            print("You are offline, or the specified server does not exist")



class WeatherAPI(WebAPI):   
    def __init__(self, zipcode, country):
        super().__init__()
        self.zipcode = zipcode
        self.country = country
        self.url = None
        self.city = None
        self.description = None
        self.temp = None
        self.feels_like = None
        self.temp_min = None
        self.temp_max = None
        self.humidity = None

    def load_data(self):
        apikey = str(input("What is your API key?"))
        self.set_apikey(apikey)
        self.url = (f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.country}&appid={self.apikey}")
        r_obj = self.download_url(self.url)
        self.description = r_obj["weather"][0]["description"]
        self.city = r_obj["name"]
        self.temp = r_obj["main"]["temp"]
        self.feels_like = r_obj["main"]["feels_like"]
        self.temp_min = r_obj["main"]["temp_min"]
        self.temp_max = r_obj["main"]["temp_max"]
        self.humidity = r_obj["main"]["humidity"]
        
        return self.description, self.city, self.temp, self.feels_like, self.temp_min, self.temp_max, self.humidity

zipcode = int(input("What is the zipcode?"))
country = str(input("What is the country abbreviation in two letters?"))
weather = WeatherAPI(zipcode, country)
description, city, temp, feels_like, temp_min, temp_max, humidity  = weather.load_data()

print(f"The weather description in {weather.city} is {weather.description}.\nThe temperature is {int(weather.temp * 1.8 - 459.67)} °F, feels like {int(weather.feels_like * 1.8 - 459.67)} °F, with an expected minimum of {int(weather.temp_min * 1.8 - 459.67)} °F, and an expected maximum of {int(weather.temp_max * 1.8 - 459.67)} °F.\nHumidity is at {weather.humidity}%.")
