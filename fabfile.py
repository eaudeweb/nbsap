from functools import wraps
from fabric.api import *
from fabric.contrib.files import exists
from path import path as ppath


env['nbsap_target_defs'] = {
    'staging': {
        'host_string': 'edw@rom.edw.ro',
        'nbsap_repo':     '/var/local/nbsap',
        'nbsap_instance': '/var/local/nbsap/instance',
        'nbsap_sandbox':  '/var/local/nbsap/sandbox',
        'nbsap_client_root': '/var/local/nbsap/instance_',
        'nbsap_clients': [
                            'burundi',
                            'cameroun',
                            'benin',
                            'niger',
                            'madagascar',
                            'rdc',
                            'burkinafaso',
                            'cotedivoire',
                            'comifac',
                            'algerie',
                            'cbd',
                            'maroc',
                            'training'
                        ]
    },
}


env['nbsap_default_target'] = 'staging'


def choose_target(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.pop('target', None)
        if name is None and 'nbsap_target' not in env:
            name = env['nbsap_default_target']

        if name is None:
            target_env = {}
        else:
            target_env = env['nbsap_target_defs'][name]
            target_env['nbsap_target'] = name

        with settings(**target_env):
            return func(*args, **kwargs)

    return wrapper


@task
@choose_target
def ssh():
    open_shell("cd '%(nbsap_repo)s' && "
               "source '%(nbsap_sandbox)s'/bin/activate"
               % env)


@task
@choose_target
def install():
    if not exists("%(nbsap_repo)s/.git" % env):
        run("git init '%(nbsap_repo)s'" % env)

    local("git push -f '%(host_string)s:%(nbsap_repo)s' HEAD:incoming" % env)
    with cd(env['nbsap_repo']):
        run("git reset incoming --hard")

    if not exists(env['nbsap_sandbox']):
        run("virtualenv --no-site-packages '%(nbsap_sandbox)s'" % env)
        run("echo '*' > '%(nbsap_sandbox)s/.gitignore'" % env)

    run("%(nbsap_sandbox)s/bin/pip install "
        "-r %(nbsap_repo)s/requirements.txt"
        % env)

    if not exists(env['nbsap_instance']):
        run("mkdir -p '%s'" % env['nbsap_instance'])

    """
    for country in env['nbsap_clients']:
        i = "".join([env['nbsap_client_root'], country])
        if not exists(i):
            run("mkdir -p '%s'" % i)
    """

@task
@choose_target
def start():
    run("/sbin/start-stop-daemon --start --background "
        "--pidfile %(nbsap_instance)s/fcgi.pid --make-pidfile "
        "--exec %(nbsap_sandbox)s/bin/python %(nbsap_repo)s/manage.py fcgi"
        % env, pty=False)

    """
    for country in env['nbsap_clients']:
        i = "".join([env['nbsap_client_root'], country])
        run("/sbin/start-stop-daemon --start --background "
            "--pidfile {0}/fcgi.pid --make-pidfile "
            "--exec {1}/bin/python {2}/manage_{3}.py fcgi".format(i,
            env['nbsap_sandbox'], env['nbsap_repo'], country), pty=False)
    """


@task
@choose_target
def stop():
    run("/sbin/start-stop-daemon --stop --retry 3 --oknodo "
        "--pidfile %(nbsap_instance)s/fcgi.pid" % env)

    """
    for country in env['nbsap_clients']:
        i = "".join([env['nbsap_client_root'], country])
        run("/sbin/start-stop-daemon --stop --retry 3 --oknodo "
            "--pidfile %s/fcgi.pid" % i)
    """

@task
@choose_target
def syncdb():
    run("%(nbsap_sandbox)s/bin/python %(nbsap_repo)s/manage.py syncdb" % env)


@task
@choose_target
def restart():
    execute('stop')
    execute('start')


@task
@choose_target
def deploy():
    execute('install')
    execute('restart')
