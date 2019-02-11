import sys
sys.path.append('..')

from abc import ABC, ABCMeta, abstractmethod
from typing import List
from .models import Interface

class L3Switch(metaclass=ABCMeta):

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

        import pdb; pdb.set_trace()
        intf_objects = self.gather_interfaces()