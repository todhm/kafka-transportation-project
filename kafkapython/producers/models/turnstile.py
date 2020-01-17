"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from models.producer import Producer
from models.turnstile_hardware import TurnstileHardware
from environments import NUM_REPLICAS_PER_TOPIC,NUM_PARTITIONS_PER_TOPIC,TURNSTILE_TOPIC_NAME


logger = logging.getLogger(__name__)


class Turnstile(Producer):
    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")

    #
    # TODO: Define this value schema in `schemas/turnstile_value.json, then uncomment the below
    #
    value_schema = avro.load(
       f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station):
        """Create the Turnstile"""
        station_name = (
            station.name.lower()
            .replace("/", "_and_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
        )

        #
        #
        # TODO: Complete the below by deciding on a topic name, number of partitions, and number of
        # replicas
        #
        #
        super().__init__(
            TURNSTILE_TOPIC_NAME, 
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema, 
            num_partitions=NUM_PARTITIONS_PER_TOPIC,
            num_replicas=NUM_REPLICAS_PER_TOPIC,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)
        timestamp = self.time_millis()
        try:
            self.producer.produce(
                topic=self.topic_name,
                key={"timestamp":timestamp },
                value_schema=self.value_schema,
                key_schema=self.key_schema,
                value={"station_id":self.station.station_id,"station_name":self.station.name,"line":self.station.color.name,"num_entries":num_entries},
            )
            logger.debug("Turnstile produce success")

        except Exception as e:
            logger.error(f"error produce turnstile data {self.station.station_id}"+str(e))
