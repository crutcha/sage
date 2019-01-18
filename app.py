from flask import Flask
from py2neo import Graph
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('NEO4J_HOST', 'bolt://localhost:7687')
DATABASE_USER = os.environ.get('NEO4J_USERNAME')
DATABASE_PASSWORD = os.environ.get('NEO4J_PASSWORD')

print(f"URL: {DATABASE_URL}")
print(f"USER: {DATABASE_USER}")
print(f"PASSWORD: {DATABASE_PASSWORD}")

graph = Graph(DATABASE_URL, auth=(DATABASE_USER, DATABASE_PASSWORD))

@app.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')