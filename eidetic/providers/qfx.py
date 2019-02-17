from .base import L3Switch
from .models import Interface, Device, Credential, L2ForwardingEntry
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
        # Also stupid
        self.device = device
        self.connection.open()
        logging.debug(f"Connection opened: {device.name}")

    def gather_l2_forwarding_table(self) -> List[L2ForwardingEntry]:
        forwarding_table = self.connection.rpc.get_ethernet_switching_table_information()
        logging.debug(etree.tostring(forwarding_table).decode())

        if self.device.name == "leaf1":
            print('here')
            # TODO: do we need to grab VLANs first so we can match on them?
            # Probably.

        vlan_db = forwarding_table.findall("l2ng-l2ald-mac-entry-vlan")

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
            encapsulation = find_and_clean_element(intf, "encapsulation")
            if_index = find_and_clean_element(intf, "local-index")

            phys_intf = Interface(
                name = name,
                mtu = mtu,
                speed = speed,
                encapsulation = encapsulation,
                mac = mac_address,
                ifindex = int(if_index) if if_index else 0,
                # TODO: needing to access self here seems dumb. Maybe we should
                # have gather interfaces abstract take device name as argument?
                device = self.device.name,
                address_family = "",
                intf_type = "physical",
                address = "",
                network = ""
            )
            phys_interfaces.append(phys_intf)

            if 'vtep' in name:
                print('here')

            logical_intfs = intf.findall("logical-interface")
            for logical_intf in logical_intfs:
                logical_name = find_and_clean_element(logical_intf, "name")
                logical_encap = find_and_clean_element(logical_intf, "encapsulation")
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
                if_index = find_and_clean_element(logical_intf, "local-index")

                logical_intf_obj = Interface(
                    name = logical_name,
                    mtu = logical_mtu,
                    encapsulation = logical_encap,
                    speed = speed,
                    mac = mac_address,
                    ifindex = int(if_index) if if_index else 0,
                    # See above TODO
                    device = self.device.name,
                    address_family = addr_family,
                    intf_type = "logical",
                    address = address,
                    network = network
                )
                logical_interfaces.append(logical_intf_obj)
    
        return phys_interfaces + logical_interfaces