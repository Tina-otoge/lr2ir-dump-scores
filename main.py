import argparse
import os

import requests


def get_xml_tag_content(xml: str, tag: str) -> str:
    return xml.split(f"<{tag}>", 1)[1].split(f"</{tag}>", 1)[0].strip()


parser = argparse.ArgumentParser()

parser.add_argument("lr2ir_player_id", type=int)
parser.add_argument("--include-replays", action="store_true")

args = parser.parse_args()

BASE_URL = "http://www.dream-pro.info/~lavalse/LR2IR/2"

rival_info_response = requests.get(
    f"{BASE_URL}/getplayerxml.cgi?id={args.lr2ir_player_id}&lastupdate",
)
rival_info_response.raise_for_status()
content = rival_info_response.content.decode("shift-jis")
rival_name = get_xml_tag_content(content, "rivalname")

target_xml_file = f"{args.lr2ir_player_id}_{rival_name}.xml"
with open(target_xml_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Saved rival info to {target_xml_file}")

if args.include_replays:
    target_replays_dir = f"replays/{args.lr2ir_player_id}_{rival_name}"

    for line in content.splitlines():
        if not line.strip().startswith("<hash>"):
            continue
        bms_hash = get_xml_tag_content(line, "hash")
        replay_response = requests.get(
            f"{BASE_URL}/getghost.cgi?songmd5={bms_hash}&targetid={args.lr2ir_player_id}",
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
