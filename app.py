from flask import Flask, render_template, jsonify, request
from database import engine
from database import load_jobs_from_db, load_job_from_db, add_application_to_db


app = Flask(__name__)

# JOBS = [{
#     'id': 1,
#     'title': 'Data Analyst',
#     'location': 'Mumbai, India',
#     'salary': 'Rs. 10,00,000'
# }, {
#     'id': 2,
#     'title': 'Front-End Engineer',
#     'location': 'Remote',
#     'salary': 'Rs. 12,00,000'
# }, {
#     'id': 3,
#     'title': 'Back-End Engineer',
#     'location': 'San Francisco, USA',
#     'salary': '$12000'
# }]

@app.route("/")
def hello_world():
  return render_template('home.html', jobs=load_jobs_from_db())


@app.route("/api/jobs")
def list_jobs():
  return jsonify(load_jobs_from_db())

#Dynamic route
@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job)

@app.route("/job/<id>/apply", methods=["post"])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html', application=data, job=job)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
