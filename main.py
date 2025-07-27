import requests
import urllib3
import time
import json
from datetime import datetime
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = "https://inymxsvpmkfwnlmowzpi.supabase.co"
TOKEN_FILE = "multi_token.jsonl"
with open("config.json") as f:
    config = json.load(f)
apikey = config["apikey"]


def load_all_tokens():
    if not os.path.exists(TOKEN_FILE):
        raise Exception("multi_token.jsonl belum ada")
    with open(TOKEN_FILE, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def save_all_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        for token in tokens:
            json.dump(token, f)
            f.write("\n")

def refresh_token_logic(token_data):
    refresh_token = token_data["refresh_token"]
    headers = {
        "apikey": apikey,
        "Authorization": f"Bearer {token_data['access_token']}",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://wizolayer.xyz",
        "Referer": "https://wizolayer.xyz/",
    }
    payload = {"refresh_token": refresh_token}
    url = f"{url_base}/auth/v1/token?grant_type=refresh_token"
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        new_token = res.json()
        new_token["expires_at"] = int(time.time()) + new_token["expires_in"]
        print("✅ Token diperbarui")
        return new_token
    else:
        print("❌ Gagal refresh token:", res.text)
        return None

def build_headers(token_data):
    now = int(time.time())
    if now >= token_data.get("expires_at", 0):
        print("🔄 Token expired, refreshing...")
        updated = refresh_token_logic(token_data)
        if updated:
            token_data.update(updated)
        else:
            raise Exception("Gagal refresh token")
    return {
        "Authorization": f"Bearer {token_data['access_token']}",
        "apikey": apikey,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://wizolayer.xyz/",
        "Origin": "https://wizolayer.xyz",
        "Cookie": "__cf_bm=placeholder;"
    }

def get_task(t_id, headers):
    url = f"{url_base}/rest/v1/rpc/handle_task_reward"
    payload = {"t_id": t_id}
    response = requests.post(url, json=payload, headers=headers)
    try:
        data = response.json()
    except:
        data = response.text
    if response.status_code == 200:
        print(f"✅ Task {t_id} success: {data.get('msg', data)}")
    else:
        print(f"❌ Task {t_id} gagal: {response.status_code} - {data}")

def handle_tasks(headers):
    task_ids = [
         "cab15d31-5924-438e-b928-9630cb42a481",
        "373193f0-e49c-43af-bc89-990ad1caff2b",
        "dffa7479-6b12-4809-9109-f76b857d6cdc",
        "2525036b-68c3-4586-b6ea-01b42fdf9e9a",
        "a609d06b-f75a-4339-b448-9de191727163",
        "e8e784e8-c5a3-4e55-b877-646c28f17de9",
        "cde30cd4-f9cd-4435-9e26-4f40ea9ee44f",
        "a46a5e91-1aad-4c5c-9356-720a40b6ff2f",
        "7a65ca76-cff4-4cd4-85da-3ac5c9df5320",
        "4f709637-22d5-4af0-8ca7-733061aff820",
        "dfe81957-b5e1-4799-9f2f-d8ea47654858",
        "e0762234-c86c-4a2e-aa6b-a5a487d2732e",
        "290b09d6-b7f9-4d99-a431-5c125130876e",
        "a996f325-dc74-4557-a48e-6345c6134e64",
        "91d6b535-ab82-4054-8960-f123294513e7",
        "052d82ac-b061-49b9-9bbe-e322cf12c6b7",
        "dd08783d-d1ab-48dd-8dc7-7df31c57e8fd",
        "4f1b0036-471d-4a1e-9f47-00ce4f424c80",
        "8038d956-53b6-45a1-ad89-0295d1289005",
        "9840c98b-34c9-4be1-81b1-1f992f724d3a",
        "3b37c8bf-a9fa-435f-aae8-b364dd15b3a2",
        "5dc39d6e-d7fa-4a72-a8e1-64abf9e4f033",
        "0eb0b5c5-8460-47fb-a11a-61c80957e20c",
        "8bb15a6a-abf3-4152-8f93-c52016e1109a",
        "4a590eaf-cfc1-49fb-8799-9dac5a6a4b90",
        "819546da-8d87-45f3-83ef-e9b6be068e1b",
        "72b40568-62f6-467e-99f2-a59a8a03a57b",
        "4eca801d-20af-4cbc-8b8f-e75430ad5502",
        "c9ab6deb-52d2-4343-a4c1-f149fb85b085",
        "734e255e-a50d-460c-a832-6185f4cd7975",
        "22ad0c1c-ba3e-49fa-a569-a6358f98bf30"
    ]
    for t_id in task_ids:
        get_task(t_id, headers)
        time.sleep(1)

def mining(headers, idx):
    url = "https://api.wizolayer.xyz/api/mining/sync"
    payload = {"origin": "https://wizolayer.xyz"}
    response = requests.post(url, json=payload, headers=headers, verify=False)
    print(f"🛠️ Akun #{idx+1} -", response.text)
    if response.status_code == 200:
        print(f"[{datetime.now().isoformat()}] 🚀 Mining berhasil di akun #{idx+1}")
    else:
        print(f"❌ Error mining akun #{idx+1}: {response.status_code}")

if __name__ == "__main__":
    try:
        all_tokens = load_all_tokens()
        updated_tokens = []

        # Jalankan semua task sekali untuk semua akun
        for idx, token_data in enumerate(all_tokens):
            print(f"\n=== 🧾 TASK Akun #{idx+1} ===")
            try:
                headers = build_headers(token_data)
                handle_tasks(headers)
            except Exception as e:
                print(f"❌ Gagal task akun #{idx+1}: {e}")
            updated_tokens.append(token_data)

        # Simpan token setelah refresh
        save_all_tokens(updated_tokens)

        # Mining loop bergiliran
        while True:
            for idx, token_data in enumerate(updated_tokens):
                print(f"\n=== 🔄 MINING Akun #{idx+1} ===")
                try:
                    headers = build_headers(token_data)
                    mining(headers, idx)
                    save_all_tokens(updated_tokens)  # Save setiap putaran
                except Exception as e:
                    print(f"❌ Error mining akun #{idx+1}: {e}")
                time.sleep(300)  # Delay 5 menit antar akun

    except KeyboardInterrupt:
        print("⛔ Program dihentikan pengguna")
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan utama: {e}")
