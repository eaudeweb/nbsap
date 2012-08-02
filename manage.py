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
    ctx = {
            'app': flask.current_app,
    }
    return ctx

if __name__=="__main__":
    manager.run()

