from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_socketio import SocketIO, emit

import json

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test_user:sadmin@192.168.7.182:5432/test_db"
db = SQLAlchemy(app)
socketio = SocketIO(app, coors_allowed_origins='*')  # для безопасности нужно типо
migrate = Migrate(app, db)


class Article(db.Model):  # для бд создание ячеек
    __tablename__ = 'articles'  # название таблицы зарезервированное слово походу

    # Для миграции устанавливается пакет Flask-Migrate
    # Созданипе бд в таблице и создание папки для миграций (в консоли питона писать)
    # $ flask db init
    # $ flask db migrate
    # $ flask db upgrade Команда flask db upgrade выполняет миграцию и создает нашу таблицу:
    # sqlalchemy_db_upgrade В случае, если мы добавляем, удаляем или
    # изменяем какие - либостолбцы, мы всегда можем выполнить команды migrate и
    # upgrade, чтобы отразить эти изменения и в нашей базе данных.

    # названия в таблицу походу берутся от названия преременных
    # статься где всё вычитал:
    # https://stackabuse.com/using sqlalchemy-with-flask-and-postgresql/

    id = db.Column(db.Integer, primary_key=True)  # уникальный индекс
    text = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(100), nullable=False)  # ullable нельзя установить нулевое значение
    intro = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime,
                     default=datetime.utcnow)
    # установка времени по умолчанию с даты создания штамп или полноценная дата ?

    def __init__(self, text, title, intro):
        self.text = text
        self.title = title
        self.intro = intro

    """С помощью этого метода будет выдаваться сам объект и его ID при обращении на основе объекта класса
    Нужно что бы получать саму запись из БД

    Из комментов:
    _repr_ ты описал немного неправильно. 
    он  в данном случае дает возможность вывести объект в том виде как ты хочешь. 
    но не выводит сам объект и атрибуты с параметрами. для начинающих - это то, что увидишь если сделать print(article)

    """

    def __repr__(self):
        return '<Article %r>' % self.id


class LoginForm(FlaskForm):
    username = StringField('u_nickname', validators=[DataRequired()])
    password = PasswordField('u_pass', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/')
@app.route('/home')
def index():

    from engine_scripts.py.sql.sql_engine import csql_eng as sql
    csql = sql()
    csql.set_default_connect_data()
    handle_one = csql.sql_connect("Europe/Moscow")

    csql.sql_query_and_get_result(handle_one, "SELECT * FROM articles WHERE id > 1", mode="_1")
    # print(result)

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/get-articles')
def garticles():
    art_unit = Article.query.order_by(Article.id.desc()).all()  # запросить всё из таблицы и отсортировать по индексу
    # results = [
    #     {
    #         "post_date": art_unit.date,
    #         "intro": art_unit.intro,
    #         "title": art_unit.title,
    #         "text": art_unit.text
    #     } можем ли мы словарь передать ?
    # ]

    return render_template('get-articles.html', articles=art_unit)


@app.route('/get-articles/<int:pid>')
def art_detail(pid):
    art_unit = Article.query.get(pid)
    return render_template('post-detail.html', article=art_unit)


@app.route('/get-articles/<int:pid>/del')
def art_del(pid):
    art_unit = Article.query.get_or_404(pid)
    try:
        db.session.delete(art_unit)
        db.session.commit()
        return redirect("/get-articles")

    except Exception as err:
        return f"При удалении статьи произошла ошибка {err}"


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        # получаем данные от кнопок и полей
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(text=text, title=title, intro=intro)

        try:
            db.session.add(article)
            db.session.commit()

            return redirect('/get-articles')
        except Exception as err:
            return "Error" + str(err)

    else:  # Иначе метод Get
        pass

    return render_template('create-article.html')


@app.route('/get-articles/<int:pid>/update', methods=['POST', 'GET'])
def update_article(pid):
    art_unit = Article.query.get_or_404(pid)
    if request.method == 'POST':

        art_unit.title = request.form['title']
        art_unit.intro = request.form['intro']
        art_unit.text = request.form['text']

        try:
            db.session.commit()
            return redirect("/get-articles")
        except Exception as err:
            return f"При редактировании статьи произошла ошибка {err}"
    return render_template('create-article.html')


@app.route('/user/<string:name>/<int:uid>')
def user(name=str, uid=int):
    return "User Page Name: " + str(name) + " ID:" + str(uid)


@app.route('/user/login/')
def user_login():
    return render_template('ulogin.html')


@app.errorhandler(404)
def page_not_found(error_str):

    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)
