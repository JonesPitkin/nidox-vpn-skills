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
        description="Optimize existing WS, XHTTP, and Hysteria transports for Shadowrocket."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--direct-host", required=True)
    parser.add_argument("--xhttp-inbound-id", required=True, type=int)
    parser.add_argument("--database", default="/etc/x-ui/x-ui.db")
    parser.add_argument(
        "--subscription",
        default="/var/www/creatornsk/subscription.txt",
    )
    args = parser.parse_args()

    remote = f"""#!/usr/bin/env bash
set -euo pipefail
direct_host={shlex.quote(args.direct_host)}
db={shlex.quote(args.database)}
subscription={shlex.quote(args.subscription)}
xhttp_id={int(args.xhttp_inbound_id)}
site=/etc/nginx/sites-available/creator-services.conf
hysteria=/etc/hysteria/config.yaml
stamp="$(date +%Y%m%d-%H%M%S)"

cp -a "$db" "$db.before-shadowrocket-opt-$stamp"
cp -a "$site" "$site.before-shadowrocket-opt-$stamp"
cp -a "$hysteria" "$hysteria.before-shadowrocket-opt-$stamp"
cp -a "$subscription" "$subscription.before-shadowrocket-opt-$stamp"

sqlite3 "$db" <<SQL
BEGIN IMMEDIATE;
UPDATE inbounds
SET stream_settings = json_set(
  stream_settings,
  '$.xhttpSettings.mode', 'auto'
)
WHERE id = $xhttp_id
  AND protocol = 'vless'
  AND json_extract(stream_settings, '$.network') = 'xhttp';
COMMIT;
SQL

python3 - "$site" "$direct_host" <<'PY'
import pathlib
import re
import sys

site_name, host = sys.argv[1:]
site = pathlib.Path(site_name)
text = site.read_text()
marker = "    # shadowrocket-direct-transports"
if marker not in text:
    server_start = text.index("# direct-subscription-host: " + host)
    insert_at = text.index("    location = /sub {{", server_start)
    block = '''    # shadowrocket-direct-transports
    location = /e400c0b5203633483d47b062 {{
        proxy_http_version 1.1;
        proxy_set_header Host assets.creatornsk.ru;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_buffering off;
        proxy_pass http://127.0.0.1:10000;
    }}

    location ^~ /dd3953a380ec7cf9ffc08f98fd0e {{
        client_max_body_size 0;
        client_body_timeout 5m;
        proxy_http_version 1.1;
        proxy_set_header Host media.creatornsk.ru;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
        proxy_read_timeout 5m;
        proxy_send_timeout 5m;
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_pass http://127.0.0.1:10001;
    }}

'''
    text = text[:insert_at] + marker + "\\n" + block + text[insert_at:]
    site.write_text(text)
PY

python3 - "$subscription" "$direct_host" <<'PY'
import base64
import pathlib
import re
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

path = pathlib.Path(sys.argv[1])
host = sys.argv[2]
raw = base64.b64decode(path.read_bytes()).decode()
lines = []
for line in raw.splitlines():
    if not line.startswith("vless://"):
        lines.append(line)
        continue
    parts = urlsplit(line)
    params = dict(parse_qsl(parts.query, keep_blank_values=True))
    transport = params.get("type")
    if transport not in {{"ws", "xhttp"}}:
        lines.append(line)
        continue
    user = parts.username or ""
    params["sni"] = host
    params["host"] = host
    if transport == "xhttp":
        params["mode"] = "stream-one"
    netloc = user + "@" + host + ":443"
    lines.append(urlunsplit((parts.scheme, netloc, parts.path, urlencode(params), parts.fragment)))
path.write_bytes(base64.b64encode(("\\n".join(lines) + "\\n").encode()))
PY

python3 - "$hysteria" <<'PY'
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
text = path.read_text()
text = re.sub(r"(?ms)^quic:\\n(?:^[ \\t]+.*\\n)*", "", text)
text = re.sub(r"(?ms)^congestion:\\n(?:^[ \\t]+.*\\n)*", "", text)
text = re.sub(r"(?m)^ignoreClientBandwidth:.*\\n", "", text)
addition = '''quic:
  maxIdleTimeout: 60s
  keepAlivePeriod: 10s
  disablePathMTUDiscovery: true

congestion:
  type: bbr
  bbrProfile: standard

ignoreClientBandwidth: true

'''
path.write_text(addition + text)
PY

if ! nginx -t; then
  cp -a "$site.before-shadowrocket-opt-$stamp" "$site"
  exit 1
fi

systemctl restart x-ui
sleep 2
/usr/local/x-ui/bin/xray-linux-amd64 run -test \
  -config /usr/local/x-ui/bin/config.json

if ! systemctl restart hysteria-server; then
  cp -a "$hysteria.before-shadowrocket-opt-$stamp" "$hysteria"
  systemctl restart hysteria-server
  exit 1
fi

systemctl reload nginx
systemctl is-active x-ui nginx hysteria-server
sqlite3 -json "$db" \
  "select id,remark,json_extract(stream_settings,'$.xhttpSettings.mode') as mode from inbounds where id=$xhttp_id;"
printf 'DIRECT_HOST=%s\\n' "$direct_host"
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
            input_text=remote,
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
