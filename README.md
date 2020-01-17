# Kafka Public Transportation Project. 


---
In this project I developed whole kafka pipeline application consists of simple kafka producer,kafka-connect & kafka-rest-proxy in producer side and ksql,kafka-faust & simple kafka consumer on consumer side. 


This application works with following flow. 

* Simulate transportation from excel file and send its to kafka through kafka producers. 
* Send data to kafka broker from postgresql DB through kafka connect. 
* Simulate weather data from excel file and send data to kafka broker through kafka rest proxy. 
* Transform turnstile data produced from first step and calculate total num entries data from ksql. 
* Transform data produced from postgresql database inside faust stream application and saved it in newly created topic. 



Execution.
---
* This app developed within docker environments you can test and run kafka files from docker environments or virtual environments in your setups. 

* This app can be run through following steps. 
    * (1) execute Kafka Producer, rest-proxy call and kafka-connect script with `docker-compose exec kafkapython python producers/simulation.py`
    * (2) execute KSQL query with `docker-compose exec kafkapython python consumers/ksql.py`
    * (3) execute kafka faust stream app with `docker-compose exec kafkapython python consumers/faust_stream.py worker`
	* (4) execute kafka consumer with `docker-compose exec kafkapython python consumers/server.py`
		- warning: It is hard to access through browser to consumer server in this step so I would recommend run this file with simple python command with required packages installed in requirements.txt file. 
	* You can Also Run this process outside docker if you installed packages in kafkapython/consumers/requirements and kafkapython/producers/requirements.txt
