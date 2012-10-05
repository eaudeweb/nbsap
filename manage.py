#!/usr/bin/env python

import os.path
import flask
import flaskext.script


def create_app():
    import nbsap.app
    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance'))
    return nbsap.app.create_app(instance_path)

manager = flaskext.script.Manager(create_app)

@manager.shell
def make_shell_context():
    import nbsap.shell
    from nbsap.database import mongo
    ctx = {
            'app': flask.current_app,
            'mongo': mongo
        }
    ctx.update(nbsap.shell.extra_shell_context)
    return ctx

@manager.command
def syncdb():
   # init users database
   from nbsap.database import Base
   Base.metadata.create_all()

class FcgiCommand(flaskext.script.Command):

    def handle(self, app):
        from flup.server.fcgi import WSGIServer
        sock_path = os.path.join(app.instance_path, 'fcgi.sock')
        server = WSGIServer(app, bindAddress=sock_path, umask=0, maxThreads=5)
        server.run()

manager.add_command('fcgi', FcgiCommand())

if __name__=="__main__":
    manager.run()

