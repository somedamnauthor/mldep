# {1} - instances
# {2} - root access for libvirt
# {3} - cloud image dir

if [ ${2} = "true" ]; then
    qemu_args=""
    qemu_dir=${3}
else
    qemu_args="--connect qemu:///system"
    qemu_dir="/tmp"
fi

cp ${3}/focal-server-cloudimg-amd64.img $qemu_dir/focal.img

qemu-img create -b $qemu_dir/focal.img -f qcow2 -F qcow2 $qemu_dir/mldepimg${1}.img 20G

genisoimage -output $qemu_dir/cidata${1}.iso -V cidata -r -J user-data meta-data

virt-install $qemu_args --name=mldep_vm${1} --ram=2048 --vcpus=1 --import --disk path=$qemu_dir/mldepimg${1}.img,format=qcow2 --disk path=$qemu_dir/cidata${1}.iso,device=cdrom --network bridge=virbr0,model=virtio --graphics none --noautoconsole

# virsh net-dhcp-leases default
