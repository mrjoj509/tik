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
            "api31-normal-alisg.tiktokv.com"
        ]

        self.params = {
            "device_platform": "android",
            "ssmix": "a",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "version_name": "37.8.5",
            "manifest_version_code": "2023708050",
            "update_version_code": "2023708050",
            "ab_version": "37.8.5",
            "os_version": "10",
            "device_type": "SM-G998B",
            "resolution": "1600*900",
            "dpi": "240",
            "language": "ar",
            "os_api": "29",
            "ac": "wifi",
            "timezone_name": "Asia/Riyadh",
            "carrier_region": "SA",
            "sys_region": "SA",
            "region": "SA",
            "app_language": "ar",
            "timezone_offset": "10800",
            "request_tag_from": "h5",
            "account_param": self.username,
            "scene": "4",
            "mix_mode": "1",
            "device_id": str(random.randint(10**18, 10**19-1)),
            "iid": str(random.randint(10**18, 10**19-1)),
            "openudid": secrets.token_hex(8),
        }

        self.headers_base = {
            "User-Agent": f"com.zhiliaoapp.musically/{self.params['manifest_version_code']} (Linux; Android 10)"
        }

    # =========================
    # SIGN WRAPPER
    # =========================
    def sign(self, params):
        ts = int(time.time())
        params["ts"] = ts
        params["_rticket"] = int(ts * 1000)
        return SignerPy.sign(params=params)

    # =========================
    # 1. ACCOUNT LOOKUP
    # =========================
    def get_ticket(self):
        for host in self.hosts:
            params = self.params.copy()

            try:
                sig = self.sign(params)
            except Exception as e:
                print("sign error:", e)
                continue

            headers = self.headers_base.copy()
            headers.update(sig)

            url = f"https://{host}/passport/account_lookup/username/"

            try:
                r = self.session.post(url, params=params, headers=headers, timeout=10)
                j = r.json()

                print("[LOOKUP]", j)

                accounts = j.get("data", {}).get("accounts", [])
                if not accounts:
                    continue

                acc = accounts[0]

                return {
                    "passport_ticket": acc.get("passport_ticket"),
                    "not_login_ticket": acc.get("not_login_ticket"),
                    "username": acc.get("username")
                }

            except Exception as e:
                print("lookup error:", e)

        return None

    # =========================
    # 2. SAFE VERIFY (OPTIONAL STEP)
    # =========================
    def safe_verify(self, ticket):
        for host in self.hosts:
            params = self.params.copy()
            params.pop("account_param", None)
            params["not_login_ticket"] = ticket
            params["target"] = "recover_account"

            try:
                sig = self.sign(params)
            except:
                continue

            headers = self.headers_base.copy()
            headers.update(sig)

            url = f"https://{host}/passport/shark/safe_verify/"

            try:
                r = self.session.get(url, params=params, headers=headers, timeout=10)
                j = r.json()

                print("[SAFE VERIFY]", j)

                return j

            except Exception as e:
                print("safe error:", e)

        return None

    # =========================
    # 3. AVAILABLE WAYS (INFO ONLY)
    # =========================
    def available_ways(self, ticket):
        for host in self.hosts:
            params = self.params.copy()
            params.pop("account_param", None)
            params["ticket"] = ticket

            try:
                sig = self.sign(params)
            except:
                continue

            headers = self.headers_base.copy()
            headers.update(sig)

            url = f"https://{host}/passport/auth/available_ways/"

            try:
                r = self.session.get(url, params=params, headers=headers, timeout=10)
                j = r.json()

                print("[AVAILABLE WAYS]", j)
                return j

            except Exception as e:
                print("available error:", e)

        return None

    # =========================
    # 4. LOGIN CORE
    # =========================
    def login(self, ticket_obj):
        ticket = ticket_obj.get("passport_ticket") or ticket_obj.get("not_login_ticket")

        # 🔥 main login
        result = self._login(ticket)

        # 🔥 extra analytics only (no effect on flow)
        self.available_ways(ticket)

        if result:
            return result

        # optional safe step
        safe = self.safe_verify(ticket)
        if safe:
            new_ticket = safe.get("data", {}).get("ticket")
            if new_ticket:
                return self._login(new_ticket)

        return None

    # =========================
    # LOGIN REQUEST
    # =========================
    def _login(self, ticket):
        if not ticket:
            return None

        for host in self.hosts:
            params = self.params.copy()
            params.pop("account_param", None)
            params["passport_ticket"] = ticket

            try:
                sig = self.sign(params)
            except:
                continue

            headers = self.headers_base.copy()
            headers.update(sig)

            url = f"https://{host}/passport/user/login_by_passport_ticket/"

            try:
                r = self.session.post(url, params=params, headers=headers, timeout=10)
                j = r.json()

                print("[LOGIN]", j)

                if j.get("message") == "success":
                    return j

            except Exception as e:
                print("login error:", e)

        return None


# =========================
# RUN
# =========================
if __name__ == "__main__":
    user = input("Enter username: ")

    flow = TikTokFlow(user)

    tickets = flow.get_ticket()

    if not tickets:
        print("no ticket")
        exit()

    print("tickets:", tickets)

    result = flow.login(tickets)

    print("\nFINAL:", result)
