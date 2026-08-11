#!/usr/bin/env python3
"""Measure exact pixel changes for the full frame and named rectangular regions."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


EXPECTED_TILES = {f"r{row}c{column}" for row in range(1, 4) for column in range(1, 4)}
REQUIRED_CAPABILITIES = {
    "preexisting_exposed_tool",
    "semantic_image_edit",
    "edit_mask",
    "frozen_pixel_passthrough",
    "exact_canvas",
    "local_result_file",
}


def parse_region(value: str) -> tuple[str, str, tuple[int, int, int, int]]:
    try:
        name, role, coords = value.split(":", 2)
        box = tuple(int(item) for item in coords.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use NAME:ROLE:X1,Y1,X2,Y2") from exc
    if role not in {"frozen", "editable", "observe"}:
        raise argparse.ArgumentTypeError("ROLE must be frozen, editable, or observe")
    if len(box) != 4 or box[0] < 0 or box[1] < 0 or box[2] <= box[0] or box[3] <= box[1]:
        raise argparse.ArgumentTypeError("Region coordinates must be a valid X1,Y1,X2,Y2 box")
    return name, role, box


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("edited", type=Path)
    parser.add_argument(
        "--region",
        action="append",
        default=[],
        type=parse_region,
        help="Repeatable NAME:ROLE:X1,Y1,X2,Y2; frozen regions require exact pixel identity",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Validated strict-final edit plan; all required protected items are audited automatically",
    )
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
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
    return mask.width * mask.height - mask.histogram()[0]


def item_mask(item: dict[str, object], base: Path, size: tuple[int, int]) -> Image.Image:
    if item.get("mask_path"):
        return binary_mask(resolve(base, str(item["mask_path"])), size)
    box = item.get("bbox")
    if not isinstance(box, list) or len(box) != 4:
        raise ValueError(f"Manifest item {item.get('id')} needs bbox or mask_path")
    x1, y1, x2, y2 = (int(value) for value in box)
    if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1 or x2 > size[0] or y2 > size[1]:
        raise ValueError(f"Manifest item {item.get('id')} has invalid bbox {box}")
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rectangle((x1, y1, x2 - 1, y2 - 1), fill=255)
    return mask


def metrics(source: Image.Image, edited: Image.Image) -> dict[str, object]:
    diff = ImageChops.difference(source, edited)
    histogram = diff.histogram()
    pixels = source.width * source.height
    total_abs = sum((index % 256) * count for index, count in enumerate(histogram))
    red, green, blue = diff.split()
    any_channel = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    unchanged = any_channel.histogram()[0]
    changed = pixels - unchanged
    return {
        "pixels": pixels,
        "changed_pixels": changed,
        "changed_percent": round(changed * 100.0 / pixels, 6),
        "mean_absolute_rgb_difference": round(total_abs / (pixels * 3), 6),
        "max_channel_difference": max(maximum for _, maximum in diff.getextrema()),
        "exact_match": changed == 0,
    }


def metrics_mask(source: Image.Image, edited: Image.Image, selection: Image.Image) -> dict[str, object]:
    selection = selection.point(lambda value: 255 if value > 0 else 0)
    selected_pixels = selection.width * selection.height - selection.histogram()[0]
    if selected_pixels == 0:
        raise ValueError("Protected mask contains zero pixels")
    diff = ImageChops.difference(source, edited)
    red, green, blue = diff.split()
    any_channel = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    any_changed = any_channel.point(lambda value: 255 if value > 0 else 0)
    changed = ImageChops.multiply(any_changed, selection)
    changed_pixels = changed.width * changed.height - changed.histogram()[0]
    selection_rgb = Image.merge("RGB", (selection, selection, selection))
    masked_diff = ImageChops.multiply(diff, selection_rgb)
    histogram = masked_diff.histogram()
    total_abs = sum((index % 256) * count for index, count in enumerate(histogram))
    return {
        "pixels": selected_pixels,
        "changed_pixels": changed_pixels,
        "changed_percent": round(changed_pixels * 100.0 / selected_pixels, 6),
        "mean_absolute_rgb_difference": round(total_abs / (selected_pixels * 3), 6),
        "max_channel_difference": max(maximum for _, maximum in masked_diff.getextrema()),
        "exact_match": changed_pixels == 0,
    }


def main() -> int:
    args = parse_args()
    with Image.open(args.source) as source_image, Image.open(args.edited) as edited_image:
        source = source_image.convert("RGB")
        edited = edited_image.convert("RGB")

    same_dimensions = source.size == edited.size
    manifest = None
    manifest_base = None
    required_ids: list[str] = []
    manifest_errors: list[str] = []
    if args.manifest:
        manifest_path = args.manifest.resolve()
        manifest_base = manifest_path.parent
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("delivery_mode") != "strict-final":
            manifest_errors.append("manifest delivery_mode must be strict-final")
        backend_raw = manifest.get("backend", {})
        backend = backend_raw if isinstance(backend_raw, dict) else {}
        if not isinstance(backend_raw, dict):
            manifest_errors.append("manifest backend must be an object")
        capabilities_raw = backend.get("capabilities", {})
        capabilities = capabilities_raw if isinstance(capabilities_raw, dict) else {}
        missing_capabilities = sorted(
            name for name in REQUIRED_CAPABILITIES if not capabilities.get(name, False)
        )
        if backend.get("classification") != "strict-local" or missing_capabilities:
            manifest_errors.append(
                f"manifest backend is not verified strict-local; missing {missing_capabilities}"
            )
        if manifest.get("inventory_complete") is not True:
            manifest_errors.append("manifest inventory_complete must be true")
        if manifest.get("inventory_method") != "full-frame-3x3-tile-sweep":
            manifest_errors.append("manifest inventory_method must be full-frame-3x3-tile-sweep")
        if set(manifest.get("reviewed_tiles", [])) != EXPECTED_TILES:
            manifest_errors.append("manifest reviewed_tiles must contain the complete 3x3 sweep")
        if manifest.get("source_size") != list(source.size):
            manifest_errors.append(
                f"manifest source_size {manifest.get('source_size')} does not match source {list(source.size)}"
            )
        items = manifest.get("protected_items", [])
        if not isinstance(items, list) or not items:
            manifest_errors.append("manifest protected_items must be non-empty")
        else:
            all_ids = [str(item.get("id", "")) for item in items if isinstance(item, dict)]
            if len(all_ids) != len(items) or not all(all_ids) or len(all_ids) != len(set(all_ids)):
                manifest_errors.append("all manifest items need unique non-empty ids")
            if manifest.get("protected_item_count") != len(items):
                manifest_errors.append("manifest protected_item_count must match protected_items")
            computed_counts = Counter(
                str(item.get("category", "")) for item in items if isinstance(item, dict)
            )
            inventory_counts = manifest.get("inventory_counts", {})
            if not isinstance(inventory_counts, dict):
                manifest_errors.append("manifest inventory_counts must be an object")
                inventory_counts = {}
            if dict(sorted(computed_counts.items())) != dict(sorted(inventory_counts.items())):
                manifest_errors.append("manifest inventory_counts must match protected_items")
            for item in items:
                if not isinstance(item, dict):
                    manifest_errors.append("manifest protected_items entries must be objects")
                    continue
                if item.get("protection") == "frozen" and item.get("required_audit") is not True:
                    manifest_errors.append(
                        f"frozen manifest item {item.get('id')} must set required_audit=true"
                    )
            editable = None
            protected = None
            for key in ("editable_mask", "protected_mask"):
                value = manifest.get(key)
                if not value:
                    manifest_errors.append(f"manifest {key} is required")
                    continue
                try:
                    loaded = binary_mask(resolve(manifest_base, str(value)), source.size)
                except (OSError, ValueError) as exc:
                    manifest_errors.append(str(exc))
                    continue
                if key == "editable_mask":
                    editable = loaded
                else:
                    protected = loaded
            if editable is not None and protected is not None:
                overlap_pixels = count_nonzero(ImageChops.multiply(editable, protected))
                if overlap_pixels:
                    manifest_errors.append(
                        f"manifest editable_mask overlaps protected_mask by {overlap_pixels} pixels"
                    )
            for item in items:
                if not isinstance(item, dict) or item.get("protection") != "frozen":
                    continue
                item_id = str(item.get("id", ""))
                try:
                    selection = item_mask(item, manifest_base, source.size)
                except (OSError, ValueError) as exc:
                    manifest_errors.append(f"{item_id}: {exc}")
                    continue
                if protected is not None:
                    missing_pixels = count_nonzero(
                        ImageChops.subtract(
                            selection,
                            ImageChops.multiply(selection, protected),
                        )
                    )
                    if missing_pixels:
                        manifest_errors.append(
                            f"frozen manifest item {item_id} is missing {missing_pixels} protected pixels"
                        )
                if editable is not None:
                    conflict_pixels = count_nonzero(ImageChops.multiply(selection, editable))
                    if conflict_pixels:
                        manifest_errors.append(
                            f"manifest editable_mask overlaps frozen item {item_id} by "
                            f"{conflict_pixels} pixels"
                        )
            required_ids = [
                str(item.get("id", ""))
                for item in items
                if isinstance(item, dict) and item.get("required_audit") is True
            ]
            if not all(required_ids) or len(required_ids) != len(set(required_ids)):
                manifest_errors.append("required manifest items need unique non-empty ids")
    report: dict[str, object] = {
        "source": str(args.source.resolve()),
        "edited": str(args.edited.resolve()),
        "source_size": list(source.size),
        "edited_size": list(edited.size),
        "same_dimensions": same_dimensions,
        "full_frame": None,
        "regions": [],
        "manifest": str(args.manifest.resolve()) if args.manifest else None,
        "manifest_required_ids": required_ids,
        "manifest_audited_ids": [],
        "manifest_complete": False,
        "manifest_errors": manifest_errors,
        "frozen_regions_exact": False,
        "pass": False,
    }
    if not same_dimensions:
        report["error"] = "Pixel-difference audit requires identical dimensions; run the size gate first."
    else:
        report["full_frame"] = metrics(source, edited)
        frozen_results: list[bool] = []
        audited_ids: list[str] = []
        if manifest is not None and manifest_base is not None:
            for item in manifest.get("protected_items", []):
                if item.get("required_audit") is not True:
                    continue
                item_id = str(item.get("id", ""))
                protection = item.get("protection")
                role = "frozen" if protection == "frozen" else "observe"
                try:
                    selection = item_mask(item, manifest_base, source.size)
                    region_metrics = metrics_mask(source, edited, selection)
                except (OSError, ValueError) as exc:
                    manifest_errors.append(f"{item_id}: {exc}")
                    continue
                region_metrics.update(
                    {
                        "name": item_id,
                        "role": role,
                        "category": item.get("category"),
                        "box": item.get("bbox"),
                        "mask_path": item.get("mask_path"),
                        "source": "manifest",
                    }
                )
                if role == "frozen":
                    region_metrics["pass"] = region_metrics["exact_match"]
                    frozen_results.append(bool(region_metrics["exact_match"]))
                else:
                    region_metrics["pass"] = None
                report["regions"].append(region_metrics)
                audited_ids.append(item_id)
        for name, role, box in args.region:
            if box[2] > source.width or box[3] > source.height:
                raise SystemExit(f"Region {name} exceeds image bounds {source.size}: {box}")
            region_metrics = metrics(source.crop(box), edited.crop(box))
            region_metrics.update({"name": name, "role": role, "box": list(box), "source": "cli"})
            if role == "frozen":
                region_metrics["pass"] = region_metrics["exact_match"]
                frozen_results.append(bool(region_metrics["exact_match"]))
            else:
                region_metrics["pass"] = None
            report["regions"].append(region_metrics)
        manifest_complete = (
            manifest is not None
            and not manifest_errors
            and set(audited_ids) == set(required_ids)
            and bool(required_ids)
        )
        report["manifest_audited_ids"] = audited_ids
        report["manifest_complete"] = manifest_complete
        report["manifest_errors"] = manifest_errors
        report["frozen_regions_exact"] = bool(frozen_results) and all(frozen_results)
        report["pass"] = manifest_complete and bool(frozen_results) and all(frozen_results)

    serialized = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0 if report["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
