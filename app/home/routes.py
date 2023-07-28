# -*- encoding: utf-8 -*-

from app import tryton
from app.home import blueprint

from flask import render_template, redirect, url_for, request, session
from jinja2 import TemplateNotFound

from functools import wraps

WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_key = None
        if 'session_key' in session:
            session_key = session['session_key']
        user = Session.get_user(session_key)
        if not user:
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return wrapper

@blueprint.route('/')
def index():
    return render_template('/index.html')

@blueprint.route('/<template>')
def route_template(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'
        # Detect the current page
        segment = get_segment( request )
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template,segment=segment)
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
