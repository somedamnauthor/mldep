import argparse

"""
Future work - Inputs:
bools for containers, vms and funcs - DONE
function api path - no
container name (= model name)
"""

parser = argparse.ArgumentParser(description="HAProxy Config Generator")

# Add arguments for container, vm, and func
parser.add_argument('--model', type=str, help='The model argument')
parser.add_argument('--container', type=str, help='The container argument')
parser.add_argument('--vm', type=str, help='The vm argument')
parser.add_argument('--func', type=str, help='The func argument')
parser.add_argument('--container_weight', type=str, help='The container weight')
parser.add_argument('--vm_weight', type=str, help='The vm weight')
parser.add_argument('--func_weight', type=str, help='The func weight')
parser.add_argument('--container_instances', type=str, help='Number of container instances')
parser.add_argument('--vm_instances', type=str, help='Number of VM instances')
parser.add_argument('--func_instances', type=str, help='Number of Function instances')

# Parse the command-line arguments
args = parser.parse_args()

# Get the values of container, vm, and func from the parsed arguments
container = args.container
vm = args.vm
func = args.func
model = args.model
container_weight = args.container_weight
vm_weight = args.vm_weight
func_weight = args.func_weight
container_instances = args.container_instances
function_instances = args.func_instances

proxy_backend_additions = ""
proxy_frontend_additions = ""
backend_additions = ""

# container = True
# vm = False
# func = True

if func=="true":

	base_port = 6004
	server_base = 4
	for i in range(int(function_instances)):
		port_bind = base_port + i
		server_num = server_base + i
		api_modifier = model+str(i+1)
		proxy_backend_additions = proxy_backend_additions + "  server proxy-server-"+str(server_num)+" localhost:"+str(port_bind)+" weight "+str(int(func_weight)/int(function_instances))+"\n"
		proxy_frontend_additions = proxy_frontend_additions + "\n\nfrontend proxy-in"+str(server_num)+"\n  bind :"+str(port_bind)+"\n  mode http\n  use_backend function"+str(i+1)
		backend_additions = backend_additions + "\n\nbackend function"+str(i+1)+"\n  mode http\n  http-request set-path /api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/"+api_modifier+"/%[path]\n  server function"+str(i+1)+" 172.17.0.1:3234 check"

# if container=="true":
# 	proxy_backend_additions = proxy_backend_additions + "\n  server proxy-server-2 localhost:6002 weight "+container_weight
# 	proxy_frontend_additions = proxy_frontend_additions + "\n\nfrontend proxy-in2\n  bind :6002\n  mode http\n  use_backend container"
# 	backend_additions = backend_additions + "\n\nbackend container\n  server container1 "+model+":5000 check"

if container=="true":
	proxy_backend_additions = proxy_backend_additions + "\n  server proxy-server-2 localhost:6002 weight "+container_weight
	proxy_frontend_additions = proxy_frontend_additions + "\n\nfrontend proxy-in2\n  bind :6002\n  mode http\n  use_backend container"
	backend_additions = backend_additions + "\n\nbackend container"

	base_port = 5000
	for i in range(1, int(container_instances)+1):
		server_name = "container"+str(i)
		container_name = model+str(i)
		host_port = base_port + i - 1
		# server container1 alexnet1:5000 check
		backend_additions = backend_additions + "\n  server "+server_name+" "+container_name+":5000 check"

if vm=="true":
	
	# # Read the content of the file into a string
	# with open("../VM/ip_out.txt", "r") as file:
	#     ip = file.read()
	# print("ip:",ip)

	# Open the file for reading

	ip_list = []
	
	with open("../VM/ip_out.txt", 'r') as file:
	    # Read each line in the file
	    for line in file:
	        # Strip any leading/trailing whitespace and add the IP to the list
	        ip = line.strip()
	        ip_list.append(ip)

	proxy_backend_additions = proxy_backend_additions + "\n  server proxy-server-3 localhost:6003 weight "+vm_weight
	proxy_frontend_additions = proxy_frontend_additions + "\n\nfrontend proxy-in3\n  bind :6003\n  mode http\n  use_backend vm"
	# backend_additions = backend_additions + "\n\nbackend vm\n  server vm1 "+ip+":5000 check"
	backend_additions = backend_additions + "\n\nbackend vm"

	for i in range(len(ip_list)):
		backend_additions = backend_additions + "\n  server vm"+str(i+1)+" "+ip_list[i]+":5000 check"

with open("mod-config.cfg", 'a') as file:
    file.write(proxy_backend_additions)
    file.write(proxy_frontend_additions)
    file.write(backend_additions)