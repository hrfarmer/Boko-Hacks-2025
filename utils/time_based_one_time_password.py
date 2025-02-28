
import duo_universal

# Download the helper library from https://www.twilio.com/docs/python/install
import os
import dotenv

dotenv.load_dotenv()
import os

client_id = "DIXMG6WOX6PVM0ACQ5SK"
client_secret="UnHVYccJdNhkHUVbBUz6kd2HcHH0n2wq9O0BHEIV"
api_hostname="api-c31233b9.duosecurity.com"


redirect_uri ="https://www.espn.com"
duo_client = duo_universal.Client(client_id, client_secret, api_hostname, redirect_uri)

try:
  duo_client.health_check()
except duo_client.DuoException:
    pass
    print("dsuafsjis")
  # Either allow login without 2FA, or abort the login proces
  
state = duo_client.generate_state()
flask.session[‘state’] = state

prompt_uri = duo_client.create_auth_url(username, state)