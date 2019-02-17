from server import graph_db, app
from jnpr.junos import Device
from celery_app import celery
from lxml import etree
from utils import find_and_clean_element
from py2neo import Node, Relationship
from providers.models import Device, Credential
from celery import group
import inspect


@celery.task(bind=True)
def dump_data(self):

    # Determine what providers are available to us at runtime, gives a bit more
    # flexibility. At least for now. Allows for addition of providers without
    # restarting of app, but also means we lose ability to create relationship
    # of provider to device and instead rely on a string property on the
    # device node.
    # TODO: verify this actually works. importing a previously imported module
    # will used cached objects but if there are new classes being exported from
    # __init__ they SHOULD be caught on the next import???
    import providers

    for attr in dir(providers):
        cls = getattr(providers, attr)
        if inspect.isclass(cls):
            # query DB for all devices of this type and create group to process
            # them.
            devices = graph_db.run(
                f"match (dev:Device)-[:USES_CRED]->(cred:Credential) where "
                f'dev.type = "{attr}" return dev,cred'
            )
            for device in devices:
                name = device.data()["dev"]["name"]
                ip = device.data()["dev"]["ip"]
                port = device.data()["dev"]["port"]
                user = device.data()["cred"]["username"]
                # TODO: proper encryption mechanism for this
                password = device.data()["cred"]["password"]

                device_obj = Device(name=name, ip=ip, port=port, device_type=attr)
                cred_obj = Credential(username=user, password=password)
                provider = cls(device_obj, cred_obj)

                # All abstract base classes will have etl_run() method
                provider.etl_run()
