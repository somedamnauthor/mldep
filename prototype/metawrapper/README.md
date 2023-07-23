# Usage

```
sh mldep.sh <model folder name> -c <true/false> -f <true/false> -v <true/false>
```

This command performs the necessary deployments and gives the user a unified endpoint at ```http://localhost:6000/predict```

The ```-c```, ```-f``` and ```-v``` arguments indicate whether the model is being deployed as a container, function and/or VM respectively

Example usage: The command below deploys the resnet50 model as a container and a function simultaneously routed through a loadbalancer with the deployment endpoint hosted at localhost:6000

```
sh mldep.sh resnet50 -c true -f true -v false 
```

This command assumes that a folder named resnet50 in the ```prototype/models``` folder has the model files written according to the template

# Teardown

To teardown all the deployments in one go, run the teardown script like so - 

```
sh teardown.sh <model folder name>
```

This will delete any function actions, remove the container, destroy and undefine the virtual machine domains and finally remove the load-balancer container

Example usage: 

```
sh teardown.sh resnet50
```
