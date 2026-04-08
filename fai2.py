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

        try:
            self.base_params = SignerPy.get(params=self.base_params)
        except Exception as e:
            print("SignerPy.get error:", e)

        self.base_params.update({
            'device_type': f'rk{random.randint(3000, 4000)}s_{uuid.uuid4().hex[:4]}',
            'language': 'AR'
        })

        self.headers = {
            'User-Agent': f'com.zhiliaoapp.musically/{self.base_params["manifest_version_code"]} (Linux; Android 10)'
        }

    def variants(self):
        return list(set([
            self.input,
            self.input.lower(),
            self.input.strip()
        ]))

    def try_endpoint(self, endpoint):
        for acct in self.variants():
            for host in self.hosts:

                params = self.base_params.copy()
                ts = int(time.time())

                params['ts'] = ts
                params['_rticket'] = int(ts * 1000)
                params['account_param'] = acct

                try:
                    sig = SignerPy.sign(params=params)
                except Exception:
                    continue

                headers = self.headers.copy()
                headers.update({
                    'x-tt-passport-csrf-token': secrets.token_hex(16),
                    'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
                    'x-ss-stub': sig.get('x-ss-stub', ''),
                    'x-argus': sig.get('x-argus', ''),
                    'x-gorgon': sig.get('x-gorgon', ''),
                    'x-khronos': sig.get('x-khronos', ''),
                    'x-ladon': sig.get('x-ladon', ''),
                })

                url = f"https://{host}{endpoint}"

                try:
                    r = self.session.post(url, params=params, headers=headers, timeout=8)

                    print(f"\n🌐 {host}")
                    print("STATUS:", r.status_code)
                    print("HEADERS:", dict(r.headers))
                    print("BODY:", r.text)

                    j = r.json()

                    accounts = j.get("data", {}).get("accounts", [])
                    if not accounts:
                        continue

                    acc = accounts[0]

                    ticket = acc.get("passport_ticket") or acc.get("not_login_ticket")
                    username = acc.get("username") or acc.get("user_name")

                    if ticket:
                        return {
                            "username": username,
                            "ticket": ticket,
                            "raw": j
                        }

                except Exception:
                    continue

        return None

    def login_with_ticket(self, ticket):
        url = "https://api19-normal-c-alisg.tiktokv.com/passport/user/login_by_passport_ticket/"

        params = {
            "passport_ticket": ticket,
            "_rticket": int(time.time() * 1000),
            "ts": int(time.time()),
            "device_platform": "android",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "version_name": "37.8.5"
        }

        try:
            r = self.session.post(url, params=params, headers=self.headers, timeout=8)

            print("\n🔐 LOGIN STATUS:", r.status_code)
            print("\n🔐 LOGIN HEADERS:\n", dict(r.headers))
            print("\n🔐 LOGIN RESPONSE:\n", r.text)

            try:
                return r.json()
            except:
                return {"raw": r.text}

        except Exception as e:
            print("Login error:", e)
            return None

    def run(self):
        res = self.try_endpoint("/passport/account_lookup/username/")
        if not res:
            res = self.try_endpoint("/passport/account_lookup/email/")

        if not res:
            return {"status": "failed"}

        ticket = res.get("ticket")

        if ticket:
            login_res = self.login_with_ticket(ticket)

            return {
                "status": "success",
                "lookup": res,
                "login": login_res
            }

        return {"status": "failed"}


if __name__ == "__main__":
    inp = input("Enter (username/email): ")

    engine = UltraTikTok(inp)
    result = engine.run()

    print("\n💣 FINAL RESULT:\n")
    print(result)
