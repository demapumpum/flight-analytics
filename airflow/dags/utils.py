import os
import json
from jsonschema import validate
from airflow.exceptions import AirflowFailException

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
schema_file = AIRFLOW_HOME + '/scripts/schema.json'
    
def load_json(filepath):
    """
    load reference json schema
    """
    with open(filepath, 'r') as f:
        ref_schema = json.load(f)
    
    return ref_schema


def checkSchema(schema):
    """
    Check if schema of ingested data matches reference schema 
    """
    ref_schema = load_json(schema_file)

    if schema != ref_schema:
        raise AirflowFailException("Schema change detected!")


def checkJSONSchema(jsonResponse):
    """
    Validate API JSON schemaa ingested 
    """
    schema = {
        "type": 'array',
        "items": {
            "type": 'object',
            "properties": {
                "latitude": {type: 'number'},
                "longitude": {type: 'number'},
                "id": {type: 'string'},
                "icao_24bit": {type: 'string'},
                "heading": {type: 'integer'},
                "altitude": {
                    "type": 'integer',
                    "minimum": 0
                    },
                "ground_speed": {
                    "type": 'integer',
                    "minimum": 0
                    },
                "squawk": {type: 'string'},
                "aircraft_code": {type: 'string'},
                "registration": {type: 'string'},
                "time": {type: 'integer'},
                "origin_airport_iata": {type: ['string', 'null']},
                "destination_airport_iata": {type: ['string', 'null']},
                "number": {type: 'string'},
                "airline_iata": {type: 'string'},
                "on_ground": {
                    "type": 'integer',
                    "minimum": 0
                    },
                "vertical_speed": {type: 'integer'},
                "callsign": {type: 'string'},
                "airline_icao": {type: 'string'}
                },
            "required": ['latitude', 'longitude', 'id', 'icao_24bit', 'heading', 'altitude', 'ground_speed', 'squawk', 'aircraft_code',
                   'registration', 'time', 'origin_airport_iata', 'destination_airport_iata', 'number', 'airline_iata',
                   'on_ground', 'vertical_speed', 'callsign', 'airline_icao']
            }
        }
    
    validate(instance=jsonResponse, schema=schema)

