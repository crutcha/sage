from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from py2neo import Graph
import os
import sys

app = Flask(__name__)
bootstrap = Bootstrap(app)

DATABASE_URL = os.environ.get('NEO4J_HOST', 'bolt://localhost:7687')
DATABASE_USER = os.environ.get('NEO4J_USERNAME')
DATABASE_PASSWORD = os.environ.get('NEO4J_PASSWORD')

print(f"DATABASE_URL: {DATABASE_URL}")
graph = Graph(DATABASE_URL, auth=(DATABASE_USER, DATABASE_PASSWORD))

@app.route('/')
def device_list():
    devices = list(graph.nodes.match("Device"))
    return render_template('devices.html', devices=devices)

@app.route('/bootstraptest')
def bootstrap_test():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')