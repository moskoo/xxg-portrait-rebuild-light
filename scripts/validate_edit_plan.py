#!/usr/bin/env python3
"""Validate a strict-local portrait edit plan and reject protected-mask overlap."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


REQUIRED_CAPABILITIES = {
    "preexisting_exposed_tool",
    "semantic_image_edit",
    "edit_mask",
    "frozen_pixel_passthrough",
    "exact_canvas",
    "local_result_file",
}
EXPECTED_TILES = {f"r{row}c{column}" for row in range(1, 4) for column in range(1, 4)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def binary_mask(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as image:
        mask = image.convert("L")
    if mask.size != size:
        raise ValueError(f"Mask {path} has size {mask.size}, expected {size}")
    return mask.point(lambda value: 255 if value > 0 else 0)


def count_nonzero(mask: Image.Image) -> int:
    histogram = mask.histogram()
    return mask.width * mask.height - histogram[0]


def item_mask(item: dict[str, object], base: Path, size: tuple[int, int]) -> Image.Image:
    if item.get("mask_path"):
        return binary_mask(resolve(base, str(item["mask_path"])), size)
    box = item.get("bbox")
    if not isinstance(box, list) or len(box) != 4:
        raise ValueError(f"Item {item.get('id')} needs bbox or mask_path")
    x1, y1, x2, y2 = (int(value) for value in box)
    if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1 or x2 > size[0] or y2 > size[1]:
        raise ValueError(f"Item {item.get('id')} has invalid bbox {box} for {size}")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
    return mask


def main() -> int:
    args = parse_args()
    plan_path = args.plan.resolve()
    base = plan_path.parent
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    overlaps: list[dict[str, object]] = []

    if plan.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if plan.get("delivery_mode") != "strict-final":
        errors.append("validate_edit_plan.py is for delivery_mode=strict-final")

    source_size_raw = plan.get("source_size")
    if not isinstance(source_size_raw, list) or len(source_size_raw) != 2:
        errors.append("source_size must be [W,H]")
        source_size = (0, 0)
    else:
        source_size = (int(source_size_raw[0]), int(source_size_raw[1]))

    source_value = plan.get("source_image")
    if not source_value:
        errors.append("source_image is required")
    else:
        source_path = resolve(base, str(source_value))
        if not source_path.exists():
            errors.append(f"source_image does not exist: {source_path}")
        elif source_size != (0, 0):
            with Image.open(source_path) as source:
                if source.size != source_size:
                    errors.append(f"source_size {source_size} does not match file size {source.size}")

    backend_raw = plan.get("backend", {})
    backend = backend_raw if isinstance(backend_raw, dict) else {}
    if not isinstance(backend_raw, dict):
        errors.append("backend must be an object")
    capabilities_raw = backend.get("capabilities", {})
    capabilities = capabilities_raw if isinstance(capabilities_raw, dict) else {}
    missing = sorted(name for name in REQUIRED_CAPABILITIES if not capabilities.get(name, False))
    if backend.get("classification") != "strict-local" or missing:
        errors.append(f"backend is not verified strict-local; missing capabilities: {missing}")

    if plan.get("inventory_complete") is not True:
        errors.append("inventory_complete must be true")
    if plan.get("inventory_method") != "full-frame-3x3-tile-sweep":
        errors.append("inventory_method must be full-frame-3x3-tile-sweep")
    reviewed_tiles = set(plan.get("reviewed_tiles", []))
    if reviewed_tiles != EXPECTED_TILES:
        errors.append(f"reviewed_tiles must contain exactly {sorted(EXPECTED_TILES)}")

    items = plan.get("protected_items", [])
    if not isinstance(items, list) or not items:
        errors.append("protected_items must be a non-empty list")
        items = []
    identifiers = [str(item.get("id", "")) for item in items if isinstance(item, dict)]
    if not all(identifiers) or len(identifiers) != len(set(identifiers)):
        errors.append("every protected item needs a unique non-empty id")
    if plan.get("protected_item_count") != len(items):
        errors.append("protected_item_count must equal len(protected_items)")
    computed_counts = Counter(str(item.get("category", "")) for item in items if isinstance(item, dict))
    inventory_counts = plan.get("inventory_counts", {})
    if not isinstance(inventory_counts, dict):
        errors.append("inventory_counts must be an object")
        inventory_counts = {}
    if dict(sorted(computed_counts.items())) != dict(sorted(inventory_counts.items())):
        errors.append("inventory_counts must exactly match protected_items categories")

    targets = plan.get("perceptual_targets", [])
    if not isinstance(targets, list):
        errors.append("perceptual_targets must be a list")
        targets = []
    target_ids = [str(target.get("id", "")) for target in targets if isinstance(target, dict)]
    if not targets or not all(target_ids) or len(target_ids) != len(set(target_ids)):
        errors.append("perceptual_targets must contain unique non-empty ids")
    for target in targets:
        if target.get("required") is True and (
            not target.get("acceptance_view") or not target.get("acceptance_criterion")
        ):
            errors.append(f"required target {target.get('id')} needs acceptance_view and acceptance_criterion")

    editable = None
    protected = None
    if source_size != (0, 0):
        for key in ("editable_mask", "protected_mask"):
            value = plan.get(key)
            if not value:
                errors.append(f"{key} is required")
                continue
            try:
                loaded = binary_mask(resolve(base, str(value)), source_size)
                if key == "editable_mask":
                    editable = loaded
                else:
                    protected = loaded
            except (OSError, ValueError) as exc:
                errors.append(str(exc))

    if editable is not None and protected is not None:
        overlap_pixels = count_nonzero(ImageChops.multiply(editable, protected))
        if overlap_pixels:
            errors.append(f"editable_mask overlaps protected_mask by {overlap_pixels} pixels")

    for item in items:
        if not isinstance(item, dict):
            errors.append("protected_items entries must be objects")
            continue
        item_id = str(item.get("id", ""))
        if not item.get("category") or not item.get("description"):
            errors.append(f"item {item_id} needs category and description")
        tile_ids = set(item.get("tile_ids", []))
        if not tile_ids or not tile_ids.issubset(EXPECTED_TILES):
            errors.append(f"item {item_id} needs valid tile_ids")
        protection = item.get("protection")
        if protection not in {"frozen", "authorized-edit"}:
            errors.append(f"item {item_id} protection must be frozen or authorized-edit")
        if protection == "frozen" and item.get("required_audit") is not True:
            errors.append(f"frozen item {item_id} must set required_audit=true")
        if protection == "authorized-edit" and not item.get("authorization"):
            errors.append(f"authorized-edit item {item_id} needs explicit authorization text")
        if source_size == (0, 0):
            continue
        try:
            current_item_mask = item_mask(item, base, source_size)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if protection == "frozen" and protected is not None:
            missing_from_union = count_nonzero(
                ImageChops.subtract(current_item_mask, ImageChops.multiply(current_item_mask, protected))
            )
            if missing_from_union:
                errors.append(f"frozen item {item_id} is missing {missing_from_union} pixels from protected_mask")
        if protection == "frozen" and editable is not None:
            conflict = count_nonzero(ImageChops.multiply(current_item_mask, editable))
            overlaps.append({"id": item_id, "editable_overlap_pixels": conflict})
            if conflict:
                errors.append(f"editable_mask overlaps frozen item {item_id} by {conflict} pixels")

    report = {
        "plan": str(plan_path),
        "delivery_mode": plan.get("delivery_mode"),
        "inventory_items": len(items),
        "reviewed_tiles_complete": reviewed_tiles == EXPECTED_TILES,
        "editable_protected_overlap": overlaps,
        "errors": errors,
        "pass": not errors,
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
