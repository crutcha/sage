from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from py2neo import Graph
from celery import Celery
import tasks
import os
import sys

app = Flask(__name__)
bootstrap = Bootstrap(app)

DATABASE_URL = os.environ.get("NEO4J_HOST", "bolt://localhost:7687")
DATABASE_USER = os.environ.get("NEO4J_USERNAME")
DATABASE_PASSWORD = os.environ.get("NEO4J_PASSWORD")
MQ_HOST = os.environ.get("MQ_HOST")
CELERY_USERNAME = os.environ.get("CELERY_USERNAME")
CELERY_PASSWORD = os.environ.get("CELERY_PASSWORD")

# Neo4J Setup
# TODO: this should be moved into views.py with other more specific URI stuff
# whenever we get to that
graph = Graph(DATABASE_URL, auth=(DATABASE_USER, DATABASE_PASSWORD))

def make_celery(app):
    # create context tasks in celery
    app.config[
        "CELERY_BROKER_URL"
    ] = f"amqp://{CELERY_USERNAME}:{CELERY_PASSWORD}@{MQ_HOST}"
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

@app.route("/")
def device_list():
    devices = list(graph.nodes.match("Device"))
    return render_template("devices.html", devices=devices)


@app.route("/bootstraptest")
def bootstrap_test():
    return render_template("base.html")


@app.route("/trigger")
def trigger():
    result = tasks.celery_test2.delay()
    return str(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
