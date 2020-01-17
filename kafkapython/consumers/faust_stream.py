"""Defines trends calculations for stations"""
import logging
from dataclasses import asdict, dataclass, field
import faust
import json 
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from environments import KAFKA_FAUST_URL,TRNAFORMED_STATION_TOPIC_NAME,KAFKA_CONNECTOR_TOPIC_NAME

logger = logging.getLogger(__name__)


# Faust will ingest records from Kafka in this format
class Station(faust.Record):
    stop_id: int
    direction_id: str
    stop_name: str
    station_name: str
    station_descriptive_name: str
    station_id: int
    order: int
    red: bool
    blue: bool
    green: bool


# Faust will produce records to Kafka in this format
class TransformedStation(faust.Record):
    station_id: int
    station_name: str
    order: int
    line: str


# TODO: Define a Faust Stream that ingests data from the Kafka Connect stations topic and
#   places it into a new topic with only the necessary information.
app = faust.App("stations-stream", broker=KAFKA_FAUST_URL, store="memory://")
# TODO: Define the input Kafka Topic. Hint: What topic did Kafka Connect output to?
topic = app.topic("producers.connector.stations", value_type=Station)
# TODO: Define the output Kafka Topic
out_topic = app.topic(TRNAFORMED_STATION_TOPIC_NAME, partitions=1)
# TODO: Define a Faust Table
table = app.Table(
   'station_summary',
   default=int,
   partitions=1,
   changelog_topic=out_topic,
)


#
#
# TODO: Using Faust, transform input `Station` records into `TransformedStation` records. Note that
# "line" is the color of the station. So if the `Station` record has the field `red` set to true,
# then you would set the `line` of the `TransformedStation` record to the string `"red"`
#
#

def transform_station_processor(station):
    line=""
    if station.red:
        line="red"
    elif station.blue:
        line="blue"
    elif station.green:
        line="green"
    ts = TransformedStation(
        station_id=station.station_id,
        station_name=station.station_name,
        order=station.order,
        line=line
    )
    return ts

@app.agent(topic)
async def stations_stream(stations):
    async for st in stations:
        line=""
        if st.red:
            line="red"
        elif st.blue:
            line="blue"
        elif st.green:
            line="green"
        ts = TransformedStation(
            station_id=st.station_id,
            station_name=st.station_name,
            order=st.order,
            line=line
        )


        await out_topic.send(key=ts.station_name,value=ts)

@app.agent(out_topic)
async def transform_stations(stations):
    async for st in stations:
        print(st)        


if __name__ == "__main__":
    app.main()
