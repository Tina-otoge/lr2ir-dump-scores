import argparse
import os
import time

from requests import Session
from requests.exceptions import ConnectTimeout

print("DO NOT ATTEMPT TO SCRAPE THE ENTIRETY OF LR2IR.")
print("LR2IR 全体をスクレイピングしようとしないでください。")
print()
print(
    "This script is intended for dumping your own LR2IR data, and tries to do"
    "\nso responsibly."
)
print("Do not remove the self-imposed rate limit.")
print()
input("Press Enter to continue...")


class LR2IRDumpSession(Session):
    RATE_LIMIT_SECONDS = 1
    TIMEOUT_SECONDS = 10

    def __init__(self):
        super().__init__()
        self.last_request_time = 0

    def request(self, *args, **kwargs):
        elapsed = time.time() - self.last_request_time
        # print(f"Time since last request: {elapsed:.2f}s")
        kwargs.setdefault("timeout", self.TIMEOUT_SECONDS)
        delta = self.RATE_LIMIT_SECONDS - elapsed
        exponential_backoff = 2
        if delta > 0:
            print(f"Self-rate limiting: sleeping for {delta:.2f}s")
            time.sleep(delta)
        while True:
            try:
                response = super().request(*args, **kwargs)
                break
            except ConnectTimeout:
                print(
                    f"Request timed out, retrying after {exponential_backoff}s"
                )
                time.sleep(exponential_backoff)
                exponential_backoff *= 2
                if exponential_backoff > 60:
                    exponential_backoff = 60
                continue
        self.last_request_time = time.time()
        return response


def get_xml_tag_content(xml: str, tag: str) -> str:
    return xml.split(f"<{tag}>", 1)[1].split(f"</{tag}>", 1)[0].strip()


parser = argparse.ArgumentParser()

parser.add_argument("lr2ir_player_id", type=int)
parser.add_argument("--include-replays", action="store_true")

args = parser.parse_args()

BASE_URL = "http://www.dream-pro.info/~lavalse/LR2IR"

session = LR2IRDumpSession()

rival_info_response = session.get(
    f"{BASE_URL}/2/getplayerxml.cgi?id={args.lr2ir_player_id}&lastupdate",
)
rival_info_response.raise_for_status()
content = rival_info_response.content.decode("shift-jis")
rival_name = get_xml_tag_content(content, "rivalname")

target_rivalinfo_file = f"{args.lr2ir_player_id}_{rival_name}_rivalinfo.xml"
with open(target_rivalinfo_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved rival info to {target_rivalinfo_file}")

mypage_response = session.get(
    f"{BASE_URL}/search.cgi?mode=mypage&playerid={args.lr2ir_player_id}",
)
mypage_response.raise_for_status()
content = mypage_response.content.decode("shift-jis")
target_mypage_file = f"{args.lr2ir_player_id}_{rival_name}_mypage.html"
with open(target_mypage_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved mypage to {target_mypage_file}")

if args.include_replays:
    target_replays_dir = f"replays/{args.lr2ir_player_id}_{rival_name}"

    for line in content.splitlines():
        if not line.strip().startswith("<hash>"):
            continue
        bms_hash = get_xml_tag_content(line, "hash")
        replay_response = session.get(
            f"{BASE_URL}/2/getghost.cgi?songmd5={bms_hash}&targetid={args.lr2ir_player_id}",
        )
        if not replay_response.ok:
            print(
                f"Failed to get replay for hash {bms_hash} {replay_response.status_code=}"
            )
            continue
        os.makedirs(target_replays_dir, exist_ok=True)
        replay_path = os.path.join(target_replays_dir, f"{bms_hash}.csv")
        with open(replay_path, "wb") as f:
            # Format: name, play_option, rseed, ghost
            wrote_bytes = f.write(replay_response.content)
        print(
            f"Saved replay for hash {bms_hash} to {replay_path} ({wrote_bytes} bytes)"
        )
