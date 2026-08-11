#!/usr/bin/env python3
"""Choose strict-local or non-blocking best-effort portrait editing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_REGISTRY = Path(__file__).resolve().parent.parent / "references" / "backend-capabilities.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", required=True, help="Profile id in backend-capabilities.json")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--face-height", type=int, required=True)
    parser.add_argument(
        "--delivery-mode",
        choices=("strict-final", "best-effort", "diagnostic-preview"),
        default="strict-final",
    )
    parser.add_argument("--complex-scene", action="store_true")
    parser.add_argument("--protected-text-or-product", action="store_true")
    parser.add_argument("--multiple-people", action="store_true")
    parser.add_argument("--subject-touches-edge", action="store_true")
    parser.add_argument(
        "--relight-requested",
        action="store_true",
        help="keep a visible medium lighting change even when skin detail or background redraw must stay low",
    )
    parser.add_argument(
        "--strong-light-requested",
        action="store_true",
        help="user explicitly requested a hard light, narrow beam, or similarly pronounced lighting effect",
    )
    parser.add_argument(
        "--explicit-preview-authorization",
        action="store_true",
        help="deprecated compatibility flag; best-effort fallback no longer requires a second authorization",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    profiles = registry.get("profiles", {})
    registered = args.backend in profiles
    profile = profiles.get(
        args.backend,
        {
            "classification": "unverified-full-frame-generative",
            "capabilities": {},
            "best_effort_allowed": True,
        },
    )
    required = registry["strict_local_required_capabilities"]
    capabilities = profile.get("capabilities", {})
    missing = [name for name in required if not capabilities.get(name, False)]
    strict_local = not missing

    flags = {
        "face_height_lt_256": args.face_height < 256,
        "complex_scene": args.complex_scene,
        "protected_text_or_product": args.protected_text_or_product,
        "multiple_people": args.multiple_people,
        "subject_touches_edge": args.subject_touches_edge,
    }
    risk_flags = [name for name in registry["full_frame_risk_flags"] if flags.get(name)]

    if strict_local:
        decision = "allow_strict_edit"
        effective_delivery_mode = "strict-final"
        reason = "All strict-local capabilities are present."
    else:
        decision = "allow_best_effort_edit"
        effective_delivery_mode = "best-effort"
        reason = (
            "Strict-local guarantees are unavailable, so continue with an identity-constrained full-frame edit "
            "and label the result as best-effort instead of refusing generation or collapsing to a no-op."
        )

    if args.strong_light_requested:
        lighting_strength = "strong-on-request"
    elif args.relight_requested:
        lighting_strength = "medium"
    else:
        lighting_strength = "source-matched"

    if args.face_height < 256:
        skin_detail_strength = "none"
    elif risk_flags:
        skin_detail_strength = "low"
    else:
        skin_detail_strength = "medium"

    result = {
        "schema_version": registry["schema_version"],
        "backend": args.backend,
        "backend_registered": registered,
        "classification": "strict-local" if strict_local else profile.get("classification"),
        "requested_delivery_mode": args.delivery_mode,
        "effective_delivery_mode": effective_delivery_mode,
        "missing_strict_capabilities": missing,
        "scene_flags": flags,
        "risk_flags_triggered": risk_flags,
        "recommended_lighting_strength": lighting_strength,
        "recommended_skin_detail_strength": skin_detail_strength,
        "minimum_visible_improvement_required": True,
        "decision": decision,
        "must_generate": True,
        "strict_guarantees_available": strict_local,
        "reason": reason,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
