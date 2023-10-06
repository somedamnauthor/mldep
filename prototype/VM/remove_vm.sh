virsh list --all | grep -o -E "(mldep_vm\w*)" | \
xargs -I % sh -c 'virsh destroy % && virsh undefine % --remove-all-storage'

#virsh destroy mldep_vm
#virsh undefine mldep_vm --remove-all-storage
#rm -f cidata.iso
#rm mldepimg.img
#rm ipout.txt

rm -f base_images/focal.img
