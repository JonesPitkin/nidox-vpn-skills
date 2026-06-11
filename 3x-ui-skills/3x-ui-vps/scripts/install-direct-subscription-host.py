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
        description="Install a DNS-only HTTPS hostname for a static subscription."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--server-name", required=True)
    parser.add_argument("--server-ip", required=True)
    parser.add_argument("--route", default="/sub")
    parser.add_argument(
        "--source",
        default="/var/www/creatornsk/subscription.txt",
    )
    args = parser.parse_args()
    route = args.route if args.route.startswith("/") else "/" + args.route

    remote = f"""#!/usr/bin/env bash
set -euo pipefail
server_name={shlex.quote(args.server_name)}
server_ip={shlex.quote(args.server_ip)}
route={shlex.quote(route)}
source_file={shlex.quote(args.source)}
zone_id="a31050069ca7f26d78b04b1400c3d821"
token="$(awk -F' = ' '/dns_cloudflare_api_token/ {{print $2}}' /root/.secrets/cloudflare.ini)"
api="https://api.cloudflare.com/client/v4/zones/${{zone_id}}/dns_records"

record_id="$(curl -fsS "$api?type=A&name=$server_name" \
  -H "Authorization: Bearer $token" | jq -r '.result[0].id // empty')"
payload="$(jq -nc --arg name "$server_name" --arg content "$server_ip" \
  '{{type:"A",name:$name,content:$content,ttl:300,proxied:false}}')"
if [[ -n "$record_id" ]]; then
  curl -fsS -X PUT "$api/$record_id" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" --data "$payload" >/dev/null
else
  curl -fsS -X POST "$api" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" --data "$payload" >/dev/null
fi

certbot certonly --manual --preferred-challenges dns \
  --manual-auth-hook '/usr/local/sbin/cloudflare-certbot-auth; sleep 70' \
  --manual-cleanup-hook /usr/local/sbin/cloudflare-certbot-cleanup \
  --disable-hook-validation --non-interactive --agree-tos \
  --cert-name creatornsk-services --expand \
  -d panel.creatornsk.ru -d hy.creatornsk.ru \
  -d reality.creatornsk.ru -d ws.creatornsk.ru -d xhttp.creatornsk.ru \
  -d sync.creatornsk.ru -d assets.creatornsk.ru -d media.creatornsk.ru \
  -d "$server_name"

site=/etc/nginx/sites-available/creator-services.conf
stream=/etc/nginx/stream-enabled/creator-reality.conf
stamp="$(date +%Y%m%d-%H%M%S)"
cp -a "$site" "$site.before-direct-sub-$stamp"
cp -a "$stream" "$stream.before-direct-sub-$stamp"
python3 - "$site" "$stream" "$server_name" "$route" "$source_file" <<'PY'
import pathlib
import sys

site_name, stream_name, host, route, source = sys.argv[1:]
site = pathlib.Path(site_name)
text = site.read_text()
marker = "# direct-subscription-host: " + host
if marker not in text:
    block = "\\n".join([
        "",
        marker,
        "server {{",
        "    listen 127.0.0.1:7443 ssl proxy_protocol;",
        "    http2 on;",
        "    server_name " + host + ";",
        "",
        "    ssl_certificate /etc/letsencrypt/live/creatornsk-services/fullchain.pem;",
        "    ssl_certificate_key /etc/letsencrypt/live/creatornsk-services/privkey.pem;",
        "    ssl_protocols TLSv1.2 TLSv1.3;",
        "",
        "    location = " + route + " {{",
        "        access_log off;",
        "        default_type text/plain;",
        '        add_header Cache-Control "no-store";',
        '        add_header Content-Disposition "inline";',
        "        alias " + source + ";",
        "    }}",
        "",
        "    location / {{ return 404; }}",
        "}}",
        "",
    ])
    site.write_text(text + block)

stream = pathlib.Path(stream_name)
text = stream.read_text()
entry = "    " + host + " creator_https;\\n"
if entry not in text:
    needle = "    panel.creatornsk.ru creator_https;\\n"
    text = text.replace(needle, needle + entry, 1)
stream.write_text(text)
PY

nginx -t
systemctl reload nginx
systemctl is-active nginx
printf 'URL=https://%s%s\\n' "$server_name" "$route"
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
