#virsh list --all | grep -o -E "(mldep_vm\w*)" | \
#xargs -I % sh -c 'virsh destroy % && virsh undefine % --remove-all-storage'

#virsh destroy mldep_vm
#virsh undefine mldep_vm --remove-all-storage
#rm -f cidata.iso
#rm mldepimg.img
#rm ipout.txt

#rm -f base_images/focal.img

if [ ${1} = "true" ]; then
    vir_arg=""
else
    vir_arg="-c qemu:///system"
fi

# Loop to run the Docker command 'number' times
for i in $(seq 1 ${2}); do
    vm_name="mldep_vm$i"
    virsh $vir_arg destroy $vm_name 
    virsh $vir_arg undefine $vm_name --remove-all-storage
done
