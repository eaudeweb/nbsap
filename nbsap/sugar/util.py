from functools import wraps

import flask

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            if template_name is None: template_name = ctx.pop("template")
            return flask.render_template(template_name, **ctx)
        decorated_function.not_templated = f
        return decorated_function
    return decorator

