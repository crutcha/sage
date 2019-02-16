import sys
sys.path.append('..')

from abc import ABC, ABCMeta, abstractmethod
from typing import List
from server import graph_db
from .models import Interface, Device, Credential, L2ForwardingEntry

class L3Switch(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, device: Device, cred: Credential):
        """
        Device and Credential type will be provided for creating
        a connection handler.
        """
        pass

    @abstractmethod
    def gather_interfaces(self) -> List[Interface]:
        # Override this method and return list of eidetic.models.Interface
        # objects to be processed.
        pass
    
    @abstractmethod
    def gather_l2_forwarding_table(self) -> List[L2ForwardingEntry]:
        # Override this method and return list of eidetic.models.L2ForwardingTable
        # objects to be processed.
        pass

    def etl_run(self):
        """
        Run all methods to extract/transform/load data from device into
        Neo4j.
        """

        intf_objects = self.gather_interfaces()

        for intf in intf_objects:
            intf_query = (
                f'MATCH (d:Device) WHERE d.name = "{self.device.name}"\n'
                f'MERGE (i:Interface {{name: "{intf.name}", device: "{self.device.name}", '
                f'mac: "{intf.mac}", mtu: "{intf.mtu}", speed: "{intf.speed}", type: '
                f'"{intf.intf_type}"}})\n'
                f'MERGE (i)-[:COMPONENT_OF]->(d)'
            )
            print(intf_query)
            graph_db.run(intf_query)      
        
        forwarding_table = self.gather_l2_forwarding_table()