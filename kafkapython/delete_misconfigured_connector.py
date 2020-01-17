import requests
from environments import CONNECTOR_URL 


if __name__=="__main__":
    resp = requests.delete(f"{CONNECTOR_URL}/connectors/stations")
    print(resp.text)