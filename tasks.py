from app import celery, graph_db
from jnpr.junos import Device

@celery.task(bind=True)
def celery_test2(self):
    print("YADA YADA YADA")
    print(f"Received task from 2!: {self}")

@celery.task(bind=True)
def gather_device_data(self):
    devices = graph_db.run("match (dev:Device)-[:USES_CRED]->(cred:Crendtial) return dev,cred")
    for device in devices:
        host = device.data()['dev']['ip']
        port = device.data()['dev']['port']
        user = device.data()['cred']['username']
        password = device.data()['cred']['password']
        dev = Device(host=host, user=user, password=password, port=port)
        dev.open()
        print(dev.facts)