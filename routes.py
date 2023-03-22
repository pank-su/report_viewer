"""
Routes and views for the bottle application.
"""

from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='О нас',
        message='Здесь вы можете ознакомиться с возможностями нашего сайта',
        year=datetime.now().year,
        functions='На этом сайте можно:',
        func1='делиться отчётами',
        func2='просматривать отчёты',
        func3='загружать отчёты',
        func4='менять формат отчётов'
    )
