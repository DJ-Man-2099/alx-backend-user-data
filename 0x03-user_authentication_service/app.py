#!/usr/bin/env python3
""" flask Module """

from flask import Flask, jsonify, request, abort, redirect
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
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ The request is expected to contain a session_id cookie.
    Use it to find the user.
    If the user exist, respond with a 200 HTTP status
    and the following JSON payload: {"email": "<user email>"}
    If the session ID is invalid
    or the user does not exist,
    respond with a 403 HTTP status. """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ The request is expected to contain form data with the "email" field.
    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status
    and the following JSON payload:
    {"email": "<user email>", "reset_token": "<reset token>"} """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """ The request is expected to contain form data
    with fields "email", "reset_token" and "new_password".
    Update the password.
    If the token is invalid,
    catch the exception and respond with a 403 HTTP code.
    If the token is valid, respond with a 200 HTTP code
    and the following JSON payload:
    {"email": "<user email>", "message": "Password updated"} """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
