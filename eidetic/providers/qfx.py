from .base import L3Switch
from .models import Interface
from typing import List

class QFX(L3Switch):

    def gather_interfaces(self) -> List[Interface]:
        pass

