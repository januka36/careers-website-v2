import sqlalchemy
#print(sqlalchemy.__version__)
from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_KEY']

engine = create_engine(db_connection_string, 
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from Jobs"))
    column_names = result.keys()
    jobs = []
    for row in result.all():
      result_dict = dict(zip(column_names, row))
      jobs.append(result_dict)
      
  return jobs

