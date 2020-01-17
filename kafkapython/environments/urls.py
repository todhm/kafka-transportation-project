import os 

KAFKA_URL=os.environ.get('BROKER_URL',"PLAINTEXT://localhost:9092")
KAFKA_FAUST_URL=os.environ.get("KAFKA_FAUST_URL",'kafka://localhost:9092')
SCHEMA_REGISTRY_URL=os.environ.get('SCHEMA_REGISTRY_URL',"http://localhost:8081")
REST_PROXY_URL=os.environ.get('REST_PROXY_URL',"http://localhost:8082")
CONNECTOR_URL=os.environ.get("CONNECTOR_URL","http://localhost:8083")
KSQL_URL=os.environ.get("KSQL_URL",'http://localhost:8088')