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

def load_job_from_db(id):
  with engine.connect() as conn:
    query = "select * from Jobs WHERE Id = :val" 
    result = conn.execute(text(query), parameters=dict(val=id))
    rows = result.all()
    column_names = result.keys()
    if len(rows) == 0:
      return None
    else:
      return dict(zip(column_names, rows[0]))
    
# with engine.connect() as conn:
#     result = conn.execute(text("select * from Jobs WHERE Id = :val"),val=0)
#     rows = result.all()
#     column_names = result.keys()
#     if len(rows) == 0:
#       print("None")
#     else:
#       print(dict(zip(column_names, rows[val])))

def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

    conn.execute(query, 
      parameters=dict(job_id = job_id,
      full_name=data["full_name"],
      email=data["email"],
      linkedin_url=data["linkedin_url"],
      education=data["education"],
      work_experience=data["work_experience"],
      resume_url=data["resume_url"]
      ))
