"""Structured logging (stderr JSON lines optional).

v1: simple prints when --verbose. Future: --log-format json + structlog or stdlib.
No secrets in logs. Used by runner/checks for event=check_start etc.
"""

import json
import sys
from datetime import datetime


def log(event: str, **fields):
    rec = {"ts": datetime.utcnow().isoformat() + "Z", "event": event, **fields}
    # Always safe: never log file contents raw unless truncated evidence in reports
    sys.stderr.write(json.dumps(rec) + "\n")
    sys.stderr.flush()


def log_check_start(check_id: str, **fields):
    log("check_start", check_id=check_id, **fields)


def log_check_finish(check_id: str, status: str, duration_ms: int, **fields):
    log("check_finish", check_id=check_id, status=status, duration_ms=duration_ms, **fields)
