# V2.1 Compact Prompt Compiler

## Contents

[Contract](#output-contract) · [Scope](#scope-first) · [Compilation](#layer-compilation) · [Outcomes](#observable-outcomes) · [Production prompts](#production-prompts) · [Skin clauses](#skin-clauses) · [Safe wording](#priming-safe-wording) · [Failure rewrites](#replace-one-failed-layer)

## Output Contract

Describe one final photograph, not a conversation about editing. Use four lines when source color/capture remain unchanged; add RENDER only for a requested grade or device response.

```text
EDIT: {scope}; retain source identity, geometry, expression, pose, camera view, focal plane, depth of field, framing, and every unauthorized axis.
LIGHT: {L + E: source, direction, landing area, highlight/midtone/shadow/black behavior, environment response} {T} {optional A}.
RENDER: {G palette/curve + D capture response}; preserve source perspective and optics. [Omit for G0 + D0.]
SKIN: {S + P}; continuous source complexion, bounded key-shaped reflection, and regional detail limited by scale/focus/light.
AVOID: {only two or three source-specific failures}.
```

- Target `55–110` English words. Combined relight plus capture-style prompts may reach `135`; never exceed it.
- Select `one L + one E + one S + one P + one T + one G + one D + zero or one A` and copy behavior, never codes.
- State identity once. The attached source is the identity card; do not redescribe attractiveness, age, facial style, or imagined camera settings.
- Put positive, visible behavior first. Keep AVOID short and source-specific.
- On retry, replace the failed layer. Never append a second lighting setup, color look, device, or defect list.

### A6 Override

For A6, force E6. Remove subject-facing light, fill, catchlights, and internal highlights. Use L/T only for the rear source/background, suppress S/P, and write: `The entire subject interior is one continuous black silhouette; retain only the original outline, proportions, pose, and placement.` G/D may affect only the background.

## Scope First

| User intent | Required compilation |
| --- | --- |
| Skin realism only | `texture-only`; force `L0 + E0 + T0 + G0 + D0 + A0`; preserve source light, color, exposure, capture, focus, and scene. |
| Brightness, dynamic range, white balance, or grade only | `tone-and-exposure`; preserve L and source geometry/optics; change only requested E/T/G axes. |
| New lighting | `relight-and-skin`; apply L/E/T/A across subject and environment; preserve geometry and source optics. |
| Camera, film, phone, CCD, or era feel | `capture-style`; change G/D and only the E response the capture logically requires; preserve viewpoint/crop/focus/DOF. |
| New angle, focal perspective, aperture, or DOF | `optical-restyle`; state the requested optical consequence and allow only the reconstruction it requires. |

Ambiguous “make it cinematic/editorial/professional” requests are not permission to relight, recolor, and change optics together. Choose the smallest axis that produces the requested visible result.

## Layer Compilation

Read [lighting/skin recipes](lighting-skin-color-temperature-recipes.md) and [tone/exposure/style/device recipes](tone-exposure-style-device-recipes.md).

1. **EDIT** — scope and invariant photograph structure.
2. **LIGHT** — one physical L, one E tonal placement, one T source-color relationship, and optional A. Explicitly place highlights, midtones, shadows, and black point.
3. **RENDER** — one G palette/curve and one D capture response. Translate a camera name into tonal steps, highlight roll-off, color separation, microcontrast, sharpening, and dynamic range.
4. **SKIN** — one S scale plus one P reflection finish. D noise/grain never acts as skin texture.
5. **AVOID** — only failures not already prevented positively.

If the user names a camera brand without describing an effect, route it to the nearest device class and omit invented manufacturer color science. If the user supplies a film stock or exact look, retain the name once and still state its visible behavior.

## Observable Outcomes

| Request | Specify this result instead of a bare adjective |
| --- | --- |
| Correct exposure | Define highlight headroom, subject midtones, directional shadows, and black point; do not say only “balanced exposure.” |
| Change color tone | Define neutral references, skin-hue protection, warm/cool placement, saturation relationship, and contrast curve. |
| Editorial | One controlled curve, clean color separation, intentional light, and stable identity—not “premium cinematic 8K.” |
| Medium format | Smooth tonal steps, gradual highlight compression, restrained sharpening, rich controlled color separation. |
| Smartphone | Broad usable range, restrained local tone mapping and edge sharpening, neutral skin, no HDR halos. |
| 35mm negative | Gentle highlight compression, softer microcontrast, restrained film color; grain only when requested. |
| Point-and-shoot flash | One on-axis flash, compact highlights, clear subject exposure, rapid ambient falloff, casual framing retained. |
| Golden hour | Side-backlight defines hair/shoulders; exposure protects the rim, face follows available bounce, background carries the same warm direction. |

## Production Prompts

### Texture-Only Fidelity Recovery

```text
EDIT: Enhance skin fidelity only; retain source identity, facial geometry, expression, pose, focal plane, depth of field, light, color, camera view, and composition.
LIGHT: Preserve the photographed exposure, highlight map, shadow transitions, white balance, and background response.
SKIN: Keep continuous source complexion and natural satin response; render faint regional microdetail only where face scale, focus, and illumination resolve it.
AVOID: facial redesign, uniform facial shine, or repeated texture.
```

### Tone and Exposure Correction Without Relighting

```text
EDIT: Correct tone and exposure only; retain source identity, geometry, pose, light direction, camera view, focal plane, depth of field, objects, and composition.
LIGHT: Keep the existing source and shadow direction; protect bright-area shape, place facial midtones clearly, open only blocked shadows, and retain a stable clean black point.
RENDER: Neutralize the unwanted color cast while preserving skin hue, white reference objects, wardrobe color, and the source capture character.
SKIN: Preserve source reflectance and scale-resolved detail.
AVOID: flat HDR tone mapping or global color wash.
```

### Soft Window Naturalism

```text
EDIT: Relight this portrait; retain source identity, facial proportions, expression, pose, camera view, focal plane, depth of field, and composition.
LIGHT: Use one large window key above camera-left, with a broad left-to-right falloff across skin, clothing, and wall. Hold luminous facial midtones, smooth highlight headroom, separated soft shadows, and weak room bounce in neutral daylight.
SKIN: Use continuous source complexion, a soft-daylight finish, and faint focus-aware regional detail.
AVOID: identity drift, uniform shine, or scene redraw.
```

### Medium-Format Editorial Portrait

```text
EDIT: Relight and apply a medium-format editorial capture; retain source identity, facial geometry, expression, pose, viewpoint, focal plane, depth of field, framing, and scene structure.
LIGHT: Place one large soft key above camera-left for clear midtones, a short soft nose shadow, one catchlight, gentle far-cheek separation, and smooth highlight headroom.
RENDER: Use neutral editorial color with smooth tonal steps, gradual highlight compression, rich controlled color separation, restrained sharpening, and coherent focus transition.
SKIN: Keep bounded T-zone reflection and scale-aware optical detail.
AVOID: facial idealization or background reconstruction.
```

### Point-and-Shoot Direct Flash

```text
EDIT: Apply a clean point-and-shoot flash capture; retain source identity, facial geometry, expression, pose, viewpoint, focal plane, framing, and background structure.
LIGHT: Use one small on-axis flash. Expose the subject in clear midtones with compact separated highlights, firm clean blacks, and rapid ambient falloff behind the subject.
RENDER: Use neutral-to-cool highlight color, modest color punch, direct compact-camera microcontrast, and no added grain.
SKIN: Keep continuous complexion with flash-bounded reflection and only focus-resolved detail.
AVOID: full-face glare, crushed features, or cutout edges.
```

### 35mm Natural-Light Documentary

```text
EDIT: Apply a restrained 35mm color-negative documentary response; retain source identity, geometry, expression, pose, original light direction, viewpoint, focal plane, depth of field, and composition.
LIGHT: Preserve the available-light exposure pattern, readable subject midtones, directional shadows, and practical highlights.
RENDER: Use gentle highlight compression, slightly softened microcontrast, muted environmental saturation with stable skin chroma, and restrained film color separation; add no grain unless requested.
SKIN: Preserve source-shaped reflection and regional detail at the resolved scale.
AVOID: vintage color wash or artificial texture overlay.
```

### Smartphone Available-Light Portrait

```text
EDIT: Apply a natural smartphone computational capture; retain source identity, facial geometry, pose, camera view, focal plane, depth of field, crop, and scene content.
LIGHT: Preserve the existing source direction; keep facial midtones readable, bright sources shaped, shadows separated, and the black point stable.
RENDER: Use broad usable dynamic range, neutral skin color, restrained local tone mapping, and controlled edge sharpening while preserving the source depth transition.
SKIN: Keep continuous tone, bounded highlights, and detail limited by scale and focus.
AVOID: HDR halos, crunchy edges, or portrait-mode cutout blur.
```

### Golden-Hour Side Backlight

```text
EDIT: Relight this portrait; retain source identity, facial proportions, feature placement, pose, camera view, focal plane, depth of field, and composition.
LIGHT: Place warm sunset light behind and to one side, outlining hair and shoulders. Expose for the rim; derive camera-facing brightness from natural reflected fill, and align background warmth, long shadows, and one restrained flare with the source.
SKIN: Keep illuminated complexion continuous with bounded warm reflections and focus-aware regional detail.
AVOID: facial redesign, global orange wash, or detached halos.
```

### A6 Full-Black Silhouette

```text
EDIT: Relight this portrait; retain the subject's original outline, proportions, pose, placement, camera view, and composition.
LIGHT: Expose for one bright source behind the subject. Remove fill, catchlights, and internal illumination; render the complete subject as one continuous black silhouette while the background follows the rear source.
SKIN: No facial, skin, hair, clothing, accessory, or body detail is visible inside the silhouette.
AVOID: outline drift, gray interior fill, or residual facial light.
```

## Skin Clauses

### Scale S

| Recipe | Model-facing clause |
| --- | --- |
| S0 `<256 px` | Maintain continuous source complexion and natural light response; the visible face scale does not resolve added surface detail. |
| S1 `256–511 px` | Render faint regional microdetail only on illuminated in-focus skin; preserve clean eye-area and lip boundaries. |
| S2 `≥512 px` | Render fine camera-resolved detail: softer cheek pores, slightly clearer nose pores, natural lip texture, and sparse vellus detail only where source focus resolves it. |

### Finish P

| Recipe | Model-facing clause |
| --- | --- |
| P0 Source finish | Preserve source diffuse/specular balance and the exact location, area, and intensity of existing highlights. |
| P1 Natural satin-matte | Use a soft diffuse base with small bounded highlights on key-facing convexities; keep cheeks and eye area less reflective. |
| P2 Soft-daylight | Use luminous clean midtones, broad soft roll-off, and restrained highlights shaped by the window or sky source. |
| P3 Editorial satin | Keep controlled T-zone highlights, smooth cheek separation, and visible but low-amplitude optical detail. |
| P4 Direct flash | Keep compact flash-facing highlights with clear boundaries; do not connect them into a continuous facial shine. |
| P5 Clean beauty | Keep even broad color, natural three-dimensional reflection, and fine optical detail without porcelain smoothness. |
| P6 Available light | Preserve source-driven highlight placement and focus falloff without adding marks, grain, or stronger color variation. |

## Priming-Safe Wording

Do not put these shortcuts in a default generation prompt; compile the observable behavior instead.

| Risky shortcut | Safer behavior |
| --- | --- |
| real/ultra-real skin | Continuous source complexion + regional microdetail + bounded reflection. |
| visible/8K pores | `faint regional pores only where scale, focus, and light resolve them` |
| HDR | Name highlight, midtone, shadow, and black-point placement; use restrained local tone mapping only for D6. |
| cinematic/editorial/premium | Select one G and state its palette, saturation relationship, curve, and highlight behavior. |
| DSLR/medium format/smartphone/film | Select one D and state its tonal steps, dynamic range, microcontrast, sharpening, and noise behavior. |
| skin color variation | `continuous source-consistent complexion with gentle light-driven transitions` |
| freckles, blemishes, blackheads, imperfections | `preserve source-identifying skin anchors without adding or amplifying marks` |
| oily/dewy/wet skin | `small bounded specular highlights on key-facing convexities` |
| raw/coarse/gritty texture | `fine low-amplitude optical microdetail` |
| 8K, ultra-detailed, crisp everywhere | `detail follows source scale, focal plane, distance, and illumination` |

## Replace One Failed Layer

| Failure | Replacement strategy |
| --- | --- |
| Nearly unchanged | Replace only the requested LIGHT, RENDER, or SKIN layer with one stronger observable result. |
| Unchanged exposure | Specify highlight headroom, facial midtones, directional shadows, and black point. |
| Flat HDR result | Remove global recovery language; use E1 and preserve directional separation. |
| Style is only a tint | Add G curve and saturation behavior while protecting skin and neutral objects. |
| Device look is absent | Replace the device name with D tonal, highlight, microcontrast, sharpening, and dynamic-range behavior. |
| Device changes viewpoint | Restore source perspective/crop/focal plane/DOF; keep only capture response. |
| Plastic skin remains | Replace SKIN with continuous source complexion, bounded source-shaped highlights, and faint focus-aware regional detail. |
| Film look dirties skin | Remove grain/cast/imperfection terms; keep G/D tone response and let S/P define skin. |
| A6 retains interior detail | Remove S/P and all subject light; require one continuous black interior. |

## Forbidden Prompt Construction

- multiple devices, film stocks, eras, or grades in one prompt;
- bare quality/style stacks such as `premium, cinematic, ultra-real, 8K, highly detailed`;
- changing camera angle, focal perspective, crop, or depth of field without explicit optical-restyle intent;
- naming a camera brand without describing the capture response;
- global highlight recovery plus global shadow lifting;
- grain, noise, sharpening, or imperfections used as skin detail;
- competing key lights or a grade that recolors the full face;
- A6 combined with visible subject texture, catchlights, fill, or clothing detail.
