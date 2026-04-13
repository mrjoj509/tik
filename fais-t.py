import requests
import time
import random
import secrets
import SignerPy


class TikTokFlow:
    def __init__(self, username, proxy=None):
        self.username = username.strip()
        self.session = requests.Session()

        self.proxy_dict = None
        if proxy:
            self.proxy_dict = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            self.session.proxies.update(self.proxy_dict)

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

    # =========================
    # SIGN
    # =========================
    def build_headers(self, params):
        sig = SignerPy.sign(params=params)

        headers = self.headers.copy()
        headers.update({
            'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
            'x-ss-stub': sig.get('x-ss-stub', ''),
            'x-argus': sig.get('x-argus', ''),
            'x-gorgon': sig.get('x-gorgon', ''),
            'x-khronos': sig.get('x-khronos', ''),
            'x-ladon': sig.get('x-ladon', ''),
        })

        return headers

    # =========================
    # LOOKUP
    # =========================
    def get_ticket(self):
        for host in self.hosts:
            try:
                params = self.params.copy()
                ts = int(time.time())
                params['ts'] = ts
                params['_rticket'] = int(ts * 1000)

                headers = self.build_headers(params)
                headers['x-tt-passport-csrf-token'] = secrets.token_hex(16)

                url = f"https://{host}/passport/account_lookup/username/"
                r = self.session.post(url, params=params, headers=headers, timeout=10)

                j = r.json()
                print(f"\n[LOOKUP {host}] ->", j)

                accounts = j.get("data", {}).get("accounts", [])
                if accounts:
                    acc = accounts[0]
                    return acc.get("passport_ticket") or acc.get("not_login_ticket")

            except Exception as e:
                print(f"[LOOKUP ERROR {host}]", e)

        return None

    # =========================
    # SAFE
    # =========================
    def safe_verify(self, ticket):
        for host in self.hosts:
            try:
                params = self.params.copy()
                ts = int(time.time())
                params['ts'] = ts
                params['_rticket'] = int(ts * 1000)

                params.pop("account_param", None)
                params["not_login_ticket"] = ticket
                params["target"] = "recover_account"

                headers = self.build_headers(params)

                url = f"https://{host}/passport/shark/safe_verify/"
                r = self.session.get(url, params=params, headers=headers, timeout=10)

                print(f"\n[SAFE {host}] -> {r.text}")

            except Exception as e:
                print(f"[SAFE ERROR {host}]", e)

    # =========================
    # AVAILABLE WAYS
    # =========================
    def available_ways(self, ticket):
        for host in self.hosts:
            try:
                params = self.params.copy()
                ts = int(time.time())
                params['ts'] = ts
                params['_rticket'] = int(ts * 1000)

                params.pop("account_param", None)
                params["not_login_ticket"] = ticket

                headers = self.build_headers(params)

                url = f"https://{host}/passport/auth/available_ways/"
                r = self.session.get(url, params=params, headers=headers, timeout=10)

                print(f"\n[WAYS {host}] -> {r.text}")

            except Exception as e:
                print(f"[WAYS ERROR {host}]", e)

    # =========================
    # LOGIN (FINAL)
    # =========================
    def login_by_ticket(self, ticket):
        for host in self.hosts:
            try:
                params = self.params.copy()
                ts = int(time.time())
                params['ts'] = ts
                params['_rticket'] = int(ts * 1000)

                params.pop("account_param", None)
                params["passport_ticket"] = ticket

                headers = self.build_headers(params)

                url = f"https://{host}/passport/user/login_by_passport_ticket/"
                r = self.session.post(
                    url,
                    params=params,
                    headers=headers,
                    proxies=self.proxy_dict,
                    timeout=10
                )

                # 🔥 RESPONSE + HEADERS (هذا المطلوب)
                print(f"\n================ LOGIN [{host}] ================")
                print("STATUS:", r.status_code)
                print("RESPONSE HEADERS:", dict(r.headers))
                print("RESPONSE BODY:", r.text)
                print("REQUEST HEADERS SENT:", dict(r.request.headers))
                print("==============================================\n")

                return r.text

            except Exception as e:
                print(f"[LOGIN ERROR {host}]", e)

        return None


# =========================
# RUN
# =========================
if __name__ == "__main__":
    proxy = "infproxy_checkemail509:NLI8oq4ZQC2fJ3yJDcSv@proxy.infiniteproxies.com:1111"

    user = input("Enter username: ")

    flow = TikTokFlow(user, proxy=proxy)

    ticket = flow.get_ticket()

    if not ticket:
        print("❌ no ticket")
        exit()

    print("🎫 Ticket:", ticket)

    flow.safe_verify(ticket)
    flow.available_ways(ticket)

    flow.login_by_ticket(ticket)
