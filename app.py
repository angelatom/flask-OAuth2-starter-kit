'''
Flask starter kit with Requests-OAuthlib library
Example with google login and a get request for google calendar
'''
from flask import Flask, session, redirect, jsonify, request
from requests_oauthlib import OAuth2Session

import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

'''
Info that the API gives you to use
Ex:
client_id = "my_client_id"
client_secret = "my_client_secret"
redirect_uri = "http://localhost:5000/oauth2callback"
auth_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://www.googleapis.com/oauth2/v4/token"
refresh_url = token_url # google has token and refresh url as the same one 
scope = [
    'https://www.googleapis.com/auth/calendar' #specific access given to you 
]
'''
# Fill this these out (some APIs do not require all of these)
client_id = ""
client_secret = ""
redirect_uri = ""
auth_base_url = ""
token_url = ""
refresh_url = ""
scope = [
    ""
]


@app.route('/')
def index():
    return ('<a href="/authorize"> Authorize</a>')

#Step 2: Use token to use API
@app.route('/login')
def login():
    if "credentials" not in session:
        return redirect("authorize") # if credentials (token) is not in session, then redirect to authorize
    any_var_name = OAuth2Session(client_id, token=session["credentials"]) # use this to make API requests
    '''for example: google calendar's get request  
    calendaruser_json = jsonify(any_var_name.get('https://www.googleapis.com/calendar/v3/users/me/calendarList/primary').json())
    '''

# Step 0: Authorize by redirecting user to OAuth provider 
@app.route("/authorize")
def auth():
    theauthmachine = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri) 
    authorization_url, state = theauthmachine.authorization_url(auth_base_url, 
    access_type="offline", include_granted_scopes="true") 
    session["state"] = state
    return redirect(authorization_url)
# Step 0.5: OAuth provider authorizes user and sends back user to callback URL with auth code
# Step 1: Get access token
@app.route("/oauth2callback", methods=["GET"]) 
def callback():
    theauthmachine = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'])
    token = theauthmachine.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    # token is fetched above and set to session below
    session["credentials"] = token 
    return redirect("/login")

# Removes the token from the session
@app.route('/clear')
def clear_credentials():
    if 'credentials' in session:
        del session['credentials']
    return ('Credentials have been cleared.<br><br><a href="/login"> Do Stuff</a>')

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # allows you to use non-secured links (http)
    app.run(debug = True)