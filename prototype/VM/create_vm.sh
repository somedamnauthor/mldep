#cp base_images/jammy-server-cloudimg-amd64.img jammy-server-cloudimg-amd64.img

cp base_images/focal-server-cloudimg-amd64.img base_images/focal.img

qemu-img create -b base_images/focal.img -f qcow2 -F qcow2 mldepimg${1}.img 20G

genisoimage -output cidata${1}.iso -V cidata -r -J user-data meta-data

virt-install --name=mldep_vm${1} --ram=2048 --vcpus=1 --import --disk path=mldepimg${1}.img,format=qcow2 --disk path=cidata${1}.iso,device=cdrom --network bridge=virbr0,model=virtio --graphics none --noautoconsole

virsh net-dhcp-leases default
