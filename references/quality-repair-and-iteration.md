# V2.3 Clean-Frame Quality, Color Lock, and Iterative Repair

## Contents

[Protocol](#selection-protocol) · [Scopes](#repair-scopes) · [Inputs](#input-roles) · [Zones](#semantic-zones) · [Recipes](#quality-recipes-q) · [Iteration](#multi-round-editing) · [Prompt line](#quality-line) · [Validation](#quality-validation) · [Failure repair](#failure-repair)

## Selection Protocol

Quality repair is a separate axis from light, exposure, grade, capture response, skin finish, and atmosphere. Select exactly one Q and compile its behavior into one `QUALITY:` line. Default to Q0.

```text
one L + one E + one S + one P + one T + one G + one D + zero or one A + one Q
```

Q may remove a generation defect but may not redesign the person, flatten real material texture, move the focal plane, alter the selected light, or undo an intentional E/T/G/A change. Name only defects visible in the source; never add a generic defect list.

## Repair Scopes

| Scope | Authorized change | Locked by default |
| --- | --- | --- |
| `quality-repair` | One Q repair on the current image | Identity, geometry, expression, pose, light, exposure, grade, optics, framing, objects, and all natural texture |
| `base-color-repair` | Q4 color/lightness alignment in unauthorized or unchanged regions | Intentional recolors, requested relight/grade, new objects, identity, geometry, optics, and composition |
| `multi-round-repair` | Q5 consolidation using the current edit plus the root base | Every intended change already present in the current edit; root identity, geometry, framing, and color truth |

Quality repair is not permission to beautify, globally denoise, resharpen, upscale, recolor, or reinterpret the scene.

## Input Roles

### One image

Use the current image as the edit target. Q1–Q3 can repair visible artifacts. Without a root base, Q4 may normalize an obvious cast using skin and neutral objects, but it cannot claim exact source-color restoration.

### Current edit plus root base

When the original first image exists, give the editor exactly two role-labeled references:

1. **Image 1 — current edit target:** retain every authorized content, light, atmosphere, and styling change already accepted.
2. **Image 2 — root base reference:** use only for identity, geometry, framing, original color relationships, clean unchanged regions, and source texture hierarchy.

In Codex, pass them in that order through `referenced_image_paths: [CURRENT_EDIT, ROOT_BASE]` and state the roles in `EDIT:`. Never use the previous raw round as the color reference, and do not attach the full intermediate chain.

If the requested edit is a global relight, warm/cool grade, monochrome conversion, or deliberate recolor, exempt those authorized axes from base-color locking. The root base remains the identity/geometry reference, not a command to undo the requested look.

## Semantic Zones

Describe three conceptual zones when the edit is local:

- **target zone:** the object or portrait area allowed to change;
- **interaction zone:** legitimate contact shadow, reflection, occlusion, haze, atmosphere, and light spill;
- **protected zone:** every other structure and appearance axis.

Keep the target and its interaction inside the named area. Match boundary exposure, white balance, saturation, sharpness, depth, noise character, shadow softness, and reflection strength to nearby pixels. These are prompt-level constraints, not a hard pixel lock; never claim pixel-identical preservation from a full-frame generative editor.

## Quality Recipes Q

| Code | Model-facing behavior |
| --- | --- |
| Q0 Source quality | Preserve the current image's noise, gradient, color, sharpness, compression, and edit-boundary behavior. |
| Q1 Clean synthetic texture noise | Remove only repeating low-contrast cellular, maze-like, worm-like, checker/grid, or dirty chroma artifacts. Restore clean material continuity while preserving real directional fibers, pores, hair, fabric weave, edges, and any explicitly requested film grain. Do not smooth the whole frame. |
| Q2 Tonal and chroma continuity | Replace posterized steps, contour bands, broken gradients, and blotchy low-frequency color transitions with continuous camera-like roll-off in skin shadows, walls, skies, haze, and bokeh. Preserve true object edges, cast-shadow boundaries, black point, and local contrast. |
| Q3 Local edit seam repair | Repair only the visible edit boundary. Match adjacent exposure, white balance, saturation, microcontrast, sharpness, noise character, depth of field, haze, reflection, and shadow softness while preserving the intended object and interaction effects. Remove halos, rectangular seams, cutout edges, and abrupt texture-density changes. |
| Q4 Root-base color lock | In unchanged or unauthorized regions, return skin hue, neutral objects, whites, darks, saturation relationships, and lightness curves to the root base. Preserve intentional new colors and every authorized E/T/G/A change; remove only the unintended global or regional cast. |
| Q5 Multi-round consolidation | Use the root base for identity, geometry, color truth, and clean texture hierarchy; use the current edit for all accepted changes. Rebuild one coherent current frame without accumulated color drift, synthetic noise, repeated texture, sharpening halos, compression residue, banding, or seam buildup. Preserve each intended change once. |
| Q6 Combined clean repair | Repair at most three observed failures from Q1–Q4 in one pass. State them explicitly, preserve every unlisted axis, and avoid generic enhancement, global smoothing, or a new grade. Use only when defects coexist in the same current image. |

Noise is not skin detail. Grain is not dirt removal. Q1 must distinguish synthetic isotropic repetition from natural directional material structure. Q2 must distinguish banding from a real shadow edge. Q3 must not blur a seam; it must restore local rendering continuity.

## Multi-Round Editing

1. Keep the root base permanently. It is the only non-accumulated color and structure reference.
2. Make one intended semantic change per round whenever possible.
3. After each round, run Q4 or Q5 against the root base before starting the next round.
4. Feed the repaired current result into the next edit, while retaining the same root base as the second reference.
5. Do not feed every intermediate image to the model; it increases ambiguity and can preserve accumulated defects.
6. If several raw rounds already exist, repair only the latest accepted current state against the root base. Earlier rounds are audit history, not generation references.
7. For an intentional global color/light change, lock identity, geometry, neutrals where still applicable, and unauthorized regions; do not force the new look back to the base.

## Quality Line

Add `QUALITY:` only when Q differs from Q0:

```text
QUALITY: {one Q behavior}; preserve {natural texture and authorized changes}; use the root base only for {declared locked axes}.
```

Keep `QUALITY:` concrete and observable. Do not send recipe codes, metrics, model names, algorithm names, or claims of pixel identity. On retry, replace the failed QUALITY line instead of appending more cleanup terms.

## Quality Validation

Inspect the full frame at normal size first, then smooth gradients, skin, hair, fabric, walls, sky, bokeh, and edit boundaries at `200%–400%`:

- **Cleanliness:** no dirty veil, repeating cellular/worm/grid pattern, chroma speckle, or new global smoothing.
- **Natural detail:** directional fibers, pores, hair, fabric weave, fine edges, and source focus hierarchy remain nonrepeating and scale-appropriate.
- **Gradient continuity:** no posterization, contour steps, hue bands, or blotchy transitions; real edges and cast-shadow boundaries remain defined.
- **Boundary continuity:** no rectangular seam, halo, cutout edge, doubled contour, abrupt blur/sharpening change, or light/color discontinuity.
- **Color lock:** compare only unchanged or unauthorized regions with the root base. Skin, neutrals, whites, darks, saturation, and lightness should agree without undoing intentional new colors or the selected E/T/G/A treatment.
- **Iteration quality:** the current result should not be noisier, sharper, dirtier, more compressed, more tinted, or more banded than the root base merely because it is a later round.

If the requested repair is not clearly visible at normal viewing size, or natural detail is lost to smoothing, mark the result failed and return a recompiled compact prompt.

## Failure Repair

| Failure | Replace only this behavior |
| --- | --- |
| Dirty pattern remains | Q1: name its location/material and replace it with clean directional material texture; keep surrounding detail unchanged. |
| Surface becomes waxy or flat | Reduce Q1 strength conceptually; restore directional fibers, bounded reflection, focus falloff, and regional microdetail. |
| Banding remains | Q2: name the affected gradient and require continuous luminance/chroma roll-off while preserving real edges and black point. |
| Seam remains visible | Q3: match boundary exposure, white balance, sharpness, noise, depth, shadow, reflection, and haze; do not blur the boundary globally. |
| Color repair undoes the requested look | Restrict Q4 to unchanged/unauthorized regions and explicitly exempt the authorized E/T/G/A axes. |
| Color still drifts after several rounds | Use the root base, not the previous round, and switch to Q5 with only current edit plus root base attached. |
| Later round looks noisier or oversharpened | Q5: consolidate once from current edit intent and root-base texture hierarchy; remove accumulated enhancement without deleting accepted changes. |
