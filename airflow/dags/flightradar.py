from FlightRadar24 import FlightRadar24API
import pandas as pd
from dateutil import tz

class FlightRadar24Client:
    def __init__(self):
        self.client = FlightRadar24API()
    
    def getBounds(self, latitude: float, longitude: float, radius: float):
        bounds = self.client.get_bounds_by_point(latitude, longitude, radius)
        return bounds
    
    def getFlightsInArea(self, latitude: float, longitude: float, radius: float, output: str):
        flights_bounded = self.client.get_flights(bounds = self.getBounds(latitude, longitude, radius))
        flights_in_area = [f.__dict__ for f in flights_bounded]
        df_flights_in_area = pd.DataFrame.from_dict(flights_in_area)
        df_flights_in_area['time'] = pd.to_datetime(df_flights_in_area['time'], unit='s', utc=False).dt.tz_localize('UTC').dt.tz_convert('Asia/Manila').dt.tz_localize(None) 
        df_flights_in_area.to_csv(output, index=False)
    
    def getAirlines(self, output: str):
        airlines = [al for al in self.client.get_airlines()]
        df_airlines = pd.DataFrame.from_dict(airlines)
        df_airlines.to_csv(output, index=False)
    
    def getAirports(self, output: str):
        airports = [ap.__dict__ for ap in self.client.get_airports()]
        df_airports = pd.DataFrame.from_dict(airports)
        df_airports.to_csv(output, index=False)