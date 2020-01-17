"""Configures a Kafka Connector for Postgres Station data"""
import json
import logging
import time 
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests


from environments import CONNECTOR_URL,POSTGRES_DB,POSTGRES_PASSWORD,\
    POSTGRES_PORT,POSTGRES_USER,POSTGRES_HOST,KAFKA_CONNECTOR_TOPIC_NAME

logger = logging.getLogger(__name__)


KAFKA_CONNECT_URL = CONNECTOR_URL

def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logging.debug("creating or updating kafka connect connector...")

    max_try = 10 
    current_try = 1
    while current_try<max_try:
        try:
            resp = requests.get(f"{KAFKA_CONNECT_URL}/connectors/{KAFKA_CONNECTOR_TOPIC_NAME}")
            logger.error(resp.status_code)
            if resp.status_code ==404:
                break 
        except Exception as e: 
            logger.error("Error occur while connecting to Kafka-connect"+str(e))
            logger.error("="*50)
            logger.error("Waiting for connections....")
            time.sleep(10)
        current_try += 1
        
    if resp.status_code == 200:
        logger.debug("connector already created skipping recreation")
        logger.debug(resp.text)
        return

    # TODO: Complete the Kafka Connect Config below.
    # Directions: Use the JDBC Source Connector to connect to Postgres. Load the `stations` table
    # using incrementing mode, with `stop_id` as the incrementing column name.
    # Make sure to think about what an appropriate topic prefix would be, and how frequently Kafka
    # Connect should run this connector (hint: not very often!)

    # TODO: Complete the Kafka Connect Config below.
    # Directions: Use the JDBC Source Connector to connect to Postgres. Load the `stations` table
    # using incrementing mode, with `stop_id` as the incrementing column name.
    # Make sure to think about what an appropriate topic prefix would be, and how frequently Kafka
    # Connect should run this connector (hint: not very often!)
    resp = requests.post(
       f"{KAFKA_CONNECT_URL}/connectors",
       headers={"Content-Type": "application/json"},
       data=json.dumps({
           "name": KAFKA_CONNECTOR_TOPIC_NAME,
           "config": {
               "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
               "key.converter": "org.apache.kafka.connect.json.JsonConverter",
               "key.converter.schemas.enable": "false",
               "value.converter": "org.apache.kafka.connect.json.JsonConverter",
               "value.converter.schemas.enable": "false",
               "batch.max.rows": "500",
               "connection.url": f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
               "connection.user": POSTGRES_USER,
               "connection.password":POSTGRES_PASSWORD,
               "table.whitelist": "cta.stations,stations",
               "mode": "incrementing",
               "incrementing.column.name": "stop_id",
               "topic.prefix": "producers.connector.",
               "poll.interval.ms": "10000",
           }
       }),
    )


    ## Ensure a healthy response was given
    resp.raise_for_status()
    logger.debug("connector created successfully")


if __name__ == "__main__":
    configure_connector()
