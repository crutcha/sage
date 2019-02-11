"""
Dynamic import of all providers that implement any base abstract class.
"""

from pathlib import Path
import os
import sys
import inspect
import pkgutil
import importlib

#import pdb; pdb.set_trace()

base_module = None
base_classes = []
concrete_classes = []
for (finder, name, ispkg) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    imported_module = importlib.import_module("." + name, package="providers")

    if name == 'base':
        to_check = inspect.getmembers(imported_module)

        for member in to_check:
            if inspect.isabstract(member[1]):
                base_classes.append(member)
            else:
                del member
        
    else:
        mod_classes = inspect.getmembers(imported_module)

        for member in mod_classes:
            if member[0] == "QFX":
                import pdb; pdb.set_trace()

import pdb; pdb.set_trace()