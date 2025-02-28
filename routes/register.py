from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)

from extensions import db
from models.user import User

register_bp = Blueprint("register", __name__, url_prefix="/api")

@register_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    captcha_response = request.form.get("captcha")
    stored_captcha = session.get("captcha_text")

    if not stored_captcha or captcha_response.upper() != stored_captcha:
        return jsonify({
            "success": False,
            "message": "Invalid CAPTCHA. Please try again."
        })

    session.pop("captcha_text", None)

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "Username already exists. Please choose a different one."
        })

    new_user = User(username=username)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": "Registration successful! You can now log in."
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "An error occurred during registration. Please try again."
        })

