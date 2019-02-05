# Lab setup

For testing/labbing purposes, a simple spine/leaf topology with some servers and a virtual firewall is used. BGP EVPN will be used for MAC learning with an OSPF underlay and iBGP overlay. 

### Devices
* Spine/Leaf - Juniper vQFX. Requires both routing-engine VM and packet forwarding engine VM
* Servers - Ubuntu 16.04
* Firewall - Juniper vSRX

### Topology

![](https://github.com/crutcha/eidetic/tree/master/vagrant/eidetic-lab.png)


These devices were chosen because boxes are freely available for them in Vagrant's box directory. Vagrant is used to provision resources and then Ansible is used to bootstrap the devices with initial configuration. Since the provisioner used is Ansible, this can only be used on Linux or MacOS.

The vQFX RE/PFE combo can be resource intensive, and as the testing topology grows, resources will become a concern. Bare metal resources from packet.com can be used which is billed hourly at a very reasonable rate. A bash script(packet.sh) is also provided to setup a bare metal Ubuntu 16.04 from Packet and provision the environment all in one step.