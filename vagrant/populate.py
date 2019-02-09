# Simple script to populate device nodes in neo4j depending on currently deployed
# packet.com public IP
from py2neo import Graph
import os

# this is redundant but importing it from app.py causes a circular import
DATABASE_URL = os.environ.get("NEO4J_HOST", "bolt://localhost:7687")
DATABASE_USER = os.environ.get("NEO4J_USERNAME")
DATABASE_PASSWORD = os.environ.get("NEO4J_PASSWORD")
graph_db = Graph(DATABASE_URL, auth=(DATABASE_USER, DATABASE_PASSWORD))

# Grab user/password from environmental variables else try some defaults
DEVICE_USER = os.environ.get("DEVICE_USER")
DEVICE_PASSWORD = os.environ.get("DEVICE_PASSWORD")

# Could probably just do this from vagrantfile but whatever...
DEVICE_TUPLES = [
    ("spine1", "L3Switch", 5001),
    ("spine2", "L3Switch", 5002),
    ("leaf1", "L3Switch", 5003),
    ("leaf2", "L3Switch", 5004),
    ("leaf3", "L3Switch", 5005),
    ("vsrx1", "Firewall", 5009),
]

public_ip = input("Enter Public IP: ")

base_insert = f'CREATE (cred:Crendtial {username:"{DEVICE_USER}", password:"{DEVICE_PASSWORD}"})\n'
for index, value in enumerate(DEVICE_TUPLES):
    base_insert += f'CREATE (d{index}:Device {{name: "{value[0]}", ip: "{public_ip}", port:{value[2]}, type: "{value[1]}"}})\n'
    base_insert += f"CREATE (d{index})-[:USES_CRED]->(cred)\n"

graph_db.run(base_insert)
