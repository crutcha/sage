import sys
sys.path.append('..')

from abc import ABC, ABCMeta, abstractmethod
from typing import List
from .models import Interface, Device, Credential

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
    
    def etl_run(self):
        """
        Run all methods to extract/transform/load data from device into
        Neo4j.
        """

        intf_objects = self.gather_interfaces()