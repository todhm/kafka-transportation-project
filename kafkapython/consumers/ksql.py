"""Configures KSQL to combine station and turnstile data"""
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import json
import logging

import requests

import topic_check
from environments import KSQL_URL,TURNSTILE_TOPIC_NAME

logger = logging.getLogger(__name__)



#
# TODO: Complete the following KSQL statements.
# TODO: For the first statement, create a `turnstile` table from your turnstile topic.
#       Make sure to use 'avro' datatype!
# TODO: For the second statment, create a `turnstile_summary` table by selecting from the
#       `turnstile` table and grouping on station_id.
#       Make sure to cast the COUNT of station id to `count`
#       Make sure to set the value format to JSON


KSQL_STATEMENT = f"""
CREATE TABLE turnstile (
    station_id INTEGER, 
    station_name VARCHAR, 
    line VARCHAR,
    num_entries INTEGER) WITH (
    KAFKA_TOPIC='{TURNSTILE_TOPIC_NAME}',
    VALUE_FORMAT='AVRO',
    KEY='station_id'
);
CREATE TABLE turnstile_summary
WITH ( 
    VALUE_FORMAT='JSON'
)
 AS SELECT SUM(num_entries) as COUNT,station_id
 FROM turnstile
 GROUP BY station_id;

"""


def execute_statement():
    """Executes the KSQL statement against the KSQL API"""
    if topic_check.topic_exists("TURNSTILE_SUMMARY") is True:
        return

    logging.debug("executing ksql statement...")

    resp = requests.post(
        f"{KSQL_URL}/ksql",
        headers={"Content-Type": "application/vnd.ksql.v1+json"},
        data=json.dumps(
            {
                "ksql": KSQL_STATEMENT,
                "streamsProperties": {"ksql.streams.auto.offset.reset": "earliest"},
            }
        ),
    )

    # Ensure that a 2XX status code was returned
    resp.raise_for_status()


if __name__ == "__main__":
    execute_statement()
