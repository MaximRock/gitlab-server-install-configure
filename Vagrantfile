# -*- mode: ruby -*-
# vi: set ft=ruby :

    
PRIVATE_NETWORK_IP = "22.22.22.22"
NETWORK_BRIDGE = "re"
HOSTNAME = "re"

VB_MEMORY = 5
VB_CPUS = 2

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/jammy64"
    config.vm.box_check_update = false

    config.vm.define "node_1" do |node_1|
        node_1.vm.hostname = HOSTNAME
        node_1.vm.network "private_network", ip: PRIVATE_NETWORK_IP, bridge: NETWORK_BRIDGE, hostname: true
        node_1.vm.synced_folder "gitlab-srv-install", "/home/vagrant/srv/"
        node_1.vm.provider "virtualbox" do |vb|
            vb.gui = false
            vb.memory = VB_MEMORY
            vb.cpus = VB_CPUS
            vb.check_guest_additions = false
            vb.name = "gitlab"
        end
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "play.yml"
    end
end

# "38.0.0.15"
# enp7s0
# vagrant.max-rock.ru 6144 2
