from flask import Flask, request, jsonify, send_from_directory, g
from flask_login import LoginManager, login_required, current_user
from auth import auth as auth_blueprint
from db.user import User
from db.db import Session
from responder.main import NewMessageHandler, MessageLoader
from item_manager import ItemManager

app = Flask(__name__)


@app.route("/")
@login_required
def index():
    """ Route to render the HTML """
    return send_from_directory("../dist", "index.html")


@app.route("/main.js")
def js():
    """ Route to render the HTML """
    return send_from_directory("../dist", "main.js")


@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("../dist", path)


@app.route("/load", methods=["POST"])
@login_required
def load():
    """ Route to return the posts """
    item_manager = ItemManager(current_user.id)
    items = [item.to_jsonable() for item in item_manager.get_items(20)]
    return jsonify(items)


@app.route("/whoami/")
@login_required
def whoami():
    return jsonify({"current user": current_user.id})


@app.route("/previous_messages/", methods=["POST"])
@login_required
def get_previous_messages_unknown_number():
    session = g.session
    return jsonify(MessageLoader(session).user_id(current_user.id).load(10).send())


@app.route("/previous_messages/<int:last_id>", methods=["POST"])
@login_required
def get_previous_messages(last_id):
    # init SQLAlchemy so we can use it later in our models
    session = g.session
    return jsonify(
        MessageLoader(session).user_id(current_user.id).last_id(last_id).send()
    )


@app.route("/store_message", methods=["POST"])
@login_required
def store_message():
    # init SQLAlchemy so we can use it later in our models
    session = g.session
    message = request.json.get("message")
    return jsonify(
        NewMessageHandler(message).user_id(current_user.id).session(session).send()
    )


@app.before_request
def attachdb():
    g.session = Session()


@app.teardown_request
def teardown_request(exception):
    g.session.close()
    Session.remove()


@app.after_request
def closedb(request):
    g.session.close()
    Session.remove()
    return request


if __name__ == "__main__":
    app.config["SECRET_KEY"] = "9OLWxND4o83j4K4iuopO"

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        session = g.session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        user = session.query(User).filter(User.id == int(user_id)).one()
        print(user.id)
        return user

    app.register_blueprint(auth_blueprint)
    app.run(port=8008, host="0.0.0.0")
