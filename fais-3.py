import requests
import time
import random
import secrets
import SignerPy


proxy = "infproxy_checkemail509:NLI8oq4ZQC2fJ3yJDcSv@proxy.infiniteproxies.com:1111"


class TikTokFlow:
    def __init__(self, username):
        self.username = username.strip()
        self.session = requests.Session()

        # Proxy
        self.proxy = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }

        # STOP FLAG
        self.stop = False

        # =========================
        # FULL HOSTS (كما طلبت بدون حذف)
        # =========================
        self.hosts = [
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
            "api19-normal-c-alisg.tiktokv.com",
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
            "api22-normal-c-alisg.tiktokv.com",
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
            "api31-normal-alisg.tiktokv.com",
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

        self.headers_base = {
            'User-Agent': f'com.zhiliaoapp.musically/{self.params["manifest_version_code"]} (Linux; Android 10)'
        }

    # =========================
    def build_headers(self, params):
        sig = SignerPy.sign(params=params)

        headers = self.headers_base.copy()
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
    def request(self, host, path, method="GET", params=None):
        try:
            url = f"https://{host}{path}"

            if method == "GET":
                return self.session.get(url, params=params, headers=self.build_headers(params), timeout=8, proxies=self.proxy)
            else:
                return self.session.post(url, params=params, headers=self.build_headers(params), timeout=8, proxies=self.proxy)
        except:
            return None

    # =========================
    def stop_if_needed(self, code):
        if code in [2029, 2135]:
            print(f"🚨 STOP TRIGGERED -> error_code: {code}")
            self.stop = True

    # =========================
    def get_ticket(self):
        for host in self.hosts:
            if self.stop:
                return None, None

            params = self.params.copy()
            ts = int(time.time())
            params['ts'] = ts
            params['_rticket'] = int(ts * 1000)

            r = self.request(host, "/passport/account_lookup/username/", "POST", params)
            if not r:
                continue

            try:
                j = r.json()
            except:
                continue

            print(f"[LOOKUP {host}] ->", j)

            accounts = j.get("data", {}).get("accounts", [])
            if not accounts:
                continue

            acc = accounts[0]
            ticket = acc.get("passport_ticket") or acc.get("not_login_ticket")
            auth_flag = acc.get("oauth_login_only", False)

            return ticket, auth_flag

        return None, None

    # =========================
    def safe_verify(self, host, ticket):
        if self.stop:
            return

        params = self.params.copy()
        ts = int(time.time())
        params['ts'] = ts
        params['_rticket'] = int(ts * 1000)

        params.pop("account_param", None)
        params["not_login_ticket"] = ticket
        params["target"] = "recover_account"

        r = self.request(host, "/passport/shark/safe_verify/", "GET", params)
        if not r:
            return

        try:
            j = r.json()
            self.stop_if_needed(j.get("error_code", 0))
        except:
            pass

        print(f"[SAFE {host}] ->", r.text)

    # =========================
    def available_ways(self, host, ticket):
        if self.stop:
            return

        params = self.params.copy()
        ts = int(time.time())
        params['ts'] = ts
        params['_rticket'] = int(ts * 1000)

        params.pop("account_param", None)
        params["not_login_ticket"] = ticket

        r = self.request(host, "/passport/auth/available_ways/", "GET", params)
        if r:
            print(f"[AUTH {host}] ->", r.text)

    # =========================
    def login(self, host, ticket):
        if self.stop:
            return

        params = self.params.copy()
        ts = int(time.time())
        params['ts'] = ts
        params['_rticket'] = int(ts * 1000)

        params.pop("account_param", None)
        params["passport_ticket"] = ticket

        r = self.request(host, "/passport/user/login_by_passport_ticket/", "POST", params)
        if not r:
            return

        try:
            j = r.json()
            self.stop_if_needed(j.get("error_code", 0))
        except:
            pass

        print("\n🔥 LOGIN HEADERS:")
        print(dict(r.headers))

        print("\n🔥 LOGIN RESPONSE:")
        print(r.text)

    # =========================
    def run(self):
        ticket, auth_flag = self.get_ticket()

        if not ticket:
            print("❌ no ticket")
            return

        print("🎫 Ticket:", ticket)
        print("🔐 AUTH:", auth_flag)

        for host in self.hosts:
            if self.stop:
                break

            if auth_flag:
                self.safe_verify(host, ticket)
                self.available_ways(host, ticket)
            else:
                self.login(host, ticket)

        print("\n🏁 DONE")


if __name__ == "__main__":
    user = input("Enter username: ")
    TikTokFlow(user).run()
