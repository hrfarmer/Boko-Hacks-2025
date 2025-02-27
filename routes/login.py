from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from models.user import User

login_bp = Blueprint("login", __name__, url_prefix="/api")


@login_bp.route("/auth/status")
def auth_status():
    try:
        print(f"Checking auth status. Is authenticated: {current_user.is_authenticated}")
        is_authenticated = current_user.is_authenticated
        if is_authenticated:
            return jsonify({
                "status": "success",
                "authenticated": True,
                "user": {
                    "username": current_user.username,
                    "id": current_user.id
                }
            })
    except Exception as e:
        print(f"Error in auth_status: {e}")
        
    return jsonify({
        "status": "success",
        "authenticated": False
    })


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return jsonify({"status": "error", "message": "Missing credentials"}), 400

        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                # Set remember=True for persistent session
                login_user(user, remember=True)
                session.permanent = True
                
                # Force session to be saved
                session.modified = True
                
                return jsonify({
                    "status": "success",
                    "user": {
                        "username": user.username,
                        "id": user.id
                    }
                })
            else:
                return jsonify({"status": "error", "message": "Invalid credentials"}), 401
        except Exception as e:
            print(f"Error in login: {e}")
            return jsonify({"status": "error", "message": "Server error"}), 500

    return jsonify({"status": "error", "message": "Method not allowed"}), 405


@login_bp.route("/logout")
@login_required
def logout():
    try:
        # Get the session ID before logout for debugging
        session_id = session.get('_id')
        print(f"Logging out user. Session ID: {session_id}")
        
        # Perform logout
        logout_user()
        
        # Clear all session data
        session.clear()
        
        # Force session modifications to be saved
        session.modified = True
        
        print(f"Logout complete. Is authenticated: {current_user.is_authenticated}")
        return jsonify({"status": "success", "message": "Logged out successfully"})
    except Exception as e:
        print(f"Error in logout: {e}")
        return jsonify({"status": "error", "message": "Logout failed"}), 500
