from flask import session, render_template
from functools import wraps

def ucheck_logged_in(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'logged_in' in session and 'username' in session:
            
            return func(*args,**kwargs)
        else:
            return render_template('homepage.html',
                                   the_title1='please log in to view the page')
                                   
    return wrapper


def adcheck_logged_in(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'logged_in' in session and 'admin' in session:
            
            return func(*args,**kwargs)
        else:
            return render_template('homepage.html',
                                   the_title1='please log in to view the page')
                                   
    return wrapper


def check_logged_out(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'logged_in' not in session:
            
            return func(*args,**kwargs)

        elif 'username' in session:

            return render_template('mainmenu1.html',
                                    the_title1='You are now logged in as "donor". Your username is ',
                                    the_title2=session['username'])

        else:

            return render_template('mainmenu2.html',
                                    the_title1='You are now logged in as "admin". Your username is ',
                                    the_title2=session['admin'])
                                   
    return wrapper
