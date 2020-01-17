"""Contains functionality related to Weather"""
import logging
import json 

logger = logging.getLogger(__name__)


class Weather:
    """Defines the Weather model"""

    def __init__(self):
        """Creates the weather model"""
        self.temperature = 70.0
        self.status = "sunny"

    def process_message(self, message):

        try:
            message_value = message.value()
            self.temperature = message_value.get("temperature")
            self.status = message_value.get("status")
    
        except KeyError as e:
            logger.fatal(f"Failed to unpack message {e}")

        #
        #
        # TODO: Process incoming weather messages. Set the temperature and status.
        #
        #
