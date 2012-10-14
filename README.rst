NBSAP (http://nbsap.eaudeweb.ro/) is a website for organizing the implementation
of Belgium's national biodiversity strategy after AICHI.

NBSAP Quick Installation
=====

1. Clone the repository::

    git clone https://github.com/eaudeweb/nbsap.git -o github

2. Create & activate a virtual environment::

    virtualenv sandbox
    echo '*' > sandbox/.gitignore
    echo 'instance' >> .gitignore
    . sandbox/bin/activate

3. Install prerequisites if missing::

    apt-get install python-setuptools python-dev

4. Install dependencies::

    pip install -r requirements-dev.txt

5. Create a configuration file::

    mkdir -p instance
    echo 'SECRET_KEY = "nbsap random stuff"' >> instance/settings.py
    echo 'MONGO_HOST = "0.0.0.0"' >> instance/settings.py
    echo 'MONGO_PORT = 27017' >> instance/settings.py
    echo 'MONDO_DBNAME' = 'nbsap'
    echo 'DATABASE_URI = "sqlite:///"'
    echo 'DATABASE_URI_NAME = "/users-openid.db"'

7. Set up the MongoDB database prerequisites::

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    echo '# MongoDB repo ###############' >> /etc/apt/sources.list

    7.1 If using Ubuntu >= 9.10 or running Upstart on Debian::

    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' >> /etc/apt/sources.list

    7.2 Otherwise(or using SysV init process)::

    echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' >> /etc/apt/sources.list


8. Install MongoDB database::

    sudo apt-get update
    sudo apt-get install mongodb-10gen

8. Prerequisites for filling database::

    ./bash-scripts/mongoimport.sh
    ./manage.py syncdb

9. Run a test server(see http://127.0.0.1:5000 afterwards)::

    ./manage.py runserver

