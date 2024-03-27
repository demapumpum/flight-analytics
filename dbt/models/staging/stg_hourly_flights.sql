{{ config(materialized='view') }}

with hourly_flights as (
    select 
        *,
        row_number() over(partition by id) as rn
    from {{ source('staging', 'external_table_hourly_flights') }}
    where id is not null
)
select
-- flight details
    id as flight_id,
    number as flight_number,
    latitude as latitude,
    longitude as longitude,
    aircraft_code as aircraft_code,
    time as datetime,

-- airport details
    origin_airport_iata as origin_airport_iata,
    destination_airport_iata as destination_airport_iata,

-- airline details
    airline_iata as airline_iata,
    airline_icao as airline_icao

from hourly_flights
where rn = 1