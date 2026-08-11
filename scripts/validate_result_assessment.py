#!/usr/bin/env python3
"""Validate reported target evidence and select accept-image or prompt-handoff delivery."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("assessment", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def main() -> int:
    args = parse_args()
    plan_raw = json.loads(args.plan.read_text(encoding="utf-8"))
    plan = plan_raw if isinstance(plan_raw, dict) else {}
    assessment_path = args.assessment.resolve()
    assessment_raw = json.loads(assessment_path.read_text(encoding="utf-8"))
    assessment = assessment_raw if isinstance(assessment_raw, dict) else {}
    targets = plan.get("perceptual_targets", [])
    if not isinstance(targets, list):
        targets = []
    required = {
        str(target["id"])
        for target in targets
        if isinstance(target, dict) and target.get("required") is True and target.get("id")
    }
    results = assessment.get("target_results", [])
    errors: list[str] = []
    if not isinstance(plan_raw, dict):
        errors.append("edit plan must be a JSON object")
    if not isinstance(assessment_raw, dict):
        errors.append("assessment must be a JSON object")
    if not required:
        errors.append("edit plan has no required perceptual targets")
    if not isinstance(results, list):
        errors.append("target_results must be a list")
        results = []
    result_ids = [str(result.get("id", "")) for result in results if isinstance(result, dict)]
    if len(result_ids) != len(results) or len(result_ids) != len(set(result_ids)):
        errors.append("target_results must contain exactly one object per unique id")
    by_id = {
        str(result.get("id", "")): result
        for result in results
        if isinstance(result, dict)
    }
    if set(result_ids) != required:
        errors.append(f"target_results ids must exactly match required targets: {sorted(required)}")
    for target_id in sorted(required):
        result = by_id.get(target_id, {})
        if result.get("status") != "pass":
            errors.append(f"target {target_id} status is not pass")
        if not result.get("finding"):
            errors.append(f"target {target_id} needs a concrete finding")
        evidence = result.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"target {target_id} needs at least one evidence file")
        else:
            for value in evidence:
                path = resolve(assessment_path.parent, str(value))
                if not path.exists():
                    errors.append(f"target {target_id} evidence does not exist: {path}")
    report = {
        "plan": str(args.plan.resolve()),
        "assessment": str(assessment_path),
        "required_targets": sorted(required),
        "errors": errors,
        "pass": not errors,
        "failed_targets": sorted(
            target_id
            for target_id in required
            if by_id.get(target_id, {}).get("status") != "pass"
        ),
        "delivery_action": (
            "accept_image" if not errors else "notify_and_output_complete_prompt"
        ),
        "validation_scope": (
            "This script validates the assessment record and evidence paths; the agent must "
            "perform an honest normal-view visual comparison and must not infer visual success "
            "from this script alone."
        ),
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
