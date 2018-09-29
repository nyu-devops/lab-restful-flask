# lab-restful-flask

[![Build Status](https://travis-ci.org/nyu-devops/lab-restful-flask.svg?branch=master)](https://travis-ci.org/rofrano/nyu-lab-travis-ci)
[![Codecov](https://codecov.io/gh/nyu-devops/lab-restful-flask/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops/lab-restful-flask)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

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
    $ python run.py
```

You should now be able to see the service running in your browser by going to
[http://localhost:5000](http://localhost:5000). You will see a message about the
service which looks something like this:

```
{
    name: "Pet Demo REST API Service",
    url: "http://localhost:5000/pets",
    version: "1.0"
}
```

When you are done, you can use `Ctrl+C` within the VM to stop the server.

## Alternative starting of the service

For running the service during development and debugging, you can also run the server
using the `flask` command with:

```
    $ export FLASK_APP=app/service.py
    $ flask run -h 0.0.0.0
```

or you can specify this all on one line with:

```
    $ env FLASK_APP=app/service.py flask run -h 0.0.0.0
```

Note that we need to bind the host IP address with `-h 0.0.0.0` so that the forwarded ports work correctly in **Vagrant**. If you were running this locally on your own computer you would not need this extra parameter.

Finally you can use the `honcho` command to start `gunicorn` to run the servce with:

```
    $ honcho start
```

**Honcho** uses the `Procfile` to determine how to run the service. This file uses **Gunicorn** which is how you would start the server in production.

## Testing

Run the tests suite with:

```
    $ nosetests
```

You should see all of the tests passing with a code coverage report at the end. this is controlled by the `setup.cfg` file in the repo.

## Shutdown

When you are done, you can use the `exit` command to get out of the virtual machine just as if it were a remote server and shut down the vm with the following:

```
    $ exit
    $ vagrant halt
```

If the VM is no longer needed you can remove it with from your computer to free up disk space with:

```
    $ vagrant destroy
```

This repo is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created by John Rofrano.
