from flask import Flask, request, jsonify, session, make_response
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session
from config import ApplicationConfig
from models import db, User

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "username": user.username
    })


@app.route("/lesson", methods=["POST"])
def promt_for_story():
    promt_for_story = request.json

    if not promt_for_story or promt_for_story == {}:
        return jsonify({"error ": "Данные не отправленны"}), 401

    #a = get_skazka(prompt_for_story)
    #b = get_zazka(prompt_for_story)
    #quickcommand(a)

    return jsonify({
        "promt_for_story": promt_for_story #b
    })

# Пользователь отправляет код доступа получает главный json
@app.route("/story", methods=["POST"])
def story_from_ai():
    code = request.json['code']

    if not code: #len(quickcommand.selectstory())!=0
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "": story_from_ai
    })


@app.route("/result", methods=["GET"])
def result():
    result = request.json["result"]

    if not promt_for_story:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=result).first()
    return jsonify({
        "result": result
    })



def register_user():
    data = request.get_json()
    story_from_AI = data["promt_for_story"]


@app.route("/register", methods=["POST"])
def register_user():
    username = request.json["username"]
    password = request.json["password"]

    user_exists = User.query.filter_by(username=username).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "username": new_user.username
    })


@app.route("/login", methods=["POST"])
def login_user():
    print(request.json)
    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    resp = jsonify({
        "id": user.id,
        "username": user.username
    })

    # resp.set_cookie("session", user.id, samesite=None, httponly=True)
    return resp


@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


if __name__ == "__main__":
    app.run(debug=True)
