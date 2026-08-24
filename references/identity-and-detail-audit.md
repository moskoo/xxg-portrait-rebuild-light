# Identity, Skin, and Result Validation

## Contents

[Evidence](#evidence-record) · [Strict protection](#strict-protection-gate) · [Face scale](#face-scale-gate) · [Identity](#identity-gate) · [Skin](#skin-gate) · [Lighting](#lighting-gate) · [Framing](#aspect-ratio-and-composition-gate) · [Improvement](#target-improvement-gate) · [Decision](#final-decision)

## Evidence Record

Follow [the backend contract](backend-and-clean-realism.md) for invocation and delivery status. When a result exists, inspect: source and result at full-frame normal size, same-coordinate face crops, side-by-side `200%–400%` views, and original result files for aspect-ratio checks. If dimensions differ, compare normalized positions without locally resizing either image. Uniform downscaling is not a failure.

Record only the minimum evidence:

```yaml
source_size: [W, H]
face_box: [x1, y1, x2, y2]
face_top_y: y_top
chin_y: y_chin
face_height_px: y_chin - y_top
face_height_ratio: face_height_px / H
audit_regions:
  face: [x1, y1, x2, y2]
  hair: [x1, y1, x2, y2]
  clothing: [x1, y1, x2, y2]
  background: [x1, y1, x2, y2]
light:
  mode: match-source | relight
  atmosphere_recipe: A0 | A1 | A2 | A3 | A4 | A5 | A6
  exposure_intent: source-matched | balanced | highlight-priority | shadow-priority | low-key | silhouette | high-key
  fill_policy: none | ambient-reflection | explicit-fill
  shadow_policy: retained-detail | deep-clean | near-black | silhouette
  highlight_policy: retained | soft-rolloff | controlled-clipping
  confidence: low | medium | high
  evidence: [{type, object, observation}]
  contradictions: []
```

Compute `face_height_px` by coordinate subtraction and reuse the same normalized audit regions before and after. Derive source confidence from consistent evidence: `low` uses `match-source`, `medium` permits only low-amplitude correction, and `high` permits explicit relighting.

## Strict Protection Gate

Use [the edit plan](edit-plan-and-protection.md) only for a verified `strict-local` backend. Require all nine inventory tiles, item-level protection, matching counts, every frozen item in the union protection mask, and zero overlap between editable and protected masks. Run `scripts/validate_edit_plan.py`. If validation fails, continue as `best-effort` rather than refusing.

## Face-Scale Gate

| Visible face height | Detail that can be evaluated |
| --- | --- |
| `≥512 px` | Low-contrast pores, vellus hair, shallow lines, lip texture, and restrained sebum reflection. |
| `256–511 px` | Restrained microtexture, lip texture, eye-area transitions, and local reflective variation. |
| `<256 px` | Continuous tone, broad illumination, and natural reflection; microtexture is not a hard target. |

Never demand pores the source cannot spatially resolve.

## Identity Gate

| Region | Compare |
| --- | --- |
| Eyes and brows | Eye aperture, corners, lids, iris placement, original left-right difference; brow head, arch, tail, and boundary. |
| Nose | Bridge, alar width, tip, nostril outline, and placement. |
| Lips | Cupid's bow, lip boundary, opening, corners, and upper-to-lower ratio. |
| Outer contour | Cheekbone, cheek, jaw, chin, ear, and hairline. |
| Expression | Gaze, lid tension, mouth-corner tension, and overall muscle state. |

Fail any reinterpretation of a visible boundary, opening, position, size, or feature into a more idealized version. Under A6, internal features are intentionally hidden; instead compare hair/head/ear/neck/limb outline, head-to-body ratio, pose, position, and framing. Black fill must not alter head shape, body proportions, or gesture.

## Skin Gate

Evaluate only visible source regions with sufficient resolution:

| Region | Pass | Fail |
| --- | --- | --- |
| Cheeks | Soft, sparse, low-contrast pore response following curvature. | Beauty smoothing, repeated pits, black-dot pores, or noise. |
| Nose and alae | Slightly crisper pores; source blackheads may remain. | Dirtiness, exaggerated black dots, or redrawn alae. |
| Forehead | Restrained sebum reflection and, when resolved, fine vellus hair. | Broad oily shine, plastic highlight, or uniform grain. |
| Under-eye | Source-appropriate shallow lines and tonal transition. | New eye bags, wrinkles, or lid-shape change. |
| Lips | Original boundary, color, and natural vertical texture. | Reshaped or enlarged lips, or a redrawn lip line. |
| Makeup | Original makeup; only source-existing powder separation remains. | New color, heavier makeup, powder debris, or mottling. |
| Neck/collarbone | Continuous exposed-skin tone and restrained reflection. | New exposure, patches, dark grooves, or invented texture. |

At normal size, skin must first read clean and continuous. Only at closer inspection should low-contrast, sparse, nonrepeating texture appear. Fail color mottling, muddy gray, local whitening, face-neck discontinuity, global grain, chroma noise, or sharpening grit. Enter `prompt-handoff`; never repair locally.

Do not fail a face `<256 px` because pores are absent. Under A6, mark skin regions `not-applicable-by-design` and instead require a continuous black interior with no color contamination, grain, gray patches, or residual facial light.

## Lighting Gate

- Catchlight; nose, eye-socket, cheek, jaw, and neck shadows; hair; clothing; and background must agree with one source system. Fail duplicate shadows, cutout rims, or disconnected illumination.
- Lighting may change luminance and reflection but may not move feature boundaries or reshape the face through localized darkening.
- Shadows, highlights, and fill must follow the exposure intent. `low-key` and `silhouette` may lose internal detail; `highlight-priority` may permit controlled clipping.
- Count dead black, discontinuity, or muddy shadow as loss only when it is unexplained under `source-matched` or `balanced` exposure.
- A6 requires `fill_policy: none` and a black interior. Any facial feature, skin color, catchlight, lit hair strand, garment texture, or accessory shading inside is a failure.

## Aspect-Ratio and Composition Gate

Run `scripts/check_aspect_ratio.py`. Relative aspect-ratio drift of `≤5%` passes. Accept edge rounding and uniform downscaling; do not compare absolute pixel dimensions. Fail stretching, orientation change, cropping/extension, ratio drift above tolerance, or altered subject position/scale. Never resize, crop, or pad locally to force a pass.

## Strict Pixel Audit

Only for a same-size `strict-local` result, run:

```bash
python3 "$XXG_SKILL_DIR/scripts/audit_pixel_regions.py" SOURCE EDITED \
  --manifest EDIT_PLAN.json --output pixel-audit.json
```

The script must cover every `required_audit` item. Fail a missing plan, incomplete inventory/count, mask overlap, omitted audit item, or changed frozen pixel. If the result was uniformly downscaled, skip pixel differencing and use `best-effort` visual validation.

## Target-Improvement Gate

Before generation, define `acceptance_view` and `acceptance_criterion` for each required target. After generation, record `pass`, an observation, and evidence. If improvement is invisible at the specified normal view, fail even when a difference map or extreme zoom reveals changes.

- Fail lighting that remains flat, contradictory, or nearly unchanged. Intentional low-key darkness, silhouette, or controlled bloom is not a defect.
- Fail skin that remains plastic or changes only in brightness/color temperature. Microtexture may be not applicable below `256 px`.
- For A6, skin microtexture is not applicable. Require a black interior plus the original outline, proportions, and pose; merely darkening the face, retaining interior detail, or using gray fill fails.

For a strict result, run `scripts/validate_result_assessment.py`. Any required target marked `fail` or `not_verifiable`, missing evidence, or omitted assessment enters `prompt-handoff`.

## Final Decision

Any applicable failure in identity, aspect ratio/composition, frozen regions/inventory, required targets, lighting, clean realism, or A6 disqualifies the image. State `This image did not achieve the requested improvement` and return a complete compact prompt recompiled from the source. Never present or locally repair a failed image. Deliver only after every applicable gate passes.
