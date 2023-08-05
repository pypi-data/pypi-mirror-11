Django FAB Deployer
===================

|Requirements Status|

Installation
------------

.. code:: bash

    pip install --upgrade django_fab_deployer

Usage
-----

.. code:: bash

    # Generate example deployment configuration:
    djdeploy write_example_config

Command above will generate ``example.json`` file in current directory.
Example of deployment configuration:

.. code:: json

    {
      "dev": {
        "celery_enabled": true, 
        "deploy_path": "/var/www/dev_my_project", 
        "hosts": "8.8.8.8", 
        "key_filename": "~/.ssh/id_rsa.PUB", 
        "project_name": "dev_my_project", 
        "user": "dev_my_project", 
        "venv_path": "data/.venv/bin/activate", 
        "warn_on_deploy": false
      }, 
      "production": {
        "celery_enabled": true, 
        "deploy_path": "/var/www/prod_my_project", 
        "hosts": "8.8.8.8", 
        "key_filename": "~/.ssh/id_rsa.PUB", 
        "project_name": "prod_my_project", 
        "user": "prod_my_project", 
        "venv_path": "data/.venv/bin/activate", 
        "warn_on_deploy": true
      }
    }

Save this file as ``deploy.json`` and run:

.. code:: bash

    djdeploy dev deploy # To upgrade pip requirements: djdeploy dev deploy:upgrade=True
    # Or
    djdeploy production deploy

.. |Requirements Status| image:: https://requires.io/github/illagrenan/django-fab-deployer/requirements.svg?branch=master
   :target: https://requires.io/github/illagrenan/django-fab-deployer/requirements/?branch=master


