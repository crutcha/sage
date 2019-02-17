from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from py2neo import Graph
from logging.config import dictConfig
import os
import sys

# Hacky, only way to make VS Code debugger work
sys.path.append('/home/drew/Documents/eidetic/')
import tasks
import time

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Logging setup
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG', # Some way to set this based on variable
        'handlers': ['wsgi']
    }
})

DATABASE_URL = os.environ.get("NEO4J_HOST", "bolt://localhost:7687")
DATABASE_USER = os.environ.get("NEO4J_USERNAME")
DATABASE_PASSWORD = os.environ.get("NEO4J_PASSWORD")

# Neo4J Setup
# TODO: this should be moved into views.py with other more specific URI stuff
graph_db = Graph(DATABASE_URL, auth=(DATABASE_USER, DATABASE_PASSWORD))

@app.route("/")
def device_list():
    devices = list(graph_db.nodes.match("Device"))
    return render_template("devices.html", devices=devices)


@app.route("/bootstraptest")
def bootstrap_test():
    return render_template("base.html")


@app.route("/trigger")
def trigger():
    # Synchronous for debugging
    result = tasks.gather_l3switch_data()
    return 'worked'

@app.route("/dumpdata")
def dump_data():
    # Synchronous for debugging
    result = tasks.dump_data()
    return 'yep'

@app.route("/clearstale")
def clear_stale():
    current_milli_time = int(round(time.time() * 1000))
    #stale_epoch = current_milli_time - 1800000
    stale_epoch = current_milli_time
    # DEBUG, let's do 1 hour?
    stale_query = (
        f"MATCH (i:Interface) WHERE i.updated_at < {stale_epoch}\n "
        f"DETACH DELETE i RETURN i"
    )
    result = list(graph_db.run(stale_query))
    return f"{len(result)} interfaces deleted"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
