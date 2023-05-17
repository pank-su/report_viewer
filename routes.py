"""
Routes and views for the bottle application.
"""
import os
import shutil
from datetime import datetime

import pypandoc
import storage3.utils
from bottle import route, view, request, response, FileUpload, BaseRequest, redirect, HTTPResponse, LocalRequest
from supabase import create_client, Client
from phone_check import validate_phone_number

BaseRequest.MEMFILE_MAX = 1024 * 1024  # ограничение по памяти

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# переменная, содержащая секретный ключ, используемый для защиты куков
SECRET = os.environ.get("SECRET_TOKEN")
# это переменная, содержащая путь к директории, в которой будут храниться файлы превью
savable_path = "./save/"
temporary_path = "./temp/"


def check_path(path: str) -> None:
    """Функция, которая проверяет есть ли путь, если нет, то создаёт его"""
    if not os.path.exists(path):
        os.makedirs(path)


check_path(savable_path)


def check_auth(request: LocalRequest) -> str:
    query = request.query
    user_id = None
    if request.query_string != "" and "error" not in request.query_string:
        try:
            supabase.auth.refresh_session(query["refresh_token"])
            user_id = supabase.auth.get_user().user.id
            return user_id
        except Exception as e:
            pass
        try:
            supabase.auth.set_session(query["access_token"])
            user_id = supabase.auth.get_user().user.id
            return user_id
        except Exception as e:
            pass
    elif user_id is None:
        try:
            user_id = request.get_cookie("user_id", secret=SECRET)
            return user_id
        except Exception as e:
            pass
    return user_id


@route('/')
@route('/editor')
@view('editor')
def editor():
    user_id = check_auth(request)

    if user_id is not None:
        response.set_cookie("user_id", user_id, secret=SECRET)
        try:
            supabase.storage.create_bucket(user_id)
        except storage3.utils.StorageException:
            pass
        storage = supabase.storage.get_bucket(user_id)
        if len(storage.list()) == 0:
            storage.upload("test.org", "./tested_file/test.org")
        return dict(
            year=datetime.now().year,
            userExist=True,
            files=storage.list(),
            user_id=user_id
        )
    else:
        return dict(
            year=datetime.now().year,
            userExist=False,
            files=[],
            user_id=""
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
def do_upload():
    """Обработчик маршрута, которая обрабатывает POST-запрос на загрузку файла. Она сохраняет загружxенный файл во
    временную директорию, конвертирует его в формат org с помощью pypandoc, генерирует случайный хэш-код и сохраняет
    конвертированный файл с использованием этого хэш-кода в постоянную директорию"""
    upload: FileUpload = request.files.get('file')
    check_path(temporary_path)
    upload.save(temporary_path + upload.filename)
    org_text = pypandoc.convert_file(temporary_path + upload.filename, 'org')
    user_id = request.get_cookie("user_id", SECRET)
    save_path = savable_path + user_id + "/"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = ".".join(upload.filename.split('.')[:-1]) + ".org"
    new_filename = filename
    with open(savable_path + user_id + "/" + filename, "w", encoding="utf-8") as f:
        f.write(org_text)
    shutil.rmtree(temporary_path)
    is_sent = False
    file_id = 0
    while not is_sent:
        try:
            supabase.storage.get_bucket(user_id).upload(new_filename, savable_path + user_id + "/" + filename)
            is_sent = True
        except storage3.utils.StorageException:
            file_id += 1
            new_filename = ".".join(upload.filename.split('.')[:-1]) + f"_{file_id}.org"
    return "ok"


def generate_preview(user_id, filename):
    """Функция, которая генерирует превью"""
    save_path = savable_path + user_id + "/"
    check_path(save_path)
    with open(save_path + filename, "wb") as f:
        res = supabase.storage.from_(user_id).download(filename)
        f.write(res)
    html_text = "С файлом что-то не так"
    try:
        html_text = pypandoc.convert_file(save_path + filename, 'html')
    except RuntimeError:
        """Если файл не текст"""
        url = supabase.storage.from_(user_id).get_public_url(filename)
        html_text = f"<img src='{url}' />"
    return html_text


@route("/preview")
@view("preview")
def preview():
    return dict(
        previewContent="<p>Site preview here</p>"
    )


@route('/preview/<filename>')
@view("preview")
def preview(filename):
    user_id = request.get_cookie("user_id", secret=SECRET)
    return dict(previewContent=generate_preview(user_id, filename))


@route('/s/<user_id>/<filename>')
@view("preview")
def preview(user_id, filename):
    return dict(previewContent=generate_preview(user_id, filename))


@route("/preview_reload", method='POST')
def preview_reload():
    """Обработчик маршрута, который вызывается при изменении содержимого файла пользователем в редакторе"""
    filename = request.json["filename"]
    data = request.json["data"]
    print(data)
    user_id = request.get_cookie("user_id", secret=SECRET)
    supabase.storage.from_(user_id).remove(filename)
    check_path(temporary_path)
    with open(temporary_path + filename, "w", encoding="utf-8") as f:
        f.write(data)
    supabase.storage.from_(user_id).upload(filename, temporary_path + filename)

    # shutil.rmtree(temporary_path)
    return "ok"


@route("/content/<filename>")
def get_content(filename: str):
    """Сохраняет файл в директории save_path и возвращает значение"""
    if filename.endswith((".png", ".jpg")):
        return HTTPResponse(status=400, body="This is not text")
    user_id = request.get_cookie("user_id", SECRET)
    save_path = savable_path + user_id + "/"
    check_path(save_path)
    if user_id is None:
        return None

    with open(save_path + filename, "wb") as f:
        res = supabase.storage.from_(user_id).download(filename)
        f.write(res)
    try:
        with open(save_path + filename, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        return HTTPResponse(status=400, body="This is not text")


@route('/orders')
@view("orders")
def orders():
    """Отображает экран с заказами"""
    error = ""
    try:
        error = request.query.error
    except KeyError:
        pass

    # Проверка авторизации
    user_id = check_auth(request)

    orders_ = supabase.table("orders").select("*").execute().data
    for i in range(len(orders_)):
        # Берём аватарки пользователей
        orders_[i]['user_image'] = supabase.auth.admin.get_user_by_id(orders_[i]["creator"]).user.user_metadata[
            'avatar_url']
        # Также заменям аватарки у картинок заказов если их нет
        if orders_[i]['image_path'] is None:
            orders_[i]['image_path'] = 'https://media.istockphoto.com/id/1281804798/photo/very-closeup-view-of' \
                                       '-amazing-domestic-pet-in-mirror-round-fashion-sunglasses-is-isolated-on.jpg?b' \
                                       '=1&s=170667a&w=0&k=20&c=4CLWHzcFeku9olx0np2htie2cOdxWamO-6lJc-Co8Vc='

    return {
        "title": "Заказы",
        "userExist": user_id is not None,
        "orders": orders_,
        "error": error
    }


@route("/submit_order", method='POST')
def submit_order():
    """Функция для добавления новго заказа"""
    upload: FileUpload = request.files.get('order_image')
    phone: str = request.forms.get('order_phone')
    user_id = request.get_cookie("user_id", SECRET)
    date: str = request.forms.get('order_due_date')
    description: str = request.forms.get('order_description')
    name: str = request.forms.get('order_description')
    price: str = request.forms.get('order_price')
    # пользователь авторизован
    if user_id is None:
        return redirect("/orders?error=Вы не авторизованы")
    # пустые поля
    if phone.strip() == '' or date.strip() == '' or description.strip() == "" or name.strip() == "" or price.strip() == "":
        return redirect("/orders?error=Не все поля заполнены")
    # проверка цены
    if int(price) < 0:
        return redirect("/orders?error=Цена меньше 0")
    # проверка даты
    if datetime.strptime(date, "%Y-%m-%d") < datetime.now():
        return redirect("/orders?error=Мы не можем выполнить заказ в прошлом, установить дату в будующем")
    # телефон некорректный
    if not validate_phone_number(phone):
        return redirect("/orders?error=Формат ввода телефона не является корректным")
    # отправка картинки на сервер
    check_path(temporary_path)
    upload.save(temporary_path + upload.filename)
    is_sent = False
    new_filename = upload.filename
    file_id = 0
    image_url = ""
    while not is_sent:
        try:
            supabase.storage.get_bucket("images").upload(new_filename, temporary_path + upload.filename)
            image_url = supabase.storage.from_("images").get_public_url(new_filename)
            is_sent = True
        except storage3.utils.StorageException:
            file_id += 1
            new_filename = ".".join(upload.filename.split('.')[:-1]) + f"_{file_id}." + upload.filename.split('.')[-1]
    # удаление временной папки
    shutil.rmtree(temporary_path)

    # добавление новой записи в таблицу с заказами
    supabase.table("orders").insert({"name": name, "description": description, "date_complete": date, "creator": user_id,
         "price": price, "image_path": str(image_url)}).execute()
    return redirect('/orders')


@route("/logout")
def logout():
    supabase.auth.sign_out()
    response.set_cookie("user_id", "")
    redirect("/")
