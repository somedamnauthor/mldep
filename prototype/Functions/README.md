Check out https://openwhisk.apache.org/documentation.html#openwhisk_deployment for comprehensive setup guide

# Setup OpenWhisk

```
git clone https://github.com/apache/openwhisk.git

cd openwhisk
```

# Start OpenWhisk

```
cd <openwhisk dir>

./gradlew -Dorg.gradle.java.home=/usr/lib/jvm/java-8-openjdk-amd64 core:standalone:bootRun
```

Visit ```http://172.17.0.1:3232/playground/ui/index.html``` to see the playground. 

The server is being hosted at port 3233


# Set APIHost:

```
./wsk property set --apihost 'http://172.17.0.1:3233' --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
```

# Create action:

```
./wsk action create test1 --docker custom_ml_runtime:latest exps/test-torch.py
```


