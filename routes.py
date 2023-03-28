"""
Routes and views for the bottle application.
"""
import os
import sqlite3
import time
from datetime import datetime
from random import getrandbits

import pypandoc
from bottle import route, view, request, response, redirect
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)
data = supabase.auth.sign_in_with_oauth({
    "provider": 'github'
})

# переменная, содержащая секретный ключ, используемый для защиты куков
SECRET = os.environ.get("SECRET_TOKEN")
# это переменная, содержащая путь к директории, в которой будут храниться файлы превью
preview_path = "./preview"


@route('/')
@route('/editor')
@view('editor')
def editor():
    query = request.query
    user = None
    if request.query_string != "":
        try:
            response.set_cookie("access_token", query["access_token"], secret=SECRET)
            response.set_cookie("expires_in", query["expires_in"], secret=SECRET)
            response.set_cookie("provider_token", query["provider_token"], secret=SECRET)
            response.set_cookie("refresh_token", query["refresh_token"], secret=SECRET)
            supabase.auth.refresh_session(query["refresh_token"])
            user = supabase.auth.get_user()
        except Exception as e:
            print(e)
            user = None
    print(user)
    if user is None:
        try:
            supabase.auth.set_session(request.get_cookie("access_token", "", secret=SECRET),
                                  request.get_cookie("refresh_token", "", secret=SECRET))
            user = supabase.auth.get_user()
        except Exception as e:
            user = None
    # secret = request.get_cookie("secret", secret=SECRET)
    return dict(
        year=datetime.now().year,
        userExist=user is not None
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
    """Обработчик маршрута, которая обрабатывает POST-запрос на загрузку файла. Она сохраняет загружxенный файл во
    временную директорию, конвертирует его в формат org с помощью pypandoc, генерирует случайный хэш-код и сохраняет
    конвертированный файл с использованием этого хэш-кода в постоянную директорию"""
    upload = request.files.get('inputFile')

    temp_path = "./tmp"
    save_path = "./save"

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if not os.path.exists(preview_path):
        os.makedirs(preview_path)

    file_path = f"{temp_path}/{upload.filename}"
    upload.save(file_path)
    output = pypandoc.convert_file(file_path, 'org')
    random_bits = getrandbits(128)
    file_hash = "%032x" % random_bits
    hash_path = f"{save_path}/{file_hash}.org"
    with open(hash_path, "w", encoding="utf-8") as f:
        f.write(output)
    os.remove(file_path)
    conn = sqlite3.connect("info.db")
    cur = conn.cursor()
    random_bits = getrandbits(128)
    hash = "%032x" % random_bits
    client_ip = request.environ.get('REMOTE_ADDR')
    cur.execute("""INSERT INTO users VALUES (?, ?)""", (hash, client_ip))
    cur.execute("""INSERT INTO files VALUES (?, ?)""", (hash, hash_path))
    conn.commit()
    cur.close()
    conn.close()
    preview_html = pypandoc.convert_file(hash_path, 'html')
    with open(f"{preview_path}/{hash}", "w", encoding="utf-8") as f:
        f.write(preview_html)
    response.set_cookie("secret", hash, secret=SECRET)

    redirect("/editor")

    # return "File successfully saved to '{0}'.".format(f"{save_path}/{hash}.org")


@route('/preview')
@view("preview")
def preview():
    try:
        secret = request.get_cookie("secret", secret=SECRET)
        with open(f"{preview_path}/{secret}", "r", encoding="utf-8") as f:
            return dict(
                previewContent=f.read()
            )
    except Exception:
        return dict(
            previewContent="<p>Здесь будет предпросмотр сайта</p>"
        )


@route("/preview_reload", method='POST')
def preview_reload():
    """Обработчик маршрута, который вызывается при изменении содержимого файла пользователем в редакторе"""
    secret = request.get_cookie("secret", secret=SECRET)
    with open(f"{preview_path}/{secret}", "w", encoding="utf-8") as f:
        f.write(pypandoc.convert_text(request.json['data'], 'html', format="org"))
    conn = sqlite3.connect("info.db")
    cur = conn.cursor()
    file = cur.execute("""SELECT file_path FROM files WHERE user_uid = ?""", (secret,)).fetchone()[0]
    with open(f"{file}", "w", encoding="utf-8") as f:
        f.write(request.json['data'])


@route("/preview/<secret>")
@view("preview")
def preview_everyone(secret):
    with open(f"{preview_path}/{secret}", "r", encoding="utf-8") as f:
        return dict(
            previewContent=f.read()
        )


@route("/logout")
def logout():
    supabase.auth.sign_out()
