NBSAP Quick Installation
=====

1. Clone the repository::

    git clone https://github.com/eaudeweb/nbsap.git -o github

2. Create & activate a virtual environment::

    virtualenv sandbox
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

7. Set up the MongoDB database::

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    echo '# MongoDB repo ###############' >> /etc/apt/sources.list

  7.1 If using Ubuntu >= 9.10 or running Upstart on Debian::

    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' >> /etc/apt/sources.list

  7.2 Otherwise(or using SysV init process)::

    echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' >> /etc/apt/sources.list

    sudo apt-get update
    sudo apt-get install mongodb-10gen

8. Prerequisites for filling database::

    ./bash-scripts/mongoimport.sh

9. Run a test server::

    ./manage.py runserver
