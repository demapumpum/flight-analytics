{{ config(materialized='table') }}

select 
    ICAO,
    Name,
    Code
from {{ ref('airlines_lookup') }}