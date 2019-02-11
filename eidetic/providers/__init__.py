"""
Dynamic import of all providers that implement any base abstract class.
"""

from pathlib import Path
import os
import sys
import inspect
import pkgutil
import importlib

base_classes = []
for (finder, name, ispkg) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    imported_module = importlib.import_module("." + name, package="providers")

    if name == "base":
        to_check = inspect.getmembers(imported_module)

        for member in to_check:
            if inspect.isabstract(member[1]):
                base_classes.append(member)
            else:
                del member

        del to_check

    else:
        mod_classes = inspect.getmembers(imported_module)

        for mem in mod_classes:
            # Can't combine these conditionals apparently...
            if inspect.isclass(mem[1]) and any(
                [issubclass(mem[1], c[1]) for c in base_classes]
            ):
                # issubclass with return true when called upon itself,
                # but we can compare this with base classes to make
                # sure we aren't exporting a concrete implementation
                if mem not in base_classes:
                    setattr(sys.modules[__name__], mem[0], mem[1])
            else:
                del mem
        del mod_classes

    del imported_module

# Export and cleanup
for c in base_classes:
    del c
del Path, os, sys, inspect, pkgutil, importlib, base_classes
