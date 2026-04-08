import requests
import time
import uuid
import random
import secrets
import SignerPy

class TikTokFlow:
    def __init__(self, username):
        self.username = username.strip()
        self.session = requests.Session()

        self.hosts = [
            "api19-normal-c-alisg.tiktokv.com",
            "api22-normal-c-alisg.tiktokv.com",
            "api31-normal-alisg.tiktokv.com"
        ]

        self.params = {
            'device_platform': 'android',
            'ssmix': 'a',
            'channel': 'googleplay',
            'aid': '1233',
            'app_name': 'musical_ly',
            'version_code': '370805',
            'version_name': '37.8.5',
            'manifest_version_code': '2023708050',
            'update_version_code': '2023708050',
            'ab_version': '37.8.5',
            'os_version': '10',
            'device_type': f'rk{random.randint(3000,4000)}',
            'device_id': str(random.randint(10**18, 10**19-1)),
            'iid': str(random.randint(10**18, 10**19-1)),
            'openudid': secrets.token_hex(8),
            'resolution': '1600*900',
            'dpi': '240',
            'language': 'ar',
            'os_api': '29',
            'ac': 'wifi',
            'timezone_name': 'Asia/Riyadh',
            'carrier_region': 'SA',
            'sys_region': 'SA',
            'region': 'SA',
            'app_language': 'ar',
            'timezone_offset': '10800',
            'request_tag_from': 'h5',
            'account_param': self.username,
            'scene': '4',
            'mix_mode': '1'
        }

        self.headers = {
            'User-Agent': f'com.zhiliaoapp.musically/{self.params["manifest_version_code"]} (Linux; Android 10)'
        }

    # ============================================
    # 1. Lookup Username
    # ============================================
    def get_ticket(self):
        for host in self.hosts:
            params = self.params.copy()

            ts = int(time.time())
            params['ts'] = ts
            params['_rticket'] = int(ts * 1000)

            try:
                sig = SignerPy.sign(params=params)
            except Exception as e:
                print("Signer error:", e)
                continue

            headers = self.headers.copy()
            headers.update({
                'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
                'x-ss-stub': sig.get('x-ss-stub', ''),
                'x-argus': sig.get('x-argus', ''),
                'x-gorgon': sig.get('x-gorgon', ''),
                'x-khronos': sig.get('x-khronos', ''),
                'x-ladon': sig.get('x-ladon', ''),
                'x-tt-passport-csrf-token': secrets.token_hex(16),
            })

            url = f"https://{host}/passport/account_lookup/username/"

            try:
                r = self.session.post(url, params=params, headers=headers, timeout=10)
                j = r.json()

                print(f"[LOOKUP {host}] ->", j)

                accounts = j.get("data", {}).get("accounts", [])
                if not accounts:
                    continue

                acc = accounts[0]
                ticket = acc.get("passport_ticket") or acc.get("not_login_ticket")
                username = acc.get("username") or acc.get("user_name")

                if ticket:
                    return ticket, username

            except Exception as e:
                print("Lookup error:", e)
                continue

        return None, None

    # ============================================
    # 2. Login باستخدام التكت
    # ============================================
    def login_with_ticket(self, ticket):
        for host in self.hosts:
            params = self.params.copy()

            ts = int(time.time())
            params['ts'] = ts
            params['_rticket'] = int(ts * 1000)

            params.pop("account_param", None)
            params['passport_ticket'] = ticket

            try:
                sig = SignerPy.sign(params=params)
            except Exception as e:
                print("Signer error login:", e)
                continue

            headers = self.headers.copy()
            headers.update({
                'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
                'x-ss-stub': sig.get('x-ss-stub', ''),
                'x-argus': sig.get('x-argus', ''),
                'x-gorgon': sig.get('x-gorgon', ''),
                'x-khronos': sig.get('x-khronos', ''),
                'x-ladon': sig.get('x-ladon', ''),
            })

            url = f"https://{host}/passport/user/login_by_passport_ticket/"

            try:
                r = self.session.post(url, params=params, headers=headers, timeout=10)
                j = r.json()

                print(f"[LOGIN {host}] ->", j)

                if j.get("message") == "success":
                    return j

            except Exception as e:
                print("Login error:", e)
                continue

        return None


# ============================================
# تشغيل
# ============================================
if __name__ == "__main__":
    user = input("Enter username: ")

    flow = TikTokFlow(user)

    ticket, username = flow.get_ticket()

    if not ticket:
        print("❌ ما حصلنا passport_ticket")
        exit()

    print("✅ Ticket:", ticket)

    login = flow.login_with_ticket(ticket)

    if login:
        print("\n🔥 LOGIN SUCCESS")
        print(login)
    else:
        print("❌ Login failed")
