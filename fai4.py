import requests
import time
import random
import secrets


class TikTokFlowFixed:
    def __init__(self, username):
        self.username = username.strip()

        self.hosts = [
            "api19-normal-c-alisg.tiktokv.com",
            "api22-normal-c-alisg.tiktokv.com",
            "api31-normal-alisg.tiktokv.com"
        ]

        self.base_params = {
            'device_platform': 'android',
            'channel': 'googleplay',
            'app_name': 'musical_ly',
            'version_code': '370805',
            'os_version': '10',
            'language': 'ar',
            'region': 'SA',
            'account_param': self.username,
        }

    def build_params(self):
        params = self.base_params.copy()

        ts = int(time.time())
        params['ts'] = ts
        params['_rticket'] = int(ts * 1000)

        params['device_id'] = str(random.randint(10**18, 10**19-1))
        params['iid'] = str(random.randint(10**18, 10**19-1))

        return params

    def new_session(self):
        return requests.Session()

    def request(self, host, url_path, params):
        session = self.new_session()

        url = f"https://{host}/{url_path}"

        try:
            r = session.post(url, params=params, timeout=10)

            print("\n===================")
            print("HOST:", host)
            print("STATUS:", r.status_code)
            print("HEADERS:", dict(r.headers))

            try:
                print("JSON:", r.json())
            except:
                print("TEXT:", r.text[:1000])

            print("===================\n")

            return r

        except Exception as e:
            print("❌ Request error:", e)
            return None

    def run(self):
        for host in self.hosts:

            params = self.build_params()

            print(f"\n🚀 Trying host: {host}")

            # طلب 1
            r1 = self.request(host, "passport/account_lookup/username/", params)

            if not r1:
                continue

            time.sleep(random.uniform(2, 5))  # مهم جدًا

            # طلب 2
            params2 = self.build_params()

            r2 = self.request(host, "passport/user/login_by_passport_ticket/", params2)

            if r2 and r2.status_code == 200:
                print("✅ Success on host:", host)
                return

        print("❌ Failed on all hosts")


if __name__ == "__main__":
    username = input("Enter username: ")
    flow = TikTokFlowFixed(username)
    flow.run()
