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

# Parse the command-line arguments
args = parser.parse_args()

# Get the values of container, vm, and func from the parsed arguments
container = args.container
vm = args.vm
func = args.func
model = args.model

proxy_backend_additions = ""
proxy_frontend_additions = ""
backend_additions = ""

# container = True
# vm = False
# func = True

if func=="true":
	proxy_backend_additions = proxy_backend_additions + "  server proxy-server-1 localhost:6001"
	proxy_frontend_additions = proxy_frontend_additions + "\n\nfrontend proxy-in1\n  bind :6001\n  mode http\n  use_backend function"
	backend_additions = backend_additions + "\n\nbackend function\n  mode http\n  http-request set-path /api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/%[path]\n  server function1 172.17.0.1:3234 check"

if container=="true":
	proxy_backend_additions = proxy_backend_additions + "\n  server proxy-server-2 localhost:6002"
	proxy_frontend_additions = proxy_frontend_additions + "\n\nfrontend proxy-in2\n  bind :6002\n  mode http\n  use_backend container"
	backend_additions = backend_additions + "\n\nbackend container\n  server container1 "+model+":5000 check"

with open("mod-config.cfg", 'a') as file:
    file.write(proxy_backend_additions)
    file.write(proxy_frontend_additions)
    file.write(backend_additions)