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
    ip = lst[-1][:-3]
except:
    pass

command = "sshpass -p 'admin' scp -oStrictHostKeyChecking=no -r ../image_classification/ ubuntu@"+ip+":/home/ubuntu/ml/"

print(command)

#os.system("ssh-keygen -R ubuntu@"+ip)

os.system(command)
