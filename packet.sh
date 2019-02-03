#!/bin/bash

# Helper script to deploy a test environment onto packet.com bare metal server running
# Ubuntu 16.04.

# Fail fast
set -e

# Grab and install everything we need
cd /tmp
apt-add-repository ppa:ansible/ansible -y
wget https://releases.hashicorp.com/vagrant/2.2.3/vagrant_2.2.3_x86_64.deb
wget -q -O - http://download.virtualbox.org/virtualbox/debian/oracle_vbox_2016.asc | apt-key add -
echo "deb http://download.virtualbox.org/virtualbox/debian xenial contrib" >> /etc/apt/sources.list.d/virtualbox.org.list
apt-get update
apt install -y gcc linux-headers-4.4.0-134-generic ansible python-pip virtualbox-5.2 vim tmux
dpkg -i vagrant_2.2.3_x86_64.deb

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
pip install junos-eznc jxmlease
ansible-galaxy install Juniper.junos


# Add boxes ahead of time
echo "INSTALLING VAGRANT BOXES..."
vagrant box add "juniper/vqfx10k-re"
vagrant box add "juniper/vqfx10k-pfe"
vagrant box add "ubuntu/xenial64"
vagrant box add juniper/ffp-12.1X47-D15.4 --provider virtualbox

# Turn up test environment
echo "SPINNING UP TEST LAB..."
make up
