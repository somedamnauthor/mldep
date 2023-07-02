# importing the module
import re
  
# opening and reading the file 
with open('ipout.txt') as fh:
   fstring = fh.readlines()
  
# declaring the regex pattern for IP addresses
#pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3})')
#pattern = re.compile(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,3}$')
#pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
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
    ip = lst[0]
except:
    pass


