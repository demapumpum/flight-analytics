{{ config(materialized='table') }}

with hourly_flights as (
    select *
    from {{ ref('stg_hourly_flights') }}
), 

airports as (
    select * from {{ ref('airports') }}
),

airlines as (
    select * from {{ ref('airlines') }}
)
select
    hourly_flights.flight_id,
    hourly_flights.flight_number,
    hourly_flights.latitude,
    hourly_flights.longitude,
    hourly_flights.aircraft_code,
    hourly_flights.datetime,
    hourly_flights.origin_airport_iata,
    origin_airports.name as origin_airport,
    hourly_flights.destination_airport_iata,
    destination_airports.name as destination_airport,
    hourly_flights.airline_icao,
    airlines.Name as airline
    
from hourly_flights
left join airports as origin_airports
on hourly_flights.origin_airport_iata = origin_airports.iata
left join airports as destination_airports
on hourly_flights.destination_airport_iata = destination_airports.iata
left join airlines as airlines
on hourly_flights.airline_icao = airlines.ICAO