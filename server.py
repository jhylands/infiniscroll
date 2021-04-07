from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
# Source https://pythonise.com/categories/javascript/infinite-lazy-loading

import datetime
import os
import pymysql.cursors
import pymysql

app = Flask(__name__)


@app.route("/")
def index():
    """ Route to render the HTML """
    return send_from_directory('dist', "index.html")


@app.route("/main.js")
def js():
    """ Route to render the HTML """
    return send_from_directory('dist', "main.js")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


@app.route("/load", methods=['POST'])
def load():
    """ Route to return the posts """
    return jsonify([{"title": "This is a title", "content": "This is some content."} for i in range(20)])


@app.route('/previous_messages/', methods=['POST'])
def get_previous_messages_unknown_number():
    number_to_load = 20
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
                acc.reverse()

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return jsonify(acc)


@app.route('/previous_messages/<int:last_id>', methods=['POST'])
def get_previous_messages(last_id):
    number_to_load = 20
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
            sql = "select * from store where id>%s order by id desc limit %s"
            acc = []
            cursor.execute(sql, (last_id, number_to_load))
            for result in cursor.fetchall():
                acc.append(result)
            acc.reverse()

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return jsonify(acc)


@app.route('/store_message', methods=['POST'])
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

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return jsonify({})


if __name__ == "__main__":
    app.run(port=8008, host="0.0.0.0")
