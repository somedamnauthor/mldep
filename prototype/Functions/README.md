# Usage

Refer to OpenWhisk_Setup/README.md first to set up OpenWhisk

### Deploy function

1. Place model files inside appropriately named folder inside the ```../models``` directory

2. Deploy function using

```
sh function_deploy.sh <path_to_openwhisk> <model_directory_name>
```

For example, the following command assumes that a folder named ```bert``` has been created in the ```../models``` dir, and the OpenWhisk installation is located at /home/ubuntu

```
sh function_deploy.sh /home/ubuntu/openwhisk bert
```

The ```function_deploy.sh``` script first creates the function code by stitching together the user-provided model code and an MLDep-provided main method, following which it creates an OpenWhisk action using the stitched code.

NOTE: When executed for the first time, the script will pull a docker image containing the action runtime. This image acts as the runtime for all models, and thus is not pulled multiple times.

### Undeploy function

The following command deletes the action and removes the stitched code file
```
sh function_undeploy.sh <path_to_openwhisk> <model_directory_name>
```
