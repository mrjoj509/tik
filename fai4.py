import requests
import time
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
            "api31-normal-alisg.tiktokv.com",

            "api16-core-aion-useast5.us.tiktokv.com",
            "api16-core-apix-quic.tiktokv.com",
            "api16-core-apix.tiktokv.com",
            "api16-core-baseline.tiktokv.com",
            "api16-core-c-alisg.tiktokv.com",
            "api16-core-c-useast1a.tiktokv.com",
            "api16-core-quic.tiktokv.com",
            "api16-core-useast5.us.tiktokv.com",
            "api16-core-useast8.us.tiktokv.com",
            "api16-core-va.tiktokv.com",
            "api16-core-ycru.tiktokv.com",
            "api16-core-zr.tiktokv.com",
            "api16-core.tiktokv.com",
            "api16-core.ttapis.com",

            "api16-normal-aion-useast5.us.tiktokv.com",
            "api16-normal-apix-quic.tiktokv.com",
            "api16-normal-apix.tiktokv.com",
            "api16-normal-baseline.tiktokv.com",
            "api16-normal-c-alisg.tiktokv.com",
            "api16-normal-c-useast1a.tiktokv.com",
            "api16-normal-c-useast1a.musical.ly",
            "api16-normal-no1a.tiktokv.eu",
            "api16-normal-quic.tiktokv.com",
            "api16-normal-useast5.tiktokv.us",
            "api16-normal-useast5.us.tiktokv.com",
            "api16-normal-useast8.us.tiktokv.com",
            "api16-normal-va.tiktokv.com",
            "api16-normal-vpc2-useast5.us.tiktokv.com",
            "api16-normal-zr.tiktokv.com",
            "api16-normal.tiktokv.com",
            "api16-normal.ttapis.com",

            "api19-core-c-alisg.tiktokv.com",
            "api19-core-c-useast1a.tiktokv.com",
            "api19-core-useast5.us.tiktokv.com",
            "api19-core-va.tiktokv.com",
            "api19-core-zr.tiktokv.com",
            "api19-core.tiktokv.com",

            "api19-normal-c-useast1a.musical.ly",
            "api19-normal-c-useast1a.tiktokv.com",
            "api19-normal-useast5.us.tiktokv.com",
            "api19-normal-va.tiktokv.com",
            "api19-normal-zr.tiktokv.com",
            "api19-normal.tiktokv.com",

            "api2-19-h2.musical.ly",
            "api2.musical.ly",

            "api21-core-c-alisg.tiktokv.com",
            "api21-core-va.tiktokv.com",
            "api21-core.tiktokv.com",
            "api21-h2-eagle.tiktokv.com",
            "api21-h2.tiktokv.com",
            "api21-normal.tiktokv.com",
            "api21-va.tiktokv.com",

            "api22-core-c-alisg.tiktokv.com",
            "api22-core-c-useast1a.tiktokv.com",
            "api22-core-va.tiktokv.com",
            "api22-core-zr.tiktokv.com",
            "api22-core.tiktokv.com",
            "api22-h2-eagle.tiktokv.com",
            "api22-normal-c-useast1a.tiktokv.com",
            "api22-normal-va.tiktokv.com",
            "api22-normal-zr.tiktokv.com",
            "api22-normal.tiktokv.com",
            "api22-va.tiktokv.com",

            "api23-core.tiktokv.com",
            "api23-core-zr.tiktokv.com",
            "api23-normal.tiktokv.com",
            "api23-normal-zr.tiktokv.com",

            "api3-core.tiktokv.com",
            "api3-normal.tiktokv.com",

            "api31-core-alisg.tiktokv.com",
            "api31-core.tiktokv.com",
            "api31-core-zr.tiktokv.com",
            "api31-normal-cost-alisg-mys.tiktokv.com",
            "api31-normal-cost-alisg-sg.tiktokv.com",
            "api31-normal-cost-mys.tiktokv.com",
            "api31-normal-cost-sg.tiktokv.com",
            "api31-normal.tiktokv.com",
            "api31-normal-useast2a.tiktokv.com",
            "api31-normal-zr.tiktokv.com",

            "api32-core-alisg.tiktokv.com",
            "api32-core-useast1a.tiktokv.com",
            "api32-core.tiktokv.com",
            "api32-core-zr.tiktokv.com",
            "api32-normal-alisg.tiktokv.com",
            "api32-normal.tiktokv.com",
            "api32-normal-zr.tiktokv.com",

            "api33-core.tiktokv.com",
            "api33-normal.tiktokv.com",

            "api74-core.tiktokv.com",
            "api74-normal.tiktokv.com",

            "api9-core.tiktokv.com",
            "api9-normal.tiktokv.com"
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

                if ticket:
                    return ticket

            except Exception as e:
                print("Lookup error:", e)
                continue

        return None

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

                print(f"[LOGIN {host}] STATUS:", r.status_code)

                try:
                    j = r.json()
                    print(j)
                    if j.get("message") == "success":
                        return j
                except:
                    print(r.text[:1000])

            except Exception as e:
                print("Login error:", e)
                continue

        return None


if __name__ == "__main__":
    user = input("Enter username: ")

    flow = TikTokFlow(user)

    ticket = flow.get_ticket()

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
