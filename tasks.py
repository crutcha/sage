from server import graph_db, app
from jnpr.junos import Device
from celery_app import celery
from lxml import etree
from utils import find_and_clean_element
from py2neo import Node


@celery.task(bind=True)
def celery_test2(self):
    print("YADA YADA YADA")
    print(f"Received task from 2!: {self}")


# The tasks to gather data depending on provider will eventually be inherited abstract base
# classes to ensure each provider does what we need it to, and will make this task
# far simpler, but for now we need to do things this way to first understand all the data
# we would need each provider to actually provide.
@celery.task(bind=True)
def gather_l3switch_data(self):
    print("here")
    devices = graph_db.run(
        'match (dev:Device)-[:USES_CRED]->(cred:Credential) where dev.type = "L3Switch" return dev,cred'
    )
    for device in devices:
        host = device.data()["dev"]["ip"]
        port = device.data()["dev"]["port"]
        user = device.data()["cred"]["username"]
        password = device.data()["cred"]["password"]
        dev = Device(host=host, user=user, password=password, port=port)

        try:
            dev.open()

            # Gather interface details
            interface_info = dev.rpc.get_interface_information()
            app.logger.debug(etree.tostring(interface_info).decode().replace("\n", ""))

            interfaces = interface_info.findall("physical-interface")
            for intf in interfaces:
                # Common amongst all device types
                name = find_and_clean_element(intf, "name")
                mtu = find_and_clean_element(intf, "mtu")
                speed = find_and_clean_element(intf, "speed")
                mac_address = find_and_clean_element(intf, "hardware-physical-address")

                phys_intf_def = {
                    "name": name,
                    "mtu": mtu,
                    "speed": speed,
                    "type": "physical",
                    "mac": mac_address,
                }
                phys_node = Node("Interface", **phys_intf_def)
                graph_db.create(phys_node)

                logical_interfaces = intf.findall("logical-interface")
                for logical_intf in logical_interfaces:
                    name = find_and_clean_element(logical_intf, "name")
                    addr_family = find_and_clean_element(
                        logical_intf, "address-family/address-family-name"
                    )
                    logical_mtu = find_and_clean_element(
                        logical_intf, "address-family/mtu"
                    )

                    if addr_family == "inet":
                        pass
                    elif addr_family == "eth-switch":
                        pass

                # Need to determine address-family as this will influence what data is sent
                # into graph DB

                # TODO: How do we handle relationship of vlan to interface? try that here or seperate
                # part of task where we need to query DB for device before creating relationship?

        except Exception as exc:
            app.logger.warning(exc)
