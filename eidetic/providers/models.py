"""
Python doesn't really have a similar construct to something like a struct in Go/C, so instead
these dataclasses will be used as pseudo structs to create common objects where we know 
upon instantiation they have the attributes we want and can reasonably assume since it's
type hinted that it's also the type we want. Provider interfaces implemented with abstract
base classes will pass around these objects.
"""

from dataclasses import dataclass

# TODO: maybe better to implement our own type system so we can verify things like
# port number does not exceed 65535 etc...

@dataclass
class Device:
    name: str
    ip: str
    port: int
    device_type: str


@dataclass
class Credential:
    username: str
    password: str

@dataclass
class Interface:
    name: str
    mtu: int
    speed: str
    mac: str
    device: str
    address_family: str
    intf_type: str
    address: str = ""
    network: str = ""

@dataclass
class L2ForwardingEntry:
    vlan: int