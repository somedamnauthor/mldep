"""
Pre-requisites: Place model files in a folder in the models directory (one level above)

Sample usage: python3 vm_wrapper.py image_classification 3 true /home/img/ 2

# {1} - model
# {2} - instances
# {3} - root access for libvirt
# {4} - cloud image dir
# {5} - CPUs

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

# Open the IPs list file in write mode to empty its contents
with open('ip_out.txt', "w") as file:
    pass  # You can leave the block empty or use 'pass' to indicate no action


if sys.argv[3] == "true":
	net_command = "virsh net-dhcp-leases default"
else:
	net_command = "virsh -c qemu:///system net-dhcp-leases default"


for i in range(1, int(sys.argv[2])+1):

	net_pre_create = os.popen(net_command).read()
	os.popen(net_command)

	print("---------------------------------------------------------------------------------")
	print("VM Wrapper: Creating VM "+str(i))
	print("---------------------------------------------------------------------------------")

	create_command = "sh create_vm.sh "+str(i)+" "+sys.argv[3]+" "+sys.argv[4]+" "+sys.argv[5]
	print(create_command)
	os.system(create_command)

	print("---------------------------------------------------------------------------------")
	print("VM Wrapper: Logging into VM "+str(i))
	print("---------------------------------------------------------------------------------")

	while True:

		net_post_create = os.popen(net_command).read()

		if net_pre_create != net_post_create:

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

			ip = ""

			#displaying the extracted IP addresses
			try:
			    ip = lst[0][:-3]
			except:
			    pass


			ip_list = []

			with open("ip_out.txt", 'r') as file:
			    # Read each line in the file
			    for line in file:
			        # Strip any leading/trailing whitespace and add the IP to the list
			        ip_read = line.strip()
			        ip_list.append(ip_read)

			if ip in ip_list:
				print("VM Wrapper: Error reading IP, retrying...")
				time.sleep(3) 
			else:
				break

		else:
			print("VM Wrapper: Waiting for network creation...")
			time.sleep(3) 


	with open('ip_out.txt', "a") as file:
		file.write(ip + "\n")

	try:
		ssh_keygen_command = "ssh-keygen -R "+ip
		os.system(ssh_keygen_command)
	except:
		pass


	copy_command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r "+model_dir+" ubuntu@"+ip+":/home/ubuntu/ml/"
	copy_install_command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r installPackages.sh ubuntu@"+ip+":/home/ubuntu/ml/"
	install_command = "sshpass -p 'admin' ssh ubuntu@"+ip+" 'sh /home/ubuntu/ml/installPackages.sh'"
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
	print("VM Wrapper: Installing Packages for VM "+str(i))
	print("---------------------------------------------------------------------------------")

	print(copy_install_command)
	os.system(copy_install_command)

	print(install_command)
	os.system(install_command)

	print("---------------------------------------------------------------------------------")
	print("VM Wrapper: Starting Model in VM "+str(i))
	print("---------------------------------------------------------------------------------")

	print(start_command)
	os.system(start_command)
