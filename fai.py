import requests
import time
import random
import secrets
import SignerPy


class TikTokHybrid:
    def __init__(self, input_value):
        self.input = input_value.strip()
        self.session = requests.Session()

        self.hosts = [
            "api19-normal-c-alisg.tiktokv.com",
            "api22-normal-c-alisg.tiktokv.com",
            "api31-normal-alisg.tiktokv.com"
        ]

        self.scenes = ["1", "2", "4"]
        self.regions = ["SA", "US", "EG"]

    def base_params(self):
        return {
            'device_platform': 'android',
            'aid': '1233',
            'app_name': 'musical_ly',
            'version_code': '370805',
            'version_name': '37.8.5',
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
            'app_language': 'ar',
            'timezone_offset': '10800',
        }

    def sign_headers(self, params):
        sig = SignerPy.sign(params=params)
        return {
            'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
            'x-ss-stub': sig.get('x-ss-stub', ''),
            'x-argus': sig.get('x-argus', ''),
            'x-gorgon': sig.get('x-gorgon', ''),
            'x-khronos': sig.get('x-khronos', ''),
            'x-ladon': sig.get('x-ladon', ''),
        }

    # ============================================
    # 🔍 Username Bruteforce Lookup
    # ============================================
    def username_lookup(self):
        print("\n🔥 [USERNAME FLOW START]\n")

        for host in self.hosts:
            for scene in self.scenes:
                for region in self.regions:

                    params = self.base_params()
                    params.update({
                        "account_param": self.input,
                        "scene": scene,
                        "region": region,
                        "sys_region": region
                    })

                    ts = int(time.time())
                    params["ts"] = ts
                    params["_rticket"] = int(ts * 1000)

                    try:
                        headers = self.sign_headers(params)
                    except:
                        continue

                    try:
                        r = self.session.post(
                            f"https://{host}/passport/account_lookup/username/",
                            params=params,
                            headers=headers,
                            timeout=10
                        )

                        j = r.json()
                        print(f"[TRY] host={host} scene={scene} region={region}")

                        accounts = j.get("data", {}).get("accounts", [])
                        if not accounts:
                            continue

                        acc = accounts[0]
                        ticket = acc.get("passport_ticket") or acc.get("not_login_ticket")
                        username = acc.get("username") or acc.get("user_name")

                        if ticket:
                            print("✅ GOT TICKET")
                            return ticket, username, "username_flow"

                    except:
                        continue

        return None, None, "username_failed"

    # ============================================
    # 🧠 Smart Runner
    # ============================================
    def run(self):
        ticket, username, method = self.username_lookup()

        if ticket:
            return {
                "status": "success",
                "method": method,
                "username": username,
                "ticket": ticket
            }

        print("\n⚠️ Username flow failed → هنا تربط email flow\n")

        return {
            "status": "partial",
            "method": "username_failed",
            "username": None,
            "ticket": None
        }


# ============================================
# تشغيل
# ============================================
if __name__ == "__main__":
    user = input("Enter username: ")

    engine = TikTokHybrid(user)
    result = engine.run()

    print("\n🔥 FINAL RESULT:")
    print(result)
