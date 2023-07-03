# importing the module
import re
import os

os.system("virsh net-dhcp-leases default > ipout.txt")

# opening and reading the file 
with open('ipout.txt') as fh:
   fstring = fh.readlines()
  
# declaring the regex pattern for IP addresses
pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)')

# initializing the list object
lst=[]
  
# extracting the IP addresses
for line in fstring:
   try:
       lst.append(pattern.search(line)[0])
   except:
       pass
  
# displaying the extracted IP addresses
try:
    ip = lst[0][:-3]
except:
    pass

ip = "192.168.122.139"

copy_command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r ../image_classification/ ubuntu@"+ip+":/home/ubuntu/ml/"
copy_install_command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r installPackages.sh ubuntu@"+ip+":/home/ubuntu/ml/"
install_command = "sshpass -p 'admin' ssh ubuntu@"+ip+" 'sh /home/ubuntu/ml/installPackages.sh'"
start_command = "sshpass -p 'admin' ssh ubuntu@"+ip+" 'cd /home/ubuntu/ml; python3 wrapper.py'"

print(copy_command)
os.system(copy_command)

print(copy_install_command)
os.system(copy_install_command)

print(install_command)
os.system(install_command)

print(start_command)
os.system(start_command)
