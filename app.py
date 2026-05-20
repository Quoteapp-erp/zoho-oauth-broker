from flask import (
    Flask,
    request,
    redirect,
    jsonify
)

import requests

app = Flask(__name__)

# ✅ ZOHO CONFIG
CLIENT_ID = "1000.V1YC2SVWK9BHPFSONMS0N4I6CHMEUQ"

CLIENT_SECRET = "84471ba45ec3da0cea301f8e0fb75563a19ab2be83"

REDIRECT_URI = (
    "https://zoho-oauth-broker.onrender.com/oauth/callback"
)

ZOHO_ACCOUNTS_URL = (
    "https://accounts.zoho.in"
)

# ✅ START OAUTH
@app.route("/connect")
def connect():

    connection_id = request.args.get(
        "connection_id"
    )

    oauth_url = (

        f"{ZOHO_ACCOUNTS_URL}/oauth/v2/auth?"

        f"scope=ZohoBooks.fullaccess.all&"

        f"client_id={CLIENT_ID}&"

        f"response_type=code&"

        f"access_type=offline&"

        f"redirect_uri={REDIRECT_URI}&"

        f"state={connection_id}"
    )

    return redirect(oauth_url)

# ✅ CALLBACK
@app.route("/oauth/callback")
def oauth_callback():

    code = request.args.get("code")

    state = request.args.get("state")

    if not code:

        return "Authorization failed"

    token_url = (
        f"{ZOHO_ACCOUNTS_URL}/oauth/v2/token"
    )

    payload = {

        "grant_type":
            "authorization_code",

        "client_id":
            CLIENT_ID,

        "client_secret":
            CLIENT_SECRET,

        "redirect_uri":
            REDIRECT_URI,

        "code":
            code
    }

    response = requests.post(
        token_url,
        data=payload
    )

    token_data = response.json()

    return jsonify({

        "success": True,

        "connection_id":
            state,

        "token_data":
            token_data
    })

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )