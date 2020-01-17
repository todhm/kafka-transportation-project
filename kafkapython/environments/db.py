import os 

POSTGRES_USER=os.environ.get('POSTGRES_USER',"cta_admin")
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD',"chicago")
POSTGRES_DB=os.environ.get('POSTGRES_DB',"cta")
POSTGRES_PORT=os.environ.get('POSTGRES_PORT',5432) 
POSTGRES_HOST=os.environ.get('POSTGRES_HOST','localhost')