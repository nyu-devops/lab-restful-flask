# lab-restful-flask

This repo demonstrates how to create a simple RESTful service using Python Flask.
The resource model has no persistence to keep the application simple. It's purpose is to show the correct API and return codes that should be used for a REST API.

## Prerequisite Installation using Vagrant

The easiest way to use this lab is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Clone the project to your development folder and create your Vagrant vm
```
    $ git clone https://github.com/nyu-devops/lab-restful-flask.git
    $ cd lab-restful-flask
    $ vagrant up
```

Once the VM is up you can use it with:
```
    $ vagrant ssh
    $ cd /vagrant
    $ python app/server.py
```

Run the tests suite with:
```
    $ nosetests
```

When you are done, you can use `Ctrl+C` to stop the server and then exit and shut down the vm with:
```
    $ exit
    $ vagrant halt
```

If the VM is no longer needed you can remove it with:
```
    $ vagrant destroy
```

This repo is part of the NYU DevOps CSCI-GA.2820-001 class
