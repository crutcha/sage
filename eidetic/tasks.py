from server import graph_db, app
from jnpr.junos import Device
from celery_app import celery
from lxml import etree
from utils import find_and_clean_element
from py2neo import Node, Relationship
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
    import provider
    for attr in dir(providers):
        cls = getattr(providers, attr)
        if inspect.isclass(cls):
            provider = cls()

            # All abstract base classes will have etl_run() method
            provider.etl_run()


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

                # There's no way for us to do a merge of BOTH the node and relationship at the
                # same time, it's just how cypher works. 'MERGE interface->belongs_to->device
                # will not return any matches if the interfaces actually does exist but the
                # device does not. We can either Check for existance of node and create it only
                # if it doesn't exist with the relationship we want already, we can keep a
                # property on the interface that contains the device name even though we'd have
                # a relationship to it eventually. Keeping the device as a property also means
                # we have multiple properties being checked to determine uniqueness/if it exists,
                # which py2neo merge operation can't handle, so we have to do this with raw
                # cypher call.
                phys_query = (
                    f"MATCH (d:Device) WHERE id(d) = {device[0].identity}\n"
                    f'MERGE (i:Interface {{name: "{name}", device: "{device[0]["name"]}", '
                    f'mac: "{mac_address}", mtu: "{mtu}", speed: "{speed}", type: '
                    f'"physical"}})\n'
                    f"MERGE (i)-[:BELONGS_TO]->(d)"
                    f"return i"
                )
                result = graph_db.run(phys_query)
                phys_intf_record = result.evaluate()

                logical_interfaces = intf.findall("logical-interface")
                for logical_intf in logical_interfaces:
                    logical_name = find_and_clean_element(logical_intf, "name")
                    addr_family = find_and_clean_element(
                        logical_intf, "address-family/address-family-name"
                    )
                    logical_mtu = find_and_clean_element(
                        logical_intf, "address-family/mtu"
                    )
                    address = find_and_clean_element(
                        logical_intf, "address-family/interface-address/ifa-local"
                    )
                    network = find_and_clean_element(
                        logical_intf,
                        "address-family/interface-address/ifa-destination",
                    )

                    logical_intf_query = (
                        f"MATCH (pi:Interface) WHERE id(pi) = {phys_intf_record.identity}\n"
                        f'MERGE (i:Interface {{name: "{logical_name}", device: "{device[0]["name"]}", '
                        f'mac: "{mac_address}", mtu: "{logical_mtu}", speed: "{speed}", type: '
                        f'"logical", addrress_family: "{addr_family}", address: "{address}", '
                        f'network: "{network}"}})\n'
                        f"MERGE (i)-[:SUB_INTERFACE]->(pi)"
                    )
                    graph_db.run(logical_intf_query)

                # Need to determine address-family as this will influence what data is sent
                # into graph DB

                # TODO: How do we handle relationship of vlan to interface? try that here or seperate
                # part of task where we need to query DB for device before creating relationship?

        except Exception as exc:
            app.logger.warning(exc)
