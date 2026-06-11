#!/usr/bin/env python3
import argparse
import secrets
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
        description="Assign one fresh subscription ID to all selected 3X-UI clients."
    )
    parser.add_argument("--host", required=True)
    parser.add_argument("--ssh-key", required=True)
    parser.add_argument("--client-email", action="append", required=True)
    parser.add_argument("--sub-id", default="")
    args = parser.parse_args()

    sub_id = args.sub_id or "main-" + secrets.token_hex(12)
    emails = ",".join(shlex.quote(email) for email in args.client_email)
    email_sql = ",".join("'" + email.replace("'", "''") + "'" for email in args.client_email)
    remote = f"""#!/usr/bin/env bash
set -euo pipefail
sub_id={shlex.quote(sub_id)}
stamp="$(date +%Y%m%d-%H%M%S)"
cp -a /etc/x-ui/x-ui.db "/etc/x-ui/x-ui.db.before-sub-id-$stamp"
sqlite3 /etc/x-ui/x-ui.db <<SQL
BEGIN IMMEDIATE;
UPDATE clients SET sub_id = '$sub_id', updated_at =
  CAST(strftime('%s','now') AS INTEGER) * 1000
WHERE email IN ({email_sql});
UPDATE inbounds
SET settings = json_set(settings, '$.clients[0].subId', '$sub_id')
WHERE json_extract(settings, '$.clients[0].email') IN ({email_sql});
COMMIT;
SQL
systemctl restart x-ui
sleep 2
/usr/local/x-ui/bin/xray-linux-amd64 run -test \
  -config /usr/local/x-ui/bin/config.json
systemctl is-active x-ui
sqlite3 -header -column /etc/x-ui/x-ui.db \
  "select id,email,sub_id,uuid from clients where email in ({email_sql}) order by id;"
printf 'SUB_ID=%s\\n' "$sub_id"
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
