"""Producer base-class providing common utilites and functionality"""
import logging
import os 
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer,CachedSchemaRegistryClient

from environments import KAFKA_URL,SCHEMA_REGISTRY_URL


logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        #
        #
        # TODO: Configure the broker properties below. Make sure to reference the project README
        # and use the Host URL for Kafka and Schema Registry!
        #
        #
        self.broker_properties = {
            'cleanup.policy':"delete",
            'delete.retention.ms':5400000,
            "file.delete.delay.ms":5400000,
        }
        self.client = AdminClient({"bootstrap.servers": KAFKA_URL})
        topic_metadata = self.client.list_topics(timeout=5)
        for topic in topic_metadata.topics.keys():
            Producer.existing_topics.add(topic)

        


        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        # TODO: Configure the AvroProducer
        schema_client = CachedSchemaRegistryClient(SCHEMA_REGISTRY_URL)
        self.producer = AvroProducer(
               {"bootstrap.servers": KAFKA_URL},
                schema_registry=schema_client
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""
        #
        #
        # TODO: Write code that creates the topic for this producer if it does not already exist on
        # the Kafka Broker.
        #
        #
        futures = self.client.create_topics(
            [
                NewTopic(
                    topic=self.topic_name, 
                    num_partitions=self.num_partitions, 
                    replication_factor=self.num_replicas, 
                    config=self.broker_properties
                )
            ]
        )

        for topic, future in futures.items():
            try:
                future.result()
                logger.info("topic created")
            except Exception as e:
                logger.error(f"failed to create topic {self.topic_name}: {str(e)}")
                raise ValueError


    def close(self):
        self.producer.flush()
        """Prepares the producer for exit by cleaning up the producer"""
        #
        #
        # TODO: Write cleanup code for the Producer here
        #
        #

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
