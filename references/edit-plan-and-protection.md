# Strict Local Edit Plan and Protection Gate

Use this file only with a verified `strict-local` backend. Follow [the backend contract](backend-and-clean-realism.md) for delivery mode and invocation evidence. If strict capability is missing, continue as `best-effort`; do not create a fictional freeze plan.

## Full-Frame Inventory

Divide the frame into `r1c1`–`r3c3` and inspect all nine tiles before setting `inventory_complete: true`. Record each:

- eye/lid, brow, ala/nostril, lip boundary/corner, jaw, ear, and hairline;
- hair mass, braid, loose strand, garment, strap, accessory, hand, and pose boundary;
- book and visible text, computer/phone, cup, lamp, and product;
- door, table, chair, shelf, plant, wall, floor, window, and object touching a frame edge.

Record same-class objects separately with a unique `id`, description, tile, `bbox`, and optional `mask_path`. Build from [edit-plan-template.json](edit-plan-template.json). `protected_item_count` and `inventory_counts` must match the actual entries.

## Edit Plan

A strict plan contains: source dimensions for coordinate/same-size audit only; verified backend profile; nine-tile inventory; `editable_mask`; union `protected_mask`; actual exposure, fill, shadow, and highlight policy; and an acceptance view and criterion for every required perceptual target.

Only user-authorized objects may be marked `authorized-edit`; every other item is `frozen + required_audit`. For a full-frame `best-effort` edit, use instead:

- `structural_invariants`: identity geometry, composition, and object content;
- `authorized_appearance_changes`: skin reflection and continuous tone, target shadows, and scene-wide illumination response;
- `minimum_visible_improvement`: one result visible at normal full-frame viewing size.

A6 authorizes luminance, skin color, feature visibility, and hair/clothing/accessory surface detail inside the original subject outline to become black. Freeze the outline, proportions, pose, composition, and background. A strict A6 editable mask must cover the complete subject interior and stop at the original outline; do not darken only the face.

## Mask Gate

```bash
python3 "$XXG_SKILL_DIR/scripts/validate_edit_plan.py" EDIT_PLAN.json \
  --output edit-plan-validation.json
```

If any tile, count, backend capability, source dimension, frozen coverage, or editable/protected mask intersection fails, do not execute the strict plan. Correct it or continue as `best-effort`. A `bbox` protects its entire rectangle by default; provide an item mask when a tighter shape is required rather than shrinking the box around content.

## Frozen-Region Audit

Only for a same-size strict result, run:

```bash
python3 "$XXG_SKILL_DIR/scripts/audit_pixel_regions.py" SOURCE EDITED \
  --manifest EDIT_PLAN.json --output pixel-audit.json
```

The script revalidates the plan and automatically covers every `required_audit` item. A missing manifest, omitted item/audit, count mismatch, mask overlap, or changed frozen pixel cannot return strict PASS. For a uniformly downscaled result, skip pixel differencing and perform `best-effort` visual validation.

## Target Improvement

For every `perceptual_targets` item, record `status`, a concrete `finding`, and evidence from the full frame or specified zoom. Then run:

```bash
python3 "$XXG_SKILL_DIR/scripts/validate_result_assessment.py" \
  EDIT_PLAN.json RESULT_ASSESSMENT.json --output target-validation.json
```

Mark an almost unchanged result `fail`; a difference map or `restrained processing` does not establish improvement. For A6, require the complete subject interior to be continuous black with no facial feature, skin color, catchlight, lit hair strand, or garment texture, while outline, proportions, pose, position, and background remain stable. Mark ordinary skin-texture targets not applicable.

If any required target fails, enter `prompt-handoff`: report the failure and return a complete compact prompt recompiled from the source. Do not repair locally or present the failed image as final.
