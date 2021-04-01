from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
import random
# Source https://pythonise.com/categories/javascript/infinite-lazy-loading

import datetime
import os
import pymysql.cursors
import pymysql

app = Flask(__name__)

heading = "Lorem ipsum dolor sit amet."

content = """
Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
Repellat inventore assumenda laboriosam, 
obcaecati saepe pariatur atque est? Quam, molestias nisi.
"""

db = list()  # The mock database

posts = 500  # num posts to generate

quantity = 20  # num posts to return per request

for x in range(posts):

    """
    Creates messages/posts by shuffling the heading & content 
    to create random strings & appends to the db
    """

    heading_parts = heading.split(" ")
    random.shuffle(heading_parts)

    content_parts = content.split(" ")
    random.shuffle(content_parts)

    db.append([x, " ".join(heading_parts), " ".join(content_parts)])


@app.route("/")
def index():
    """ Route to render the HTML """
    return render_template("index.html")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('templates/js', path)



@app.route("/load")
def load():
    """ Route to return the posts """
    if request.args:
        counter = int(request.args.get("c"))  # The 'counter' value sent in the QS

        if counter == 0:
            print("Returning posts 0 to {quantity}".format(quantity=quantity))
            # Slice 0 -> quantity from the db
            res = make_response(jsonify(db[0: quantity]), 200)

        elif counter == posts:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print("Returning posts {} to {}".format(counter, counter + quantity))
            # Slice counter -> quantity from the db
            res = make_response(jsonify(db[counter: counter + quantity]), 200)
    return res

@app.route('/last/<int:k>', methods=['GET'])
def last_k_entries(k):
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
            cursor.execute(sql, (k,))
            for result in cursor.fetchall():
                acc.append(result)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return jsonify(acc)


@app.route('/store', methods=['POST'])
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
