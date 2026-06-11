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


def ssh(host: str, key: str, command: str) -> subprocess.CompletedProcess:
    return run(
        "ssh",
        "-i",
        key,
        "-o",
        "StrictHostKeyChecking=accept-new",
        host,
        command,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair an existing native 3X-UI XHTTP inbound for CDN clients."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--inbound-id", required=True, type=int)
    parser.add_argument("--database", default="/etc/x-ui/x-ui.db")
    parser.add_argument(
        "--mode",
        choices=("packet-up", "stream-one", "auto"),
        default="packet-up",
        help="Use packet-up for compatibility with Cloudflare and nginx proxy_pass.",
    )
    args = parser.parse_args()

    db = shlex.quote(args.database)
    inbound_id = int(args.inbound_id)
    mode = args.mode
    sql = f"""
BEGIN IMMEDIATE;
UPDATE inbounds
SET stream_settings = json_set(
  stream_settings,
  '$.xhttpSettings.mode', '{mode}',
  '$.externalProxy[0].alpn', json_array('h2')
)
WHERE id = {inbound_id}
  AND protocol = 'vless'
  AND json_extract(stream_settings, '$.network') = 'xhttp';
COMMIT;
"""
    command = (
        "set -e; "
        "stamp=$(date +%Y%m%d-%H%M%S); "
        f"cp -a {db} {db}.before-xhttp-repair-$stamp; "
        f"sqlite3 {db} {shlex.quote(sql)}; "
        f"python3 - {shlex.quote(mode)} <<'PY'\n"
        "import base64\n"
        "import pathlib\n"
        "import re\n"
        "import sys\n"
        "mode = sys.argv[1]\n"
        "path = pathlib.Path('/var/www/creatornsk/subscription.txt')\n"
        "if path.exists():\n"
        "    raw = base64.b64decode(path.read_bytes()).decode()\n"
        "    lines = []\n"
        "    for line in raw.splitlines():\n"
        "        if 'type=xhttp' in line:\n"
        "            line = re.sub(r'([?&]mode=)[^&#]+', r'\\1' + mode, line)\n"
        "        lines.append(line)\n"
        "    path.write_bytes(base64.b64encode(('\\n'.join(lines) + '\\n').encode()))\n"
        "PY\n"
        "systemctl restart x-ui; "
        "sleep 2; "
        "systemctl is-active x-ui; "
        "/usr/local/x-ui/bin/xray-linux-amd64 run -test "
        "-config /usr/local/x-ui/bin/config.json; "
        f"sqlite3 -json {db} "
        f"\"select id,stream_settings from inbounds where id={inbound_id};\""
    )
    result = ssh(args.host, args.ssh_key, command)
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
