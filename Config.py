import time
import requests

CLIENT_ID = "8podfeops91wqk1a909qdbq1ywe1cv"
CLIENT_SECRET = "cnj6qxsru8fegyw1knc7whaj8kaa0l"
CHANNEL = "THeLeVYNeSS"
AWTRIX_IP = "192.168.0.101"   # az óra IP-címe
INTERVAL = 120               # másodperc két lekérdezés között


def get_token():
    r = requests.post("https://id.twitch.tv/oauth2/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }, timeout=10)
    r.raise_for_status()
    return r.json()["access_token"]


def helix(path, token, **params):
    r = requests.get(
        f"https://api.twitch.tv/helix/{path}",
        params=params,
        headers={"Client-Id": CLIENT_ID, "Authorization": f"Bearer {token}"},
        timeout=10,
    )
    if r.status_code == 401:
        raise PermissionError
    r.raise_for_status()
    return r.json()


token = get_token()
user_id = helix("users", token, login=CHANNEL)["data"][0]["id"]

while True:
    try:
        total = helix("channels/followers", token,
                      broadcaster_id=user_id, first=1)["total"]
        requests.post(
            f"http://{AWTRIX_IP}/api/custom?name=twitch",
            json={
                "text": str(total),
                "icon": "twitch",          # lásd lent
                "color": [145, 70, 255],
                "lifetime": 600,
            },
            timeout=10,
        )
    except PermissionError:
        token = get_token()                # lejárt a token, kérünk újat
        continue
    except Exception as e:
        print("Hiba:", e)
    time.sleep(INTERVAL)