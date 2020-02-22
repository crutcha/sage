#!/bin/bash

# Helper script to deploy a test environment onto packet.com bare metal server running
# Ubuntu 16.04.

# Fail fast
set -e

# Grab and install everything we need
cd /tmp
wget https://releases.hashicorp.com/vagrant/2.2.3/vagrant_2.2.3_x86_64.deb
wget -q -O - http://download.virtualbox.org/virtualbox/debian/oracle_vbox_2016.asc | apt-key add -
wget https://download.virtualbox.org/virtualbox/5.2.36/virtualbox-5.2_5.2.36-135684~Ubuntu~xenial_amd64.deb
echo "deb http://download.virtualbox.org/virtualbox/debian xenial contrib" >> /etc/apt/sources.list.d/virtualbox.org.list
apt-get update
apt install -y gcc linux-headers-4.4.0-134-generic python-pip vim tmux
dpkg -i vagrant_2.2.3_x86_64.deb
apt install ./virtualbox-5.2_5.2.36-135684~Ubuntu~xenial_amd64.deb

# dotfile setup stuff
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
git clone https://github.com/crutcha/dotfiles.git
cp dotfiles/.bashrc ~/
cp dotfiles/.tmux.conf ~/
cp dotfiles/.vimrc ~/

# Verify virtualbox setup
echo "CHECKING VIRTUALBOX INSTALL..."
VBOX_STATUS=$(vboxmanage --version)
VBOX_EXIT_CODE=$(echo $?)
if [ $VBOX_EXIT_CODE -ne 0 ]; then
    echo $VBOX_STATUS
    echo "VIRTUALBOX SETUP FAILED"
    exit $VBOX_EDIT_CDE
fi

# Install all the ansible things
echo "SETTING UP ANSIBLE..."
cd ~/eidetic
pip install ansible==2.7.15
pip install junos-eznc jxmlease
ansible-galaxy install Juniper.junos,2.1.0


# Add boxes ahead of time
echo "INSTALLING VAGRANT BOXES..."
vagrant plugin install vagrant-host-shell
vagrant plugin install vagrant-junos
vagrant box add "juniper/vqfx10k-re"
vagrant box add "juniper/vqfx10k-pfe"
vagrant box add "ubuntu/xenial64"
vagrant box add juniper/ffp-12.1X47-D15.4 --provider virtualbox

# Turn up test environment
echo "SPINNING UP TEST LAB..."
make up
