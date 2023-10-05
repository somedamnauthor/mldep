#cp base_images/jammy-server-cloudimg-amd64.img jammy-server-cloudimg-amd64.img

#cp base_images/focal-server-cloudimg-amd64.img base_images/focal.img

cp /var/scratch/ssundar/focal-server-cloudimg-amd64.img /var/scratch/ssundar/focal.img

qemu-img create -b /var/scratch/ssundar/focal.img -f qcow2 -F qcow2 mldepimg.img 20G

genisoimage -output cidata.iso -V cidata -r -J user-data meta-data

#virt-install --name=mldep_vm --ram=2048 --vcpus=1 --import --disk path=jammy-server-cloudimg-amd64.img --disk path=cidata.iso,device=cdrom --network bridge=virbr0,model=virtio --graphics none

virt-install --name=mldep_vm --ram=2048 --vcpus=1 --import --disk path=mldepimg.img,format=qcow2 --disk path=cidata.iso,device=cdrom --network bridge=virbr0,model=virtio --graphics none --noautoconsole

virsh net-dhcp-leases default
