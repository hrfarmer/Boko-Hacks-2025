from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models.user import User
from extensions import db

callback_bp = Blueprint("callback", __name__)

@callback_bp.route("/duo-callback")
def duo_callback():
   state = request.args.get('state')
   code = request.args.get('duo_code')
   
   
   if state != flask.session['state']:
       #abot login
       
    try:
        decoded_token = duo_client.exchange_authorization_code_for_2fa_result(code, username)
    except DuoException as e:
        pass
  # Handle authentication failure.
# User successfully passed Duo authentication.