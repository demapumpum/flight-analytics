{{ config(materialized='table') }}

with daily_flights as (
    select *
    from {{ ref('stg_daily_flights') }}
), 

airports as (
    select * from {{ ref('airports') }}
),

airlines as (
    select * from {{ ref('airlines') }}
)
select
    daily_flights.flight_id,
    daily_flights.flight_number,
    daily_flights.latitude,
    daily_flights.longitude,
    daily_flights.aircraft_code,
    daily_flights.datetime,
    daily_flights.origin_airport_iata,
    origin_airports.name as origin_airport,
    daily_flights.destination_airport_iata,
    destination_airports.name as destination_airport,
    daily_flights.airline_icao,
    airlines.Name as airline
    
from daily_flights
left join airports as origin_airports
on daily_flights.origin_airport_iata = origin_airports.iata
left join airports as destination_airports
on daily_flights.destination_airport_iata = destination_airports.iata
left join airlines as airlines
on daily_flights.airline_icao = airlines.ICAO