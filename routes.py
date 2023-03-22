"""
Routes and views for the bottle application.
"""
import os
from random import getrandbits

import pypandoc
from bottle import route, view, request, response
from datetime import datetime
import sqlite3

SECRET = "ABOBA"


@route('/')
@route('/editor')
@view('editor')
def editor():
    """Renders the home page."""
    secret = request.get_cookie("secret", secret=SECRET)
    if secret is None:
        return dict(
            year=datetime.now().year
        )
    else:
        return dict(
            year=datetime.now().year,
            filename=""
        )


@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        year=datetime.now().year
    )


@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About us',
        message='Here you can see the possibilities of our site',
        year=datetime.now().year,
        functions='At this site you could:',
        func1='share reports',
        func2='watch reports',
        func3='download reports',
        func4='change report format'
    )


@route('/upload', method='POST')
@view("editor")
def do_upload():
    upload = request.files.get('inputFile')
    print(upload)

    temp_path = "./tmp"
    save_path = "./save"

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = f"{temp_path}/{upload.filename}"
    upload.save(file_path)
    output = pypandoc.convert_file(file_path, 'org')
    random_bits = getrandbits(128)
    hash = "%032x" % random_bits
    with open(f"{save_path}/{hash}.org", "w", encoding="utf-8") as f:
        f.write(output)
    os.remove(file_path)
    conn = sqlite3.connect("info.db")
    cur = conn.cursor()
    random_bits = getrandbits(128)
    hash = "%032x" % random_bits
    client_ip = request.environ.get('REMOTE_ADDR')
    cur.execute("""INSERT INTO users VALUES (?, ?)""", (hash, client_ip))
    cur.execute("""INSERT INTO files VALUES (?, ?)""", (hash, f"{save_path}/{hash}.org"))
    conn.commit()
    cur.close()
    conn.close()
    response.set_cookie("secret", hash, secret=SECRET)
    return "File successfully saved to '{0}'.".format(f"{save_path}/{hash}.org")
