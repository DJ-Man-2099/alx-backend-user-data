#!/usr/bin/env python3
""" flask Module """

from flask import Flask, jsonify, request, abort ,redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

AUTH = Auth()
app = Flask(__name__)
app.debug = True


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """ Home endpoint """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register() -> str:
    """ Register user """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """ create a new session for the user,
    store it the session ID as a cookie with key "session_id"
    on the response and return a JSON payload of the form """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status. """
    try:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect("/")
    except NoResultFound:
        return jsonify({}), 403



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
