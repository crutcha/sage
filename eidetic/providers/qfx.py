from .base import L3Switch
from .models import Interface, Device, Credential
from typing import List
from jnpr.junos import Device as JunosDevice
from lxml import etree
from utils import find_and_clean_element
import logging

class QFX(L3Switch):

    def __init__(self, device: Device, cred: Credential) -> None:
        self.connection = JunosDevice(
            host=device.ip,
            port=device.port,
            user=cred.username,
            password=cred.password
        )
        self.connection.open()
        logging.debug(f"Connection opened: {device.name}")

    def gather_interfaces(self) -> List[Interface]:


        interface_info = self.connection.rpc.get_interface_information()
        logging.debug(etree.tostring(interface_info).decode().replace("\n", ""))

        interfaces = interface_info.findall("physical-interface")
        for intf in interfaces:
            # Common amongst all device types
            name = find_and_clean_element(intf, "name")
            mtu = find_and_clean_element(intf, "mtu")
            speed = find_and_clean_element(intf, "speed")
            mac_address = find_and_clean_element(intf, "hardware-physical-address")