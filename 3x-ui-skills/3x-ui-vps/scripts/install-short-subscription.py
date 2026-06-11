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
        description="Install a short static subscription route in an existing nginx host."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--server-name", required=True)
    parser.add_argument("--route", required=True)
    parser.add_argument(
        "--source",
        default="/var/www/creatornsk/subscription.txt",
    )
    args = parser.parse_args()

    route = args.route if args.route.startswith("/") else "/" + args.route
    remote = f"""#!/usr/bin/env bash
set -euo pipefail
server_name={shlex.quote(args.server_name)}
route={shlex.quote(route)}
source_file={shlex.quote(args.source)}
config=/etc/nginx/sites-available/creator-services.conf
stamp="$(date +%Y%m%d-%H%M%S)"
cp -a "$config" "$config.before-short-sub-$stamp"
python3 - "$config" "$server_name" "$route" "$source_file" <<'PY'
import pathlib
import sys

config, server_name, route, source = sys.argv[1:]
path = pathlib.Path(config)
text = path.read_text()
location = "\\n".join([
    "",
    "    location = " + route + " {{",
    "        access_log off;",
    "        default_type text/plain;",
    '        add_header Cache-Control "no-store";',
    '        add_header Profile-Title "CreatorNSK";',
    '        add_header Profile-Update-Interval "12";',
    '        add_header Content-Disposition "inline";',
    "        alias " + source + ";",
    "    }}",
    "",
])
if f"location = {{route}}" not in text:
    marker = f"    server_name {{server_name}} xhttp.creatornsk.ru;\\n"
    if marker not in text:
        marker = f"    server_name {{server_name}};\\n"
    if marker not in text:
        raise SystemExit(f"server block not found for {{server_name}}")
    text = text.replace(marker, marker + location, 1)
path.write_text(text)
PY
nginx -t
systemctl reload nginx
curl -fsS -o /tmp/short-sub-check \
  -H "Host: $server_name" \
  --resolve "$server_name:7443:127.0.0.1" \
  --proxy-header "PROXY UNKNOWN" \
  "https://$server_name:7443$route" >/dev/null 2>&1 || true
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
