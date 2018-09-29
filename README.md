# lab-restful-flask

[![Build Status](https://travis-ci.org/nyu-devops/lab-restful-flask.svg?branch=master)](https://travis-ci.org/rofrano/nyu-lab-travis-ci)
[![Codecov](https://img.shields.io/codecov/c/github/nyu-devops/lab-restful-flask.svg)]()
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

## Alternative starting of the service

For running the service during development and debugging, you can also run the server
using the `flask` command with:

```
    $ export FLASK_APP=app/service.py
    $ flask run -h 0.0.0.0
```

or you can specify this all on one like with:

```
env FLASK_APP=app/service.py flask run -h 0.0.0.0
```

Note that we need to bind the host with `-h 0.0.0.0` so that the forwarded ports work correctly in **Vagrant**
If you were running this locally on your own computer you would not need this extra parameter.

Finally you can use the `honcho` command to start `gunicorn` to run the servce with:

```
honcho start
```

**Honcho** uses the `Procfile` to determine how to run the service. This file uses **Gunicorn** which is how you would start the server in production

## Testing

Run the tests suite with:

```
    $ nosetests
```

When you are done, you can use `Ctrl+C` to stop the server.

## Shutdown

When you are done, you can use `exit` to get out of the virtual machime and shut down the vm with:

```
    $ exit
    $ vagrant halt
```

If the VM is no longer needed you can remove it with:

```
    $ vagrant destroy
```

This repo is part of the NYU DevOps CSCI-GA.2820-001 class
