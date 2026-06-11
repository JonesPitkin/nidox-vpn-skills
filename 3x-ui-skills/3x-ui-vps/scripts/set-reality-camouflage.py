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
        description="Change the target and server name of an existing Reality inbound."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--inbound-id", required=True, type=int)
    parser.add_argument("--server-name", required=True)
    args = parser.parse_args()

    target = shlex.quote(args.server_name + ":443")
    server_name = shlex.quote(args.server_name)
    inbound_id = int(args.inbound_id)
    remote = f"""#!/usr/bin/env bash
set -euo pipefail
target={target}
server_name={server_name}
stamp="$(date +%Y%m%d-%H%M%S)"
cp -a /etc/x-ui/x-ui.db "/etc/x-ui/x-ui.db.before-reality-sni-$stamp"
sqlite3 /etc/x-ui/x-ui.db <<SQL
BEGIN IMMEDIATE;
UPDATE inbounds SET stream_settings = json_set(
  stream_settings,
  '$.realitySettings.target', '$target',
  '$.realitySettings.serverNames', json_array('$server_name')
) WHERE id = {inbound_id}
  AND protocol = 'vless'
  AND json_extract(stream_settings, '$.security') = 'reality';
COMMIT;
SQL
python3 - "$server_name" <<'PY'
import base64
import pathlib
import sys

server_name = sys.argv[1]
path = pathlib.Path("/var/www/creatornsk/subscription.txt")
if path.exists():
    raw = base64.b64decode(path.read_bytes()).decode()
    lines = []
    for line in raw.splitlines():
        if "security=reality" in line:
            parts = line.split("&")
            parts = [
                "sni=" + server_name if part.startswith("sni=") else part
                for part in parts
            ]
            line = "&".join(parts)
        elif "type=xhttp" in line:
            parts = line.split("&")
            parts = [
                "sni=media.creatornsk.ru" if part.startswith("sni=") else part
                for part in parts
            ]
            line = "&".join(parts)
        lines.append(line)
    path.write_bytes(base64.b64encode(("\\n".join(lines) + "\\n").encode()))
PY
systemctl restart x-ui
sleep 2
/usr/local/x-ui/bin/xray-linux-amd64 run -test \
  -config /usr/local/x-ui/bin/config.json
systemctl is-active x-ui
sqlite3 -json /etc/x-ui/x-ui.db \
  "select id,stream_settings from inbounds where id={inbound_id};"
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
