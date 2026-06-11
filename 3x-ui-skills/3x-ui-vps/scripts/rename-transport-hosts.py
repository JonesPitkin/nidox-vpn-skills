#!/usr/bin/env python3
import argparse
import shlex
import subprocess
import sys
from typing import Optional


def run(*args: str, input_text: Optional[str] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        input=input_text,
        text=True,
        check=True,
        capture_output=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate 3X-UI transport hostnames while retaining old aliases."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--zone", required=True)
    parser.add_argument("--server-ip", required=True)
    parser.add_argument("--reality-host", required=True)
    parser.add_argument("--ws-host", required=True)
    parser.add_argument("--xhttp-host", required=True)
    args = parser.parse_args()

    zone = shlex.quote(args.zone)
    server_ip = shlex.quote(args.server_ip)
    reality = shlex.quote(args.reality_host)
    ws = shlex.quote(args.ws_host)
    xhttp = shlex.quote(args.xhttp_host)

    remote_script = f"""#!/usr/bin/env bash
set -euo pipefail

zone={zone}
server_ip={server_ip}
reality_host={reality}
ws_host={ws}
xhttp_host={xhttp}
zone_id="a31050069ca7f26d78b04b1400c3d821"
token="$(awk -F' = ' '/dns_cloudflare_api_token/ {{print $2}}' /root/.secrets/cloudflare.ini)"
api="https://api.cloudflare.com/client/v4/zones/${{zone_id}}/dns_records"

upsert_record() {{
    local name="$1" proxied="$2"
    local record_id
    record_id="$(curl -fsS "$api?type=A&name=$name" \
      -H "Authorization: Bearer $token" \
      -H "Content-Type: application/json" | jq -r '.result[0].id // empty')"
    payload="$(jq -nc --arg name "$name" --arg content "$server_ip" \
      --argjson proxied "$proxied" \
      '{{type:"A",name:$name,content:$content,ttl:1,proxied:$proxied}}')"
    if [[ -n "$record_id" ]]; then
        curl -fsS -X PUT "$api/$record_id" \
          -H "Authorization: Bearer $token" \
          -H "Content-Type: application/json" \
          --data "$payload" >/dev/null
    else
        curl -fsS -X POST "$api" \
          -H "Authorization: Bearer $token" \
          -H "Content-Type: application/json" \
          --data "$payload" >/dev/null
    fi
}}

upsert_record "$reality_host" false
upsert_record "$ws_host" true
upsert_record "$xhttp_host" true

certbot certonly --manual --preferred-challenges dns \
  --manual-auth-hook /usr/local/sbin/cloudflare-certbot-auth \
  --manual-cleanup-hook /usr/local/sbin/cloudflare-certbot-cleanup \
  --non-interactive --agree-tos \
  --cert-name creatornsk-services --expand \
  -d panel.creatornsk.ru \
  -d hy.creatornsk.ru \
  -d reality.creatornsk.ru \
  -d ws.creatornsk.ru \
  -d xhttp.creatornsk.ru \
  -d "$reality_host" \
  -d "$ws_host" \
  -d "$xhttp_host"

stamp="$(date +%Y%m%d-%H%M%S)"
cp -a /etc/x-ui/x-ui.db "/etc/x-ui/x-ui.db.before-neutral-hosts-$stamp"
cp -a /etc/nginx/sites-available/creator-services.conf \
  "/etc/nginx/sites-available/creator-services.conf.before-neutral-hosts-$stamp"
cp -a /etc/nginx/stream-enabled/creator-reality.conf \
  "/etc/nginx/stream-enabled/creator-reality.conf.before-neutral-hosts-$stamp"

python3 - "$ws_host" "$xhttp_host" "$reality_host" <<'PY'
import pathlib
import sys

ws, xhttp, reality = sys.argv[1:]
site = pathlib.Path("/etc/nginx/sites-available/creator-services.conf")
text = site.read_text()
text = text.replace(
    "server_name ws.creatornsk.ru;",
    f"server_name {{ws}} ws.creatornsk.ru;",
)
text = text.replace(
    "proxy_set_header Host ws.creatornsk.ru;",
    f"proxy_set_header Host {{ws}};",
)
text = text.replace(
    "server_name xhttp.creatornsk.ru;",
    f"server_name {{xhttp}} xhttp.creatornsk.ru;",
)
text = text.replace(
    "proxy_set_header Host xhttp.creatornsk.ru;",
    f"proxy_set_header Host {{xhttp}};",
)
site.write_text(text)

stream = pathlib.Path("/etc/nginx/stream-enabled/creator-reality.conf")
text = stream.read_text()
needle = "    panel.creatornsk.ru creator_https;\\n"
aliases = (
    f"    {{ws}} creator_https;\\n"
    f"    {{xhttp}} creator_https;\\n"
)
if aliases not in text:
    text = text.replace(needle, needle + aliases)
stream.write_text(text)
PY

sqlite3 /etc/x-ui/x-ui.db <<SQL
BEGIN IMMEDIATE;
UPDATE inbounds SET stream_settings = json_set(
  stream_settings,
  '$.externalProxy[0].dest', '$reality_host'
) WHERE id = 1;
UPDATE inbounds SET stream_settings = json_set(
  stream_settings,
  '$.wsSettings.host', '$ws_host',
  '$.externalProxy[0].dest', '$ws_host',
  '$.externalProxy[0].sni', '$ws_host'
) WHERE id = 2;
UPDATE inbounds SET stream_settings = json_set(
  stream_settings,
  '$.xhttpSettings.host', '$xhttp_host',
  '$.externalProxy[0].dest', '$xhttp_host',
  '$.externalProxy[0].sni', '$xhttp_host'
) WHERE id = 3;
COMMIT;
SQL

python3 - "$reality_host" "$ws_host" "$xhttp_host" <<'PY'
import base64
import pathlib
import sys

reality, ws, xhttp = sys.argv[1:]
path = pathlib.Path("/var/www/creatornsk/subscription.txt")
raw = base64.b64decode(path.read_bytes()).decode()
raw = raw.replace("reality.creatornsk.ru", reality)
raw = raw.replace("ws.creatornsk.ru", ws)
raw = raw.replace("xhttp.creatornsk.ru", xhttp)
path.write_bytes(base64.b64encode(raw.encode()))
PY

nginx -t
systemctl restart x-ui
systemctl reload nginx
sleep 2
/usr/local/x-ui/bin/xray-linux-amd64 run -test \
  -config /usr/local/x-ui/bin/config.json
systemctl is-active x-ui nginx hysteria-server
"""

    try:
        result = run(
            "ssh",
            "-i",
            args.ssh_key,
            "-o",
            "StrictHostKeyChecking=accept-new",
            args.host,
            "bash -s",
            input_text=remote_script,
        )
    except subprocess.CalledProcessError as exc:
        sys.stdout.write(exc.stdout or "")
        sys.stderr.write(exc.stderr or "")
        return exc.returncode
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
