from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from flask_login import LoginManager, login_required, current_user
from sqlalchemy import desc
from auth import auth as auth_blueprint
from db.user import User
from db.message import Message
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import datetime
import os

from item_manager import ItemManager
engine = create_engine('mysql://timepcou_site:{}@141.136.33.223/timepcou_devopchallenge?charset=utf8&use_unicode=1'.format(os.environ["code"]))
Session = scoped_session( sessionmaker(bind=engine) )

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

@app.route('/whoami/')
@login_required
def whoami():
    return jsonify({"current user": current_user.id})

@app.route('/previous_messages/', methods=['POST'])
@login_required
def get_previous_messages_unknown_number():
    with Session() as session:
        number_to_load = 5
        messages = (
            session
            .query(Message)
            .filter(Message.user_id == current_user.id)
            .order_by(desc(Message.id))
            .limit(number_to_load)
            .all())
        acc = [{"id": message.id, "message": message.message} for message in messages]
        return jsonify(acc)


@app.route('/previous_messages/<int:last_id>', methods=['POST'])
@login_required
def get_previous_messages(last_id):
    # init SQLAlchemy so we can use it later in our models
    with Session() as session:
        number_to_load = 10
        messages = (
            session
            .query(Message)
            .filter(Message.user_id == current_user.id)
            .filter(Message.id < last_id)
            .order_by(desc(Message.id))
            .limit(number_to_load)
            .all())
        acc = [{"id": message.id, "message": message.message} for message in messages]
        return jsonify(acc)


@app.route('/store_message', methods=['POST'])
@login_required
def store_message():
    # init SQLAlchemy so we can use it later in our models
    with Session() as session:
        message = request.json.get("message")
        now = datetime.datetime.now()
        new_message = Message(
            user_id=current_user.id,
            message=message,
            timestamp=now)
        session.add(new_message)
        session.commit()
        return jsonify({"message": message, "id": new_message.id})


if __name__ == "__main__":
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with Session() as session:
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return session.query(User).get(int(user_id))

    app.register_blueprint(auth_blueprint)
    app.run(port=8008, host="0.0.0.0")
