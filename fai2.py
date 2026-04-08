import requests
import time
import uuid
import random
import secrets


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
            'User-Agent': f'com.zhiliaoapp.musically/{self.base_params["manifest_version_code"]} (Linux; Android 10)'
        }

    def variants(self):
        return list(set([
            self.input,
            self.input.lower(),
            self.input.strip()
        ]))

    def request(self, url, params=None, data=None):
        try:
            res = self.session.post(url, params=params, data=data, headers=self.headers, timeout=8)
            return res.json()
        except:
            return None

    def try_lookup(self, endpoint):
        for acct in self.variants():
            for host in self.hosts:

                url = f"https://{host}{endpoint}"

                params = self.base_params.copy()
                params.update({
                    "account_param": acct,
                    "_rticket": int(time.time() * 1000),
                    "ts": int(time.time())
                })

                res = self.request(url, params=params)

                if not res:
                    continue

                print(f"[{host}] -> {res}")

                accounts = res.get("data", {}).get("accounts", [])
                if not accounts:
                    continue

                acc = accounts[0]

                ticket = acc.get("passport_ticket") or acc.get("not_login_ticket")
                username = acc.get("username") or acc.get("user_name")

                if ticket:
                    return {
                        "username": username,
                        "ticket": ticket,
                        "raw": res
                    }

        return None

    def login_by_ticket(self, ticket):
        url = "https://api19-normal-c-alisg.tiktokv.com/passport/user/login_by_passport_ticket/"

        params = self.base_params.copy()
        params.update({
            "passport_ticket": ticket,
            "_rticket": int(time.time() * 1000),
            "ts": int(time.time())
        })

        try:
            res = self.session.post(url, params=params, headers=self.headers, timeout=8)
            return res.json()
        except Exception as e:
            return {"error": str(e)}

    def run(self):
        res = self.try_lookup("/passport/account_lookup/username/")
        if not res:
            res = self.try_lookup("/passport/account_lookup/email/")

        if not res:
            return {"status": "failed"}

        ticket = res.get("ticket")

        if ticket:
            login_res = self.login_by_ticket(ticket)

            return {
                "status": "success",
                "username": res.get("username"),
                "ticket": ticket,
                "login_response": login_res
            }

        return {"status": "failed"}


if __name__ == "__main__":
    inp = input("Enter (username/email): ")

    engine = UltraTikTok(inp)
    result = engine.run()

    print("\nFINAL RESULT:\n")
    print(result)
