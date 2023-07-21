"""
Pre-requisites: Place model files in a folder in the models directory (one level above)

Sample usage: python3 vm_wrapper.py image_classification
"""

import os
import time
import re
import sys

print("---------------------------------------------------------------------------------")
print("VM Wrapper: Setting up")
print("---------------------------------------------------------------------------------")

model_dir = "../models/"+sys.argv[1]+"/"
print("Model Directory:",model_dir)

lb_config_path = "../loadbalancer/haproxy.cfg"

net_pre_create = os.popen("virsh net-dhcp-leases default").read()

print("---------------------------------------------------------------------------------")
print("VM Wrapper: Creating VM")
print("---------------------------------------------------------------------------------")

os.system("sh create_vm.sh")

print("---------------------------------------------------------------------------------")
print("VM Wrapper: Logging into VM")
print("---------------------------------------------------------------------------------")

while True:

	net_post_create = os.popen("virsh net-dhcp-leases default").read()

	if net_pre_create != net_post_create:
		break
	else:
		print("VM Wrapper: Waiting for network creation...")
		time.sleep(3) 

b_s = net_post_create.splitlines()
a_s = net_pre_create.splitlines()

fstring = [x for x in b_s if x not in a_s]

# declaring the regex pattern for IP addresses
pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)')

lst = []

# extracting the IP addresses
for line in fstring:
   try:
       lst.append(pattern.search(line)[0])
   except:
       pass

#displaying the extracted IP addresses
try:
    ip = lst[0][:-3]
except:
    pass

print("IP Address Found:",ip)

try:
	ssh_keygen_command = "ssh-keygen -R "+ip
	os.system(ssh_keygen_command)
except:
	pass


copy_command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r "+model_dir+" ubuntu@"+ip+":/home/ubuntu/ml/"
copy_install_command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r installPackages.sh ubuntu@"+ip+":/home/ubuntu/ml/"
install_command = "sshpass -p 'admin' ssh ubuntu@"+ip+" 'sh /home/ubuntu/ml/installPackages.sh'"
# start_command = "sshpass -p 'admin' ssh ubuntu@"+ip+" 'cd /home/ubuntu/ml; python3 wrapper.py'"
start_command = "sshpass -p 'admin' ssh ubuntu@"+ip+" 'cd /home/ubuntu/ml; nohup python3 wrapper.py > applogs.txt 2>&1 &'"

print(copy_command)
while True:
	if os.system(copy_command)!=0:
		print("VM Wrapper: Retrying Connection...")
		time.sleep(1)
		continue
	else:
		break

print("---------------------------------------------------------------------------------")
print("VM Wrapper: Installing Packages")
print("---------------------------------------------------------------------------------")

print(copy_install_command)
os.system(copy_install_command)

print(install_command)
os.system(install_command)

print("---------------------------------------------------------------------------------")
print("VM Wrapper: Starting Model")
print("---------------------------------------------------------------------------------")

print(start_command)
os.system(start_command)

print("---------------------------------------------------------------------------------")
print("VM Wrapper: Adding backend to loadbalancer")
print("---------------------------------------------------------------------------------")

lb_conf_command = "echo '  server "+sys.argv[1]+"_vm1 "+ip+":5000 check' >> "+lb_config_path
print(lb_conf_command)
os.system(lb_conf_command)
os.system("sudo docker kill -s HUP haproxy")