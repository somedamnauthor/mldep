virsh destroy mldep_vm
virsh undefine mldep_vm --remove-all-storage
#rm -f cidata.iso
#rm mldepimg.img
rm ipout.txt
rm -f base_images/focal.img
