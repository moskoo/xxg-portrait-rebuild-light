---
name: xxg-portrait-rebuild-light
description: "Relight an existing JPG, JPEG, PNG, or WebP portrait and rebuild clean photographic skin response without changing the person. Use for realistic skin recovery, plastic-skin removal, natural fill, backlight correction, soft window light or shadows, tree shadows, bokeh, golden-hour side backlight, neon, studio soft light, low-key light beams, full-black silhouettes, or Higgsfield-Relight-like image edits."
---

# XXG Portrait Rebuild Light

## Objective

Treat the input as the same photograph, not as a reference for a replacement image. Change illumination and material response while:

- retaining identity, natural facial asymmetry, facial geometry, expression, pose, camera view, framing, and subject scale;
- using one physically coherent key light to drive the subject, clothing, nearby surfaces, and background;
- rendering illuminated skin as clean and healthy, with low-contrast camera-resolved microtexture appropriate to the visible face scale.

The requested change must be visible at normal viewing size. Do not flatten backlight, low-key light, hard light, or silhouette exposure merely to keep every detail readable.

## Use the Host Image Editor

1. Inspect the source image and read the host's native image-generation or image-editing skill.
2. Discover the actual callable in the tool registry. In Codex, inspect `ALL_TOOLS` and prefer the exact discovered name `image_gen__imagegen`.
3. For a local source image in Codex, use only the discovered tool and its real arguments:

```js
const result = await tools.image_gen__imagegen({
  referenced_image_paths: ["/absolute/path/source.png"],
  prompt: "compact four-line English image-edit prompt"
});
generatedImage(result);
```

Never guess `tools.image_gen` or `input_image`. A wrong member name, argument, or `TypeError` is a dispatch error: correct the call from the registered signature instead of declaring the image tool unavailable. In Claude, OpenClaw, or another host, use the equivalent native image-edit action explicitly exposed by that host.

## Route the Outcome

| Observed state | Required action |
| --- | --- |
| Compatible image tool discovered | Invoke it. A small face, dense text, complex props, or a subject touching frame edges lowers detail ambition but never blocks generation. |
| Correct image tool returns a real error | Report the actual error, enter `prompt-only`, and return a complete compact prompt. |
| Discovery completes with no compatible callable | Enter `invocation-handoff` and return a complete compact prompt. |
| Generated result is nearly unchanged, changes identity, dirties skin, or misses the lighting design | State that the result did not achieve the requested improvement, enter `prompt-handoff`, and recompile from the source image. |

Reading a skill, inspecting an image, creating a task, or saying that generation is starting does not count as an image-tool invocation.

## Never Produce the Final Image Locally

Do not use Pillow, NumPy, OpenCV, ImageMagick, FFmpeg, `sips`, or custom raster scripts to relight, grade, retouch, sharpen, add texture, resize, crop, extend, composite, repair, or otherwise produce the delivered image. Use them only for read-only aspect-ratio, mask, and result audits. See `requirements.txt`.

## Compile the Image Prompt

Read [the prompt compiler](references/prompt-recipes.md) and [the lighting recipes](references/lighting-skin-color-temperature-recipes.md). Decide internally in this order:

```text
Key → Exposure → Fill → Shadow → Subject → Background → Atmosphere
```

Select exactly:

```text
one L + one S + one T + zero or one A
```

Use one key-light system. Any atmosphere must inherit that key's direction, color logic, and exposure. `A6` is the sole override: force silhouette exposure, place the effective source behind the subject, remove fill/catchlights/internal illumination, render the entire subject interior black, use L/T only for the backlight and background, and suppress S.

Send only four lines to the image model:

```text
EDIT: identity and structural invariants.
LIGHT: key, exposure, shadow behavior, background response, color temperature, and optional atmosphere.
SKIN: one scale-appropriate S target; replace with black interior for A6.
AVOID: the four highest-risk failure modes for this image.
```

- Target `40–90` English words; allow up to `120` for dense text or product scenes.
- State the identity lock once and name no more than three protected object categories.
- Describe visible photographic outcomes; omit recipe codes, audits, confidence, backend notes, and reasoning.
- Do not stack synonyms or use “change nothing,” “minimal pixel change,” or equivalent language that suppresses the edit.
- On retry, replace the failed line instead of appending more constraints.

Every handoff must use the same four-line structure with no placeholders.

## Edit Envelope

- **Structural invariants:** identity; face/head shape and ratio; feature position and size; natural asymmetry; expression; gaze; hairline; pose; camera perspective; composition; and subject-to-frame scale. Never beautify, idealize, or symmetrize.
- **Authorized appearance changes:** source-consistent luminance, reflection, cast shadow, color temperature, and requested atmosphere across skin, hair, clothing, and nearby background surfaces.
- **A6 exception:** internal facial detail is intentionally hidden. Judge preservation from the hair/head/body outline, head-to-body ratio, pose, position, and framing.

## Photographic Priors

- Choose S0/S1/S2 by visible face height. Skin must read clean and continuous at normal size; low-contrast, nonrepeating microtexture should appear only on closer inspection. Preserve blackheads, moles, powder separation, and similar details only when they already exist in the source.
- Add fill only when the exposure intent requires readable shadows. Low-key, highlight-priority, and silhouette treatments may use no fill.
- Derive shadow hardness from apparent source size and distance. Subject, clothing, nearby surfaces, and background must share direction, falloff, and reflected color.
- Window or tree shadows must cross subject curvature and nearby surfaces; bokeh belongs only in optically defocused regions; light rays require a directional source and visible medium; neon needs a clear primary and secondary color source.
- Under A6, suspend visible skin goals. Face, skin, hair, clothing, accessories, and body interior must form one clean black mass with no facial light, skin color, catchlight, hair strands, or garment texture. Permit only a very narrow source-consistent rim that does not enter the silhouette.

## Preserve the Frame

Retain orientation, aspect ratio, composition, and subject-to-frame scale. A backend may downscale uniformly; exact pixel dimensions are not required. If a local result file exists, perform this read-only check:

```bash
python3 "$XXG_SKILL_DIR/scripts/check_aspect_ratio.py" SOURCE_IMAGE EDITED_IMAGE
```

Accept relative aspect-ratio drift of `≤5%`. Never resize, crop, pad, or extend locally to force a pass.

## Validate the Result

After generation, read [the identity and detail audit](references/identity-and-detail-audit.md). At normal viewing size, verify:

1. the requested key, exposure, and atmosphere are immediately legible and physically coherent;
2. identity, geometry, pose, and composition remain stable; for A6, inspect outline, proportions, and pose;
3. illuminated skin is clean and photographic, without added grain, mottling, or fake sculpting; for A6, inspect the continuous black interior;
4. subject and background share the same light logic, with plausible placement for window/tree shadows, bokeh, neon, flare, or light rays;
5. orientation, aspect ratio, and subject scale remain stable; uniform downscaling is acceptable.

If the result is nearly unchanged, strengthen the single key and one observable outcome. If skin becomes dirty, replace the SKIN line with `clean continuous skin tone with low-contrast reflective microtexture`. Never present a failed image as the final result.

## Load References Only When Needed

- For every prompt: `references/prompt-recipes.md` and `references/lighting-skin-color-temperature-recipes.md`
- For tool routing, backend classification, or failure handling: `references/backend-and-clean-realism.md`
- After generation: `references/identity-and-detail-audit.md`
- Only for a verified strict local-edit backend: `references/edit-plan-and-protection.md`
