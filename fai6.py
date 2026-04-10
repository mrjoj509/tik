import requests
import time
import SignerPy


class TikTokAPI:
    def __init__(self):
        self.session = requests.Session()
        self.host = "api19-normal-c-alisg.tiktokv.com"

    # =========================
    # LOOKUP
    # =========================
    def lookup(self, username):
        ts = int(time.time())

        params = {
            "request_tag_from": "h5",
            "fixed_mix_mode": "1",
            "mix_mode": "1",
            "account_param": username,
            "scene": "4",
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "_rticket": int(ts * 1000),
            "cdid": "5dfe9a97-2cad-47db-9fea-9bde2844ed5b",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "version_name": "37.8.5",
            "manifest_version_code": "2023708050",
            "update_version_code": "2023708050",
            "ab_version": "37.8.5",
            "resolution": "1600*900",
            "dpi": "240",
            "device_type": "SM-G998B",
            "device_brand": "samsung",
            "language": "ar",
            "os_api": "28",
            "os_version": "9",
            "ac": "wifi",
            "is_pad": "0",
            "current_region": "CA",
            "app_type": "normal",
            "sys_region": "EG",
            "last_install_time": "1772828019",
            "mcc_mnc": "302720",
            "timezone_name": "Asia/Riyadh",
            "carrier_region_v2": "302",
            "residence": "CA",
            "app_language": "ar",
            "carrier_region": "CA",
            "timezone_offset": "10800",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "ac2": "wifi",
            "uoo": "0",
            "op_region": "CA",
            "build_number": "37.8.5",
            "region": "EG",
            "ts": ts,
            "iid": "7614238166543714068",
            "device_id": "7551605328187246087",
            "openudid": "1035cfbf232d5e80",
            "support_webview": "1",
            "okhttp_version": "4.2.210.6-tiktok",
            "use_store_region_cookie": "1"
        }

        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2023708050 (Linux; Android 9; SM-G998B)",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "rpc-persist-pyxis-policy-v-tnc": "1",
            "x-ss-stub": "D41D8CD98F00B204E9800998ECF8427E",
            "x-tt-referer": "https://inapp.tiktokv.com/ucenter_web/account_lookup_tool",
            "x-tt-pba-enable": "1",
            "x-tt-dm-status": "login=0;ct=1;rt=1",
            "sdk-version": "2",
            "passport-sdk-version": "6031990",
            "x-tt-request-tag": "n=0;nr=011;bg=0",
            "content-type": "application/x-www-form-urlencoded"
        }

        sig = SignerPy.sign(params=params)
        headers.update({
            "x-ss-req-ticket": sig.get("x-ss-req-ticket", ""),
            "x-argus": sig.get("x-argus", ""),
            "x-gorgon": sig.get("x-gorgon", ""),
            "x-khronos": sig.get("x-khronos", ""),
            "x-ladon": sig.get("x-ladon", "")
        })

        url = f"https://{self.host}/passport/account_lookup/username/"
        r = self.session.post(url, params=params, headers=headers)

        print("\n========== LOOKUP ==========")
        print("STATUS:", r.status_code)
        print("HEADERS:", dict(r.headers))

        try:
            print("JSON:", r.json())
        except:
            print("TEXT:", r.text)

        try:
            return r.json()["data"]["accounts"][0]["passport_ticket"]
        except:
            return None

    # =========================
    # LOGIN
    # =========================
    def login(self, ticket):
        ts = int(time.time())

        params = {
            "request_tag_from": "h5",
            "passport_ticket": ticket,
            "device_platform": "android",
            "os": "android",
            "ssmix": "a",
            "_rticket": int(ts * 1000),
            "cdid": "5dfe9a97-2cad-47db-9fea-9bde2844ed5b",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "370805",
            "version_name": "37.8.5",
            "manifest_version_code": "2023708050",
            "update_version_code": "2023708050",
            "ab_version": "37.8.5",
            "resolution": "1600*900",
            "dpi": "240",
            "device_type": "SM-G998B",
            "device_brand": "samsung",
            "language": "ar",
            "os_api": "28",
            "os_version": "9",
            "ac": "wifi",
            "is_pad": "0",
            "current_region": "CA",
            "app_type": "normal",
            "sys_region": "EG",
            "last_install_time": "1772828019",
            "mcc_mnc": "302720",
            "timezone_name": "Asia/Riyadh",
            "carrier_region_v2": "302",
            "residence": "CA",
            "app_language": "ar",
            "carrier_region": "CA",
            "timezone_offset": "10800",
            "host_abi": "arm64-v8a",
            "locale": "ar",
            "ac2": "wifi",
            "uoo": "0",
            "op_region": "CA",
            "build_number": "37.8.5",
            "region": "EG",
            "ts": ts,
            "iid": "7614238166543714068",
            "device_id": "7551605328187246087",
            "openudid": "1035cfbf232d5e80",
            "support_webview": "1",
            "okhttp_version": "4.2.210.6-tiktok",
            "use_store_region_cookie": "1"
        }

        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2023708050 (Linux; Android 9; SM-G998B)",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "rpc-persist-pyxis-policy-v-tnc": "1",
            "x-ss-stub": "D41D8CD98F00B204E9800998ECF8427E",
            "x-tt-referer": "https://inapp.tiktokv.com/ucenter_web/account_lookup_tool",
            "x-tt-pba-enable": "1",
            "x-tt-dm-status": "login=0;ct=1;rt=1",
            "sdk-version": "2",
            "passport-sdk-version": "6031990",
            "x-tt-request-tag": "n=0;nr=011;bg=0",
            "content-type": "application/x-www-form-urlencoded"
        }

        sig = SignerPy.sign(params=params)
        headers.update({
            "x-ss-req-ticket": sig.get("x-ss-req-ticket", ""),
            "x-argus": sig.get("x-argus", ""),
            "x-gorgon": sig.get("x-gorgon", ""),
            "x-khronos": sig.get("x-khronos", ""),
            "x-ladon": sig.get("x-ladon", "")
        })

        url = f"https://{self.host}/passport/user/login_by_passport_ticket/"
        r = self.session.post(url, params=params, headers=headers)

        print("\n========== LOGIN ==========")
        print("STATUS:", r.status_code)
        print("HEADERS:", dict(r.headers))

        try:
            print("JSON:", r.json())
        except:
            print("TEXT:", r.text)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    user = input("username: ")

    api = TikTokAPI()

    ticket = api.lookup(user)

    if not ticket:
        print("❌ فشل lookup")
        exit()

    print("✅ ticket:", ticket)

    api.login(ticket)
