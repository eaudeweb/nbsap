Product owner:
-------
    * Franz Daffner
    * franz.daffner@eea.europa.eu

Min. hardware resources
-------

    * [CPU] Single Core >= 2.5 GHz
    * [RAM] 1024 MB
    * [Hard disc] current necessary < 1 GB
    * [Hard disc] 6 months forecast <= 20 GB
    * [NIC] 100 Mbit

Min. software resources
-------

    * Software dependencies stated below in a step-by-step short guide
    * UNIX (kernel version >= 2.6)
    * mongodb-10gen database
    * python 2.7
    * all other dependecies are stated in the requirements.txt file


About
-------
National Biodiversity Strategies and Action Plan (or simply NBSAP) (http://nbsap.eaudeweb.ro/)
is a platform for organizing the implementation of Belgium's national biodiversity strategy
after AICHI. It consists of two panels each corresponding an operation: viewing and editing.

The first panel allows anyone to overview the aichi goals, targets and
indicators along with national strategy mappings (the way a country develops its
own strategy in terms of objectives and actions) and its implementation.

The second panel(Admin), authentication-available only, allows an user to actually define
the national strategy. (e.g. add/modify/delete an objective, action or even
elements from AICHI) in the purpose of building it.


NBSAP Quick Installation Guide
=====
0. Install python prerequisites if missing::

    apt-get install python-setuptools python-dev


1. Clone the repository::

    git clone https://github.com/eaudeweb/nbsap.git -o github
    cd nbsap

2. Create & activate a virtual environment::

    virtualenv sandbox
    echo '*' > sandbox/.gitignore
    echo 'instance' >> .gitignore
    . sandbox/bin/activate

3. Install dependencies::

    pip install -r requirements-dev.txt

4. Create a configuration file::

    mkdir -p instance
    echo 'SECRET_KEY = "nbsap random stuff"' >> instance/settings.py
    echo 'MONGO_HOST = "0.0.0.0"' >> instance/settings.py
    echo 'MONGO_PORT = 27017' >> instance/settings.py
    echo 'MONGO_DBNAME = "nbsap"' >> instance/settings.py
    echo 'DATABASE_URI = "sqlite:///"' >> instance/settings.py
    echo 'DATABASE_URI_NAME = "/users-openid.db"' >> instance/settings.py

    4.1 If there is a need for EU strategy
    echo 'EU_STRATEGY = True' >> instance/settings.py

    4.2 Otherwise
    echo 'EU_STRATEGY = False' >> instance/settings.py

5.1 Set up MongoDB database for Debian based systems::

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    echo '# MongoDB repo ###############' >> /etc/apt/sources.list

    5.1.1 If using Ubuntu >= 9.10 or running Upstart on Debian::

    echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' >> /etc/apt/sources.list

    5.1.2 Otherwise(or using SysV init process)::

    echo 'deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen' >> /etc/apt/sources.list

    5.1.3 Issue the following command (as root or with sudo) to install the
    latest stable version of MongoDB and the associated tools:

    sudo apt-get install mongodb-10gen

5.2 Set up MongoDB database for CentOS based systems::

    5.2.1 Create a /etc/yum.repos.d/10gen.repo file to hold information about your
    repository. If you are running a 64-bit system (recommended,) place the
    following configuration in /etc/yum.repos.d/10gen.repo file:

    [10gen]
    name=10gen Repository
    baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
    gpgcheck=0
    enabled=1

    5.2.2 Issue the following command (as root or with sudo) to install the
    latest stable version of MongoDB and the associated tools:

    yum install mongo-10gen mongo-10gen-server

6. Prerequisites for creating & filling databases(both data and users)::

    ./bin/mongoimport.sh
    ./manage.py syncdb

10. Run a test server(see http://127.0.0.1:5000 afterwards)::

    ./manage.py runserver

