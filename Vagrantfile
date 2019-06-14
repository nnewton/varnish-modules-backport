Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"
  config.vm.provider "virtualbox" do |v|
    v.memory = 8048
    v.cpus = 4
  end
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
end
