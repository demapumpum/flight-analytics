from FlightRadar24 import FlightRadar24API
import pandas as pd
from dateutil import tz
from utils import checkSchema, checkJSONSchema


class FlightRadar24Client:
    def __init__(self):
        self.client = FlightRadar24API()
    
    def getBounds(self, latitude: float, longitude: float, radius: float):
        """
        Get coordinate bounds of specified area given lat, long, and radius values
        """
        bounds = self.client.get_bounds_by_point(latitude, longitude, radius)
        return bounds
    

    def getFlightsInArea(self, latitude: float, longitude: float, radius: float, output: str):
        """
        Get flight data in bounded area and check if the schema matches reference schema
        """
        flights_bounded = self.client.get_flights(bounds = self.getBounds(latitude, longitude, radius))
        flights_in_area = [f.__dict__ for f in flights_bounded]
        checkJSONSchema(flights_in_area)

        df_flights_in_area = pd.DataFrame.from_dict(flights_in_area)
        # checkSchema(df_flights_in_area.dtypes.to_dict())

        df_flights_in_area['time'] = pd.to_datetime(df_flights_in_area['time'], unit='s', utc=False).dt.tz_localize('UTC').dt.tz_convert('Asia/Manila').dt.tz_localize(None) 
        df_flights_in_area.to_csv(output, index=False)
    

    def getAirlines(self, output: str):
        """
        Get the list of airlines
        """
        airlines = [al for al in self.client.get_airlines()]
        df_airlines = pd.DataFrame.from_dict(airlines)
        df_airlines.to_csv(output, index=False)
    

    def getAirports(self, output: str):
        """
        Get the list of airports
        """
        airports = [ap.__dict__ for ap in self.client.get_airports()]
        df_airports = pd.DataFrame.from_dict(airports)
        df_airports.to_csv(output, index=False)