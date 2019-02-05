# Lab setup

For testing/labbing purposes, a simple spine/leaf topology with some servers and a virtual firewall is used. BGP EVPN will be used for MAC learning with an OSPF underlay and iBGP overlay. 

### Devices
* Spine/Leaf - Juniper vQFX. Requires both routing-engine VM and packet forwarding engine VM
* Servers - Ubuntu 16.04
* Firewall - Juniper vSRX

### Topology

![](https://raw.githubusercontent.com/crutcha/eidetic/master/vagrant/eidetic-lab.png)


These devices were chosen because boxes are freely available for them in Vagrant's box directory. Vagrant is used to provision resources and then Ansible is used to bootstrap the devices with initial configuration. Since the provisioner used is Ansible, this can only be used on Linux or MacOS.

The vQFX RE/PFE combo can be resource intensive, and as the testing topology grows, resources will become a concern. Bare metal resources from packet.com can be used which is billed hourly at a very reasonable rate. A bash script(packet.sh) is also provided to setup a bare metal Ubuntu 16.04 from Packet and provision the environment all in one step.

### SSH

Once the topology is spun up, you can access the VMs either via vagrant IE: `vagrant ssh {{box_name}}` or externally via the bare metal servers public IP since port-forwarding is configured. NetConf can also use the same forwarded port.

* spine1 - 5001
* spine2 - 5002
* leaf1  - 5003
* leaf2  - 5004
* leaf3  - 5005
* srv1   - 5006
* srv2   - 5007
* srv3   - 5008
* vsrx1  - 5009