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

        #TODO: should we use label vs property for interfaces for faster query?
        # or would indexing suffice?
        for intf in intf_objects:
            # Merge only on interface and device, the rest of the properties
            # will be updated on every ETL run
            intf_query = (
                f'MATCH (d:Device) WHERE d.name = "{self.device.name}"\n'
                f'MERGE (i:Interface {{name: "{intf.name}", device: "{self.device.name}"}}) '
                f'SET i.mac = "{intf.mac}", i.mtu = "{intf.mtu}", i.speed = "{intf.speed}", '
                f' i.type = "{intf.intf_type}" , i.encapsulation = "{intf.encapsulation}", '
                f'i.ifindex = {intf.ifindex}, i.updated_at = timestamp()\n'
                f'MERGE (i)-[:COMPONENT_OF]->(d)'
            )
            print(intf_query)
            graph_db.run(intf_query)      
        
        forwarding_table = self.gather_l2_forwarding_table()