#!/usr/bin/env python3
"""Check only aspect-ratio similarity; proportional resolution changes are accepted."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="original portrait")
    parser.add_argument("edited", type=Path, help="edited portrait")
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.05,
        help="maximum relative aspect-ratio delta; default: 0.05 (5%%)",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    return parser.parse_args()


def read_ratio(path: Path) -> float:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        width, height = image.size
    if width <= 0 or height <= 0:
        raise ValueError(f"invalid image dimensions: {path}")
    return width / height


def main() -> int:
    args = parse_args()
    if not 0 <= args.tolerance <= 1:
        print("error: --tolerance must be between 0 and 1", file=sys.stderr)
        return 1

    try:
        source_ratio = read_ratio(args.source)
        edited_ratio = read_ratio(args.edited)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    relative_delta = abs(source_ratio - edited_ratio) / source_ratio
    within_tolerance = relative_delta <= args.tolerance
    payload = {
        "source": str(args.source),
        "edited": str(args.edited),
        "source_aspect_ratio": round(source_ratio, 8),
        "edited_aspect_ratio": round(edited_ratio, 8),
        "relative_aspect_ratio_delta": round(relative_delta, 8),
        "tolerance": args.tolerance,
        "within_tolerance": within_tolerance,
        "proportional_resolution_change_allowed": True,
        "operation": "read-only-aspect-ratio-check",
        "delivery_action": "accept_ratio_gate" if within_tolerance else "reject_ratio_gate",
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"source_aspect_ratio: {source_ratio:.6f}")
        print(f"edited_aspect_ratio: {edited_ratio:.6f}")
        print(f"relative_delta: {relative_delta:.2%}")
        print(f"tolerance: {args.tolerance:.2%}")
        print(f"within_tolerance: {str(within_tolerance).lower()}")
        print(f"delivery_action: {payload['delivery_action']}")

    return 0 if within_tolerance else 2


if __name__ == "__main__":
    raise SystemExit(main())
