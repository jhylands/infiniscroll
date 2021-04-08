from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from auth import auth as auth_blueprint
from db.user import User
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

import datetime
import os
import pymysql.cursors
import pymysql

from item_manager import ItemManager

app = Flask(__name__)


@app.route("/")
@login_required
def index():
    """ Route to render the HTML """
    return send_from_directory('../dist', "index.html")


@app.route("/main.js")
def js():
    """ Route to render the HTML """
    return send_from_directory('../dist', "main.js")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../dist', path)


@app.route("/load", methods=['POST'])
@login_required
def load():
    """ Route to return the posts """
    item_manager = ItemManager()
    items = [item.to_jsonable() for item in item_manager.get_items(20)]
    return jsonify(items)


@app.route('/previous_messages/', methods=['POST'])
@login_required
def get_previous_messages_unknown_number():
    number_to_load = 5
    try:
        # https://stackoverflow.com/a/34503728/1320619
        # Connect to the database
        connection = pymysql.connect(host="141.136.33.223",
                                     user='timepcou_site',
                                     password=os.environ["code"],
                                     db='timepcou_devopchallenge',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Create a new record
            sql = "select * from store order by id desc limit %s"
            acc = []
            cursor.execute(sql, (number_to_load))
            for result in cursor.fetchall():
                acc.append(result)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return jsonify(acc)


@app.route('/previous_messages/<int:last_id>', methods=['POST'])
@login_required
def get_previous_messages(last_id):
    number_to_load = 10
    try:
        # https://stackoverflow.com/a/34503728/1320619
        # Connect to the database
        connection = pymysql.connect(host="141.136.33.223",
                                     user='timepcou_site',
                                     password=os.environ["code"],
                                     db='timepcou_devopchallenge',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Create a new record
            sql = "select * from store where id<%s order by id desc limit %s"
            acc = []
            cursor.execute(sql, (last_id, number_to_load))
            for result in cursor.fetchall():
                acc.append(result)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return jsonify(acc)


@app.route('/store_message', methods=['POST'])
@login_required
def store_message():
    message = request.json.get("message")
    now = datetime.datetime.now()
    try:
        # https://stackoverflow.com/a/34503728/1320619
        # Connect to the database
        connection = pymysql.connect(host="141.136.33.223",
                                     user='timepcou_site',
                                     password=os.environ["code"],
                                     db='timepcou_devopchallenge',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `store` (`message`, `timestamp`) VALUES (%s, %s)"
            cursor.execute(sql, (message, now))
            sql = "select * from store order by id desc limit 1"
            cursor.execute(sql, ())
            for result in cursor.fetchall():
                a = jsonify(result)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return a


if __name__ == "__main__":
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://timepcou_site:{}@141.136.33.223/timepcou_devopchallenge?charset=utf8&use_unicode=1'.format(os.environ["code"])

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.run(port=8008, host="0.0.0.0")
