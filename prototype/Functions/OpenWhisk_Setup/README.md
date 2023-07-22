Check out https://openwhisk.apache.org/documentation.html#openwhisk_deployment for comprehensive setup guide

# Requirements

1. Go
2. Java 8
3. Docker


# Setup OpenWhisk

```
git clone https://github.com/apache/openwhisk.git

cd openwhisk
```

# Edit Config for action memory limit

```
nano common/scala/src/main/resources/application.conf
```

Edit the following lines, set max to 1024 m

```
 # action memory configuration
    memory {
        min = 128 m
        max = 512 m
        std = 256 m
    }
```


# Start OpenWhisk in Standalone mode, built using Gradle

```
cd <openwhisk dir>

./gradlew -Dorg.gradle.java.home=/usr/lib/jvm/java-8-openjdk-amd64 core:standalone:bootRun --args="--api-gw"
```

Visit ```http://172.17.0.1:3232/playground/ui/index.html``` to see the playground. 

The server is being hosted at port 3233


# Setup OpenWhisk CLI

Visit ```https://github.com/apache/openwhisk-cli/releases```

Download the file appropriate for your system

Extract the tgz using ```tar -xvzf <file>.tgz```

Add the extracted file (wsk) to your system's bin directory using

```
cp wsk /usr/local/bin/wsk
```

Alternatively you could add your current OpenWhisk installation directory to the PATH variable - Refer to https://linuxize.com/post/how-to-add-directory-to-path-in-linux/

# Set APIHost (Optional, only if you want to use wsk CLI separately)

This, and the following steps, are optional. Placing the wsk CLI binary into the /usr/local/bin directory essentially gives the standalone JAR full control. However, if you want to test your actions out separately before deploying them via MLDep, you can try out this and the next two steps

```
./wsk property set --apihost 'http://172.17.0.1:3233' --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
```


# Create web action (Optional)

```
./wsk action create bert2 --docker somedamnauthor/custom_ml_runtime:mldepv3 exps/bert_function_code.py --memory 1024 --web=true
```

# Invoke action (Optional)

```
Use cURL or Postman to hit the endpoint yielded by the create action command
```
