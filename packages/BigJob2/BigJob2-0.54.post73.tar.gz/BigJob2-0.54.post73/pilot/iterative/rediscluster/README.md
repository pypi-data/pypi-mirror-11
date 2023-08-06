# redis-py-cluster

Python cluster client for the official cluster support targeted for redis 3.0

This project is a port to python based on the redis-rb-cluster implementation done by antirez.

The original source can be found at https://github.com/antirez/redis-rb-cluster



## Dependencies

- redis (Python client - https://github.com/andymccurdy/redis-py - Install [pip install redis])
- Cluster enabled redis server (Download the branch that is version 2.9.9+ and that will be 3.0.0 in the future. Build redis and setup a cluster with n machines. Redis can be found at https://github.com/antirez/redis) (Or use the docker image to create a new cluster)



## Docker support

To make it easier to test this library there is an Dockerfile that can be used to install and run an entire redis cluster.

The cluster is 6 redis instances running with 3 master & 3 slaves.

It will allways run on the latest commit in the 3.0 branch of redis git repo (https://github.com/antirez/redis). To change this, change the git clone command inside Dockerfile.

How to setup docker and start the cluster image.

- Install lxc-docker on your system (I currently use Docker version 0.7.1, build 88df052) (Instructions can be found at: http://docs.docker.io/en/latest/installation/)
- Naviaget to root of this project
- Run 'make docker-build'
- Run 'make docker-run' or 'make docker-run-d' if you want to run the image in daemon (For interactive/debug mode run 'make docker-run-interactive')
- redis-trib.rb will prompt your for a question to create the cluster, type 'yes' and press enter.
- Test the connection by running either 'redis-cli -p 7000' or 'python example.py'



## Implemented commands

- set
- get
- smembers
- srem
- delete
- sadd
- publish
- hset
- hget
- hdel
- hexists
- type
- exists
- rename (NYI)
- renamex (NYI)



## How to setup a cluster manually

 - This video will describe how to setup and use a redis cluster: http://vimeo.com/63672368 (This video is old so look at instructions in Redis cluster tutorial link below)
 - Redis cluster tutorial: http://redis.io/topics/cluster-tutorial
 - Redis cluster specs: http://redis.io/topics/cluster-spect



## Python support

Current python support is

- 2.6   (Not yet tested)
- 2.7.5 (Working)
- 3.1   (Not yet tested)
- 3.2   (Not yet tested)
- 3.3   (Not yet tested)
- 3.4   (Not yet tested)



## Speed

On my laptop with x2 redis servers in cluster mode and one python process on the same machine i do 50k set/get commands in between 6-8 sec



## Disclaimer

Both this client and Redis Cluster are a work in progress that is not suitable to be used in production environments. This is only my current personal opinion about both projects.



## License

This is done for educational purposes and to test the official cluster support for redis
