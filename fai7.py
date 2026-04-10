import requests
import time
import SignerPy


class TikTokAPI:
    def __init__(self):
        self.session = requests.Session()
        self.host = "api19-normal-c-alisg.tiktokv.com"

        self.params = {
            'device_platform': 'android',
            'ssmix': 'a',
            'channel': 'googleplay',
            'aid': '1233',
            'app_name': 'musical_ly',
            'version_code': '360505',
            'version_name': '36.5.5',
            'manifest_version_code': '2023605050',
            'update_version_code': '2023605050',
            'ab_version': '36.5.5',
            'os_version': '10',
            "device_id": 0,
            'app_version': '30.1.2',
            "request_from": "profile_card_v2",
            "request_from_scene": '1',
            "scene": "1",
            "mix_mode": "1",
            "os_api": "34",
            "ac": "wifi",
            "request_tag_from": "h5",
        }

    # =========================
    # LOOKUP
    # =========================
    def lookup(self, username):
        ts = int(time.time())

        params = self.params.copy()
        params.update({
            "account_param": username,
            "_rticket": int(ts * 1000),
            "ts": ts
        })

        headers = {
            "User-Agent": "com.zhiliaoapp.musically/36.5.5",
        }

        sig = SignerPy.sign(params=params)
        headers.update(sig)

        url = f"https://{self.host}/passport/account_lookup/username/"
        r = self.session.post(url, params=params, headers=headers)

        print("\n[LOOKUP]")
        print("STATUS:", r.status_code)
        print("HEADERS:", dict(r.headers))
        print("BODY:", r.text)

        try:
            return r.json()["data"]["accounts"][0]["passport_ticket"]
        except:
            return None

    # =========================
    # LOGIN (NO username)
    # =========================
    def login(self, ticket):
        ts = int(time.time())

        params = self.params.copy()
        params.update({
            "passport_ticket": ticket,
            "ts": ts,
            "_rticket": int(ts * 1000)
        })

        headers = {
            "User-Agent": "com.zhiliaoapp.musically/36.5.5",
        }

        sig = SignerPy.sign(params=params)
        headers.update(sig)

        url = f"https://{self.host}/passport/user/login_by_passport_ticket/"
        r = self.session.post(url, params=params, headers=headers)

        print("\n[LOGIN]")
        print("STATUS:", r.status_code)
        print("HEADERS:", dict(r.headers))
        print("BODY:", r.text)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    user = input("username: ")

    api = TikTokAPI()

    ticket = api.lookup(user)

    if not ticket:
        print("❌ فشل lookup")
        exit()

    print("✅ ticket:", ticket)

    api.login(ticket)
