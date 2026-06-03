"""ReportBuilder: produces GATE_REPORT.md , gate_report.json , computes mechanical verdict + exit code."""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

from .config import ProjectContext
from .detector import detect_stack
from .registry import CheckResult, Status

BANNER = (
    "> **MECHANICAL GATE ONLY** — This report is **not** a substitute for the autonomous verifier "
    "`VERDICT: PASS` on the full Production Readiness Checklist (`PRODUCTION_CHECKLIST.md`). "
    "Phase 6 succeeds only when the verifier subagent declares production `VERDICT: PASS` with evidence for all applicable items."
)


def _status_to_md(status: Status) -> str:
    if status == Status.PASS:
        return "[x]"
    if status == Status.FAIL:
        return "[FAIL]"
    if status == Status.SKIP:
        return "[SKIP]"
    return "[ ]"  # MANUAL


def compute_mechanical_verdict(results: list[CheckResult], ctx: ProjectContext) -> tuple[str, int]:
    """Return (verdict_str, exit_code)."""
    has_strict_fail = False
    strict_ids = ("s03.", "s04.05", "s05.03")
    manual_pending = False
    for r in results:
        if r.status == Status.FAIL and any(r.check_id.startswith(p) for p in strict_ids):
            has_strict_fail = True
        if r.status == Status.MANUAL_REVIEW_REQUIRED:
            manual_pending = True
    if has_strict_fail:
        return "FAIL", 1
    if ctx.strict and manual_pending:
        return "MECHANICAL_PASS", 1
    return "MECHANICAL_PASS", 0


class ReportBuilder:
    def __init__(self, ctx: ProjectContext, results: list[CheckResult]):
        self.ctx = ctx
        self.results = results
        self.ds = detect_stack(ctx.project_path)
        self.verdict, self.exit_code = compute_mechanical_verdict(results, ctx)
        self.started_at = datetime.datetime.now(datetime.UTC).isoformat()
        self.finished_at = self.started_at

    def to_json(self) -> dict[str, Any]:
        checks = []
        for r in self.results:
            checks.append({
                "check_id": r.check_id,
                "section": r.section,
                "bullet": r.bullet,
                "status": r.status.value,
                "automatable": r.automatable,
                "evidence": r.evidence,
                "duration_ms": r.duration_ms,
                "message": r.message,
            })
        return {
            "schema_version": "1.0",
            "tool_version": "0.1.0",
            "project_path": str(self.ctx.project_path),
            "auton_id": self.ctx.auton_id,
            "profile": self.ctx.profile,
            "checklist_path": str(self.ctx.checklist_path),
            "checklist_sha256": self.ctx.checklist_sha256,
            "detected_stack": {"primary": self.ds.primary, "manifest": self.ds.manifest},
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "checks": checks,
            "mechanical_verdict": self.verdict,
            "exit_code": self.exit_code,
            "production_verdict": None,  # only by verifier subagent
        }

    def to_md(self) -> str:
        proj = self.ctx.project_path.name
        lines = []
        lines.append("## Production Readiness Gate Report (auton-gate — mechanical)")
        lines.append(BANNER)
        lines.append("")
        lines.append(f"**Project**: {proj}")
        lines.append(f"**AUTON_ID**: {self.ctx.auton_id or 'N/A'}")
        lines.append(f"**Profile**: {self.ctx.profile}")
        lines.append(f"**Checklist**: {self.ctx.checklist_path} (sha256:{self.ctx.checklist_sha256 or 'n/a'})")
        lines.append(f"**Date**: {self.started_at}")
        lines.append(f"**Detected stack**: {self.ds.primary} ({self.ds.manifest or 'n/a'})")
        lines.append("")
        lines.append("### Checklist Status (automated)")
        manuals: list[CheckResult] = []
        fails: list[CheckResult] = []
        for r in sorted(self.results, key=lambda x: (x.section, x.bullet, x.check_id)):
            md = _status_to_md(r.status)
            line = f"- {md} {r.check_id} {r.message}"
            lines.append(line)
            if r.status == Status.MANUAL_REVIEW_REQUIRED:
                manuals.append(r)
            if r.status == Status.FAIL:
                fails.append(r)
        lines.append("")
        if fails:
            lines.append("### FAILS")
            for r in fails:
                lines.append(f"- {r.check_id}: {r.message}")
                if r.evidence:
                    lines.append(f"  ```\n  {json.dumps(r.evidence, indent=2)[:800]}\n  ```")
            lines.append("")
        if manuals:
            lines.append("### Manual Review Required")
            for r in manuals:
                lines.append(f"- {r.check_id}: {r.message}")
            lines.append("")
        lines.append("### Evidence Summary")
        lines.append(f"- Total checks run: {len(self.results)}")
        lines.append(f"- PASS: {sum(1 for r in self.results if r.status == Status.PASS)}")
        lines.append(f"- FAIL: {sum(1 for r in self.results if r.status == Status.FAIL)}")
        lines.append(f"- MANUAL_REVIEW_REQUIRED: {sum(1 for r in self.results if r.status == Status.MANUAL_REVIEW_REQUIRED)}")
        lines.append(f"- SKIP: {sum(1 for r in self.results if r.status == Status.SKIP)}")
        lines.append("")
        lines.append(f"**Mechanical verdict:** VERDICT: {self.verdict}")
        lines.append("")
        lines.append("---")
        lines.append("*Generated by auton-gate. See docs/DESIGN.md and docs/INTEGRATION_AUTONOMOUS.md for Phase 6 usage.*")
        return "\n".join(lines)

    def write(self, output_dir: Path | None = None) -> tuple[Path, Path]:
        out = output_dir or self.ctx.output_dir
        out.mkdir(parents=True, exist_ok=True)
        md_path = out / "GATE_REPORT.md"
        json_path = out / "gate_report.json"
        md_path.write_text(self.to_md())
        json_path.write_text(json.dumps(self.to_json(), indent=2))
        return md_path, json_path
