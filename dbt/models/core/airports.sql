{{ config(materialized='table') }}

select 
    iata,
    name,
    country
from {{ ref('airports_lookup') }}