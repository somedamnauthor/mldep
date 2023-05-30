genisoimage -output cidata.iso -V cidata -r -J user-data meta-data

virt-install --name=mldep_vm --ram=2048 --vcpus=1 --import --disk path=focal-server-cloudimg-amd64.img --disk path=cidata.iso,device=cdrom --os-variant=ubuntu20.04 --network bridge=virbr0,model=virtio --graphics none

virsh net-dhcp-leases default
