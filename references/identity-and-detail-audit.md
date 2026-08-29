# V2 Identity, Skin, Light, and Optics Validation

## Contents

[Evidence](#evidence-record) · [Strict protection](#strict-protection-gate) · [Face scale](#face-scale-gate) · [Identity](#identity-signature-gate) · [Skin](#skin-realism-gate) · [Focus](#focus-and-detail-distribution-gate) · [Lighting](#lighting-gate) · [Framing](#aspect-ratio-and-composition-gate) · [Improvement](#target-improvement-gate)

## Evidence Record

Follow [the backend contract](backend-and-clean-realism.md). When a result exists, inspect source/result at normal full-frame size, same normalized face regions, side-by-side `200%–400%` views, and original result files for aspect ratio. Do not locally resize either image for comparison; uniform backend downscaling is acceptable.

```yaml
source_size: [W, H]
operation_scope: texture-only | relight-and-skin
face_box: [x1, y1, x2, y2]
face_top_y: y_top
chin_y: y_chin
face_height_px: y_chin - y_top
face_height_ratio: face_height_px / H
recipes:
  lighting: L0
  skin_scale: S1
  skin_finish: P0
  color_temperature: T0
  atmosphere: A0
light:
  mode: match-source | relight
  exposure_intent: source-matched | balanced | highlight-priority | shadow-priority | low-key | silhouette | high-key
  fill_policy: none | ambient-reflection | explicit-fill
  shadow_policy: retained-detail | dramatic-clean | silhouette
  highlight_policy: retained | soft-rolloff | controlled-clipping
  confidence: low | medium | high
  evidence: [{type, object, observation}]
  contradictions: []
optics:
  focal_plane_preserved: true
  depth_of_field_preserved: true
```

Compute `face_height_px` by coordinate subtraction and reuse normalized audit regions. Derive light confidence from evidence: `low` uses `match-source`, `medium` permits low-amplitude correction, and `high` permits explicit relighting.

## Strict Protection Gate

Use [the edit plan](edit-plan-and-protection.md) only for verified `strict-local`. Require all nine inventory tiles, item-level protection, matching counts, every frozen item in the union mask, and zero editable/protected overlap. Run `scripts/validate_edit_plan.py`. On failure, continue as `best-effort` rather than refusing.

## Face-Scale Gate

| Visible face height | Evaluated detail |
| --- | --- |
| `≥512 px` | Fine regional pores, natural lip texture, sparse focus-resolved vellus detail, and bounded reflections. |
| `256–511 px` | Faint regional microdetail, clean lip/eye boundaries, and local reflective variation. |
| `<256 px` | Continuous tone, broad illumination, and natural reflection; surface microdetail is not a target. |

Never demand detail the source scale cannot resolve.

## Identity Signature Gate

Compare six source-defined groups:

| Group | Compare |
| --- | --- |
| Face outline | Jawline, face width, forehead/head ratio, cheek/chin contour. |
| Feature geometry | Eye spacing/aperture/lids, brow shape, nose bridge/alae/tip, lip boundary/opening and feature size/placement. |
| Hair signature | Hairline, parting, fringe, hair mass, braid/loose-strand layout. |
| Skin anchors | Source-existing identifying marks and lip/eye-area structure, without requiring newly visible imperfections. |
| Fixed styling | Makeup boundaries, glasses, earrings, accessories, and wardrobe identity. |
| Age/expression | Apparent age, gaze, lid/mouth tension, expression, and overall demeanor. |

Fail any idealization, symmetry correction, boundary/size/placement change, or reconstructed identity. Under A6, internal features are intentionally hidden; compare hair/head/body outline, head-to-body ratio, pose, placement, and framing instead.

## Skin Realism Gate

Judge broad tone before zoomed texture:

| Signal/region | Pass | Fail |
| --- | --- | --- |
| Face-neck color | Clean source complexion with gentle continuous transitions across ear, neck, and visible chest. | Patch-like hue/luminance changes, local whitening, or face-neck separation. |
| Forehead/nose | Small bounded highlights that match key direction and P profile; detail appropriate to scale. | One continuous shine layer, fixed plastic highlight, or overdefined pore pattern. |
| Cheeks/jaw | Softer diffuse response, visible tonal shape, and lower surface contrast than the nose. | Flat smoothing, equally shiny cheeks, texture overlay, or locally burned contour. |
| Eye area | Original lids and tonal transition remain clean; no newly emphasized surface detail. | Darkened lines, invented bags/wrinkles, or changed lid geometry. |
| Lips | Original shape/color with separate natural lip texture when resolved. | Reshaping, enlargement, or skin texture copied onto lips. |
| Makeup | Original boundaries, color, and intensity remain. | Heavier/redesigned makeup or changed complexion. |

At normal size, skin must read clean, continuous, and dimensional before any microdetail is noticed. At closer view, detail must be faint, regional, nonrepeating, and optical—not a surface layer. Under A6, mark skin targets `not-applicable-by-design` and require one clean black interior.

## Focus and Detail Distribution Gate

- Preserve the source focal plane and depth of field unless the user explicitly requests an optical change.
- Highest detail belongs only on in-focus, adequately illuminated regions. Let detail reduce naturally with distance, shadow, curvature, and defocus.
- Fail equally crisp pores across the entire face, every hair strand sharply separated, oversharpened clothing/background, artificial blur, or cutout edges.
- In `texture-only`, any focus relocation, background change, global sharpening, or altered bokeh fails.

## Lighting Gate

- In `texture-only`, preserve source highlight placement, exposure, white balance, shadow transition, subject/environment response, and atmosphere.
- In `relight-and-skin`, catchlight; nose/eye-socket/cheek/jaw/neck shadows; hair; clothing; and background must agree with one source system.
- Lighting may change luminance/reflection but may not move feature boundaries or sculpt the face through localized line darkening.
- Default/ambiguous relight should preserve luminous midtones under `source-matched` or `balanced`. Dramatic shadow loss passes only when the user explicitly selected a compatible recipe.
- A6 requires `fill_policy: none` and one black interior; any internal feature, skin color, catchlight, lit hair, garment texture, or accessory shading fails.

## Aspect-Ratio and Composition Gate

Run `scripts/check_aspect_ratio.py`. Relative aspect-ratio drift of `≤5%` passes. Accept edge rounding and uniform downscaling; do not compare absolute dimensions. Fail stretching, orientation change, crop/extension, ratio drift above tolerance, altered camera view, or changed subject position/scale. Never repair framing locally.

## Strict Pixel Audit

Only for a same-size `strict-local` result, run:

```bash
python3 "$XXG_SKILL_DIR/scripts/audit_pixel_regions.py" SOURCE EDITED \
  --manifest EDIT_PLAN.json --output pixel-audit.json
```

Fail a missing plan, incomplete inventory/count, mask overlap, omitted `required_audit`, or changed frozen pixel. For uniform downscaling, skip pixel differencing and use `best-effort` visual validation.

## Target-Improvement Gate

Define `acceptance_view` and `acceptance_criterion` before generation. Afterward, record `pass`, an observation, and evidence. Improvement must be visible at the specified normal view; a difference map or extreme zoom is insufficient.

- `texture-only`: source light/optics remain stable; plastic smoothness is replaced by bounded reflection and scale/focus-aware regional detail.
- `relight-and-skin`: requested direction, exposure consequence, background response, and skin reflectance are immediately legible and coherent.
- Fail whole-face gloss, fully dead-matte flattening, texture overlay, uniform sharpness, unintended dimming, complexion change, or identity drift.
- A6: require a black interior plus original outline, proportions, pose, and placement.

For strict results, run `scripts/validate_result_assessment.py`. Any required target marked `fail` or `not_verifiable`, missing evidence, or omitted assessment enters `prompt-handoff`.

## Final Decision

Any applicable failure in identity signature, light/scope, skin realism, focus distribution, framing, frozen regions, or target improvement disqualifies the image. State `This image did not achieve the requested improvement` and return a compact prompt recompiled from source. Never present or locally repair a failed image.
