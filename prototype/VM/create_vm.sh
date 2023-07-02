#cp base_images/jammy-server-cloudimg-amd64.img jammy-server-cloudimg-amd64.img

cp base_images/jammy-server-cloudimg-amd64.img base_images/jammy.img

qemu-img create -b base_images/jammy.img -f qcow2 -F qcow2 mldepimg.img 20G

genisoimage -output cidata.iso -V cidata -r -J user-data meta-data

#virt-install --name=mldep_vm --ram=2048 --vcpus=1 --import --disk path=jammy-server-cloudimg-amd64.img --disk path=cidata.iso,device=cdrom --network bridge=virbr0,model=virtio --graphics none

virt-install --name=mldep_vm --ram=2048 --vcpus=1 --import --disk path=mldepimg.img,format=qcow2 --disk path=cidata.iso,device=cdrom --network bridge=virbr0,model=virtio --graphics none

virsh net-dhcp-leases default
