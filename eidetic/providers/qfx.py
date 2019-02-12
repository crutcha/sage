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
        phys_interfaces = []
        logical_interfaces = []
        interface_info = self.connection.rpc.get_interface_information()
        logging.debug(etree.tostring(interface_info).decode().replace("\n", ""))

        interfaces = interface_info.findall("physical-interface")
        for intf in interfaces:
            # Common amongst all device types
            name = find_and_clean_element(intf, "name")
            mtu = find_and_clean_element(intf, "mtu")
            speed = find_and_clean_element(intf, "speed")
            mac_address = find_and_clean_element(intf, "hardware-physical-address")

            phys_intf = Interface(
                name = name,
                mtu = mtu,
                speed = speed,
                mac = mac_address,
                device = device.name,
                address_family = "",
                intf_type = "physical",
                address = "",
                network = ""
            )
            phys_interfaces.append(phys_intf)

            logical_intfs = intf.findall("logical-interface")
            for logical_intf in logical_intfs:
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
                    logical_intf, "address-family/interface-address/ifa-destination"
                )

                logical_intf_obj = Interface(
                    name = logical_name,
                    mtu = logical_mtu,
                    speed = speed,
                    mac = mac_address,
                    device = device.name,
                    address_family = addr_family,
                    intf_type = "logical",
                    address = address,
                    network = network
                )
                logical_interfaces.append(logical_intf_obj)
    
        return physical_interfaces + logical_interfaces