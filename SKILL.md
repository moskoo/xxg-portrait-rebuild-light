---
name: xxg-portrait-rebuild-light
description: "Edit an existing JPG, JPEG, PNG, or WebP portrait to rebuild physically coherent light and clean optical skin realism without changing the person. Use for plastic-skin or AI-look removal, texture-only fidelity enhancement, natural fill, backlight correction, soft window light or shadows, tree shadows, bokeh, golden-hour side backlight, neon, studio light, low-key beams, full-black silhouettes, or Higgsfield-Relight-like edits."
---

# XXG Portrait Rebuild Light V2

## Objective

Treat the input as the same photograph, never as a reference for a replacement portrait. Improve illumination and skin response while retaining identity, facial geometry and natural asymmetry, expression, pose, camera view, source optics, framing, and subject scale.

Build realism from three separable signals:

1. clean low-frequency skin tone and broad transitions;
2. source-driven diffuse/specular response with highlights confined to plausible light-facing areas;
3. fine, region-specific microdetail limited by face scale, focus, and illumination.

Do not manufacture realism with dirt, darkness, coarse pores, uniform grain, random color patches, or exaggerated facial lines. The result must first read as a clean photograph at normal size.

## Choose the Edit Scope

- **`texture-only`**: when the user asks only to remove plastic/AI skin or recover detail, force `L0 + T0 + A0`. Preserve the source lighting, highlight placement, exposure, white balance, focal plane, depth of field, and background.
- **`relight-and-skin`**: when the user requests a lighting change or selects L/T/A, authorize the requested light response while preserving source focal plane and depth of field unless explicitly changed.

Never let a texture-only request become a relight or a relight request become a simple color-temperature shift.

## Use the Host Image Editor

1. Inspect the source and read the host's native image-generation or image-editing skill.
2. Discover the actual callable in the tool registry. In Codex, inspect `ALL_TOOLS` and prefer the exact discovered name `image_gen__imagegen`.
3. For a local source in Codex, use the discovered tool and its real arguments:

```js
const result = await tools.image_gen__imagegen({
  referenced_image_paths: ["/absolute/path/source.png"],
  prompt: "compact four-line English image-edit prompt"
});
generatedImage(result);
```

Never guess `tools.image_gen` or `input_image`. Correct wrong members, arguments, or `TypeError` from the registered signature and retry. In Claude, OpenClaw, or another host, use the equivalent native image-edit action explicitly exposed by that host.

## Route the Outcome

| Observed state | Required action |
| --- | --- |
| Compatible image tool discovered | Invoke it. A small face, dense text, complex props, or edge contact lowers detail ambition but never blocks generation. |
| Correct image tool returns a real error | Report the actual error, enter `prompt-only`, and return a complete compact prompt. |
| Discovery completes with no compatible callable | Enter `invocation-handoff` and return a complete compact prompt. |
| Result is nearly unchanged, changes identity, creates artificial skin, or misses the light | State that the result did not achieve the requested improvement, enter `prompt-handoff`, and recompile from the source. |

Reading a skill, inspecting an image, creating a task, or announcing generation is not an image-tool invocation.

## Never Produce the Final Image Locally

Do not use Pillow, NumPy, OpenCV, ImageMagick, FFmpeg, `sips`, or custom raster scripts to relight, grade, retouch, sharpen, add texture, resize, crop, extend, composite, repair, or produce the delivered image. Use them only for read-only aspect-ratio, mask, and result audits. See `requirements.txt`.

## Compile the Image Prompt

Read [the V2 prompt compiler](references/prompt-recipes.md) and [the recipe library](references/lighting-skin-color-temperature-recipes.md). Decide internally as:

```text
Scope → Key → Exposure → Fill → Shadow → Skin scale → Skin finish → Background → Atmosphere
```

Select exactly:

```text
one L + one S + one P + one T + zero or one A
```

Use one key-light system. Atmosphere and skin reflections must inherit its direction, size, falloff, and color. `A6` is the sole override: force silhouette exposure, remove all subject fill/catchlights/internal illumination, use L/T only for the rear source and background, and suppress both S and P.

Send only four lines:

```text
EDIT: scope, identity/structure lock, and source-optics lock.
LIGHT: one key, exposure consequence, shadow transition, background response, color, and optional atmosphere.
SKIN: one scale-aware S behavior plus one source-consistent P finish.
AVOID: only the three or four failures most likely for this source.
```

- Target `45–95` English words; allow up to `125` for dense text or product scenes.
- State identity once. Treat the source itself as the identity card; do not invent a new age, personality, beauty description, lens, or aperture.
- Use positive, observable photographic behavior before negative constraints. Omit recipe codes, audits, confidence, backend notes, and reasoning.
- Keep default prompts free of realism-by-dirt terms: freckles, blemishes, blackheads, rough skin, color irregularity, film grain, gritty texture, under-eye lines, and high contrast. Preserve source-specific marks without naming or amplifying them.
- Use `deep`, `near-black`, or `hard contrast` only when the user explicitly selects backlight, hard light, low-key, neon, or silhouette behavior.
- On retry, replace the failed line instead of appending more instructions.

Every handoff must use this structure with no placeholders.

## Preserve the Identity Signature

Keep six source-defined groups stable: face outline/proportions; feature spacing, shape, and size; hairline, parting, and hair mass; source-identifying skin anchors; makeup/accessories; and apparent age/expression. Do not describe these groups in detail to the image model unless a real failure requires a shorter identity retry. Detailed identity checks belong in validation, not the generation prompt.

Under A6, internal features are intentionally hidden. Judge identity from hair/head/body outline, head-to-body ratio, pose, position, and framing.

## Apply Optical Skin Realism

- Keep overall skin color clean and continuous across face, ear, neck, and visible upper chest. Local transitions should be gentle and source-consistent, never patch-like.
- Use a diffuse base with small bounded specular highlights only on planes facing the selected key. Avoid a whole-face gloss layer and avoid removing all highlights.
- Vary surface detail by region: cheek pores softer, nose pores slightly clearer, lip texture separate, eye-area structure undisturbed. Do not tile one pore pattern across the face.
- Match detail to the source focus plane, depth of field, face size, and illumination. Never sharpen the whole face, every hair, clothing, and background equally.
- Preserve source-existing marks as identity anchors, but do not list or generate new imperfections by default.
- Preserve source skin tone; do not use `fair`, `whiter`, or beauty-grade language unless the user explicitly requests a complexion change.

## Apply Physical Light Without Unwanted Darkness

- Default unspecified edits to `source-matched` or `balanced`, with clean midtones and readable but directional shadow separation.
- Add fill only when the selected exposure requires information to remain readable. Do not flatten intended backlight, hard light, low-key, or silhouette.
- Derive shadow edge from apparent source size and distance. Carry direction, falloff, cast shadows, and reflected color across subject, clothing, nearby surfaces, and background.
- Keep window/tree shadows continuous across curvature and adjacent surfaces; keep bokeh only in optically defocused regions; require a visible or strongly inferred source for rays; give neon a clear primary and secondary source.
- Under A6, render the complete subject interior as one clean black mass. Permit only a narrow source-consistent rim that does not enter the silhouette.

## Preserve the Frame

Retain orientation, aspect ratio, composition, focal plane, depth of field, and subject-to-frame scale. A backend may downscale uniformly; exact pixel dimensions are not required. If a local result exists, run the read-only check:

```bash
python3 "$XXG_SKILL_DIR/scripts/check_aspect_ratio.py" SOURCE_IMAGE EDITED_IMAGE
```

Accept relative aspect-ratio drift of `≤5%`. Never resize, crop, pad, or extend locally to force a pass.

## Validate the Result

After generation, read [the V2 identity and detail audit](references/identity-and-detail-audit.md). At normal size first, verify:

1. the requested lighting change—or exact source-light preservation in `texture-only`—is immediately clear;
2. identity signature, pose, source optics, framing, and subject scale remain stable;
3. skin reads clean before microdetail becomes visible, with bounded highlights and no uniform gloss or texture overlay;
4. detail density follows facial region, focus, scale, and illumination rather than appearing equally sharp everywhere;
5. subject and environment share one physical light system; A6 remains a complete black interior.

If a result is nearly unchanged, strengthen one observable target. If skin becomes artificial, replace SKIN with `clean continuous source skin tone; bounded source-shaped highlights; faint region-specific microdetail only where focus and light resolve it`. Never present a failed image as final.

## Load References Only When Needed

- For every prompt: `references/prompt-recipes.md` and `references/lighting-skin-color-temperature-recipes.md`
- For tool routing, backend classification, or failure handling: `references/backend-and-clean-realism.md`
- After generation: `references/identity-and-detail-audit.md`
- Only for a verified strict local-edit backend: `references/edit-plan-and-protection.md`
