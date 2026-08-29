# V2 Compact Prompt Compiler

## Contents

[Contract](#output-contract) · [Scope](#scope-first) · [Outcomes](#observable-outcomes) · [Production prompts](#six-production-prompts) · [Skin clauses](#skin-clauses) · [Safe wording](#priming-safe-wording) · [Failure rewrites](#replace-one-failed-line)

## Output Contract

Send one structural lock, one optical/light system, one scale-aware skin behavior, one skin-finish profile, one color relationship, and at most one atmosphere. Target `45–95` English words; allow up to `125` only for dense text or product scenes.

```text
EDIT: {texture-only or relight-and-skin}; retain source identity, geometry, expression, pose, focal plane, depth of field, camera view, and composition.
LIGHT: {L + exposure consequence + shadow transition + background response} {A} {T}.
SKIN: {S + P}; keep tone continuous and specular highlights bounded by the key.
AVOID: identity drift, whole-face gloss, repeated texture, or structural scene redraw.
```

Compile by these rules:

1. Select one L, one S, one P, one T, and zero or one A from [the V2 recipe library](lighting-skin-color-temperature-recipes.md); copy behavior, never codes.
2. State direction, apparent source size, landing area, exposure consequence, shadow transition, and environmental response as one visible result.
3. Lock identity once. Treat the attached source as the identity description; do not restate perceived age, attractiveness, facial style, lens, or aperture.
4. Make the SKIN line describe three separable signals: clean broad tone, bounded source-shaped reflection, and focus-aware regional microdetail.
5. Use at most four source-specific avoid clauses. On retry, replace the failed line rather than appending a corrective paragraph.

### A6 Override

For A6, force silhouette exposure. Remove all subject-facing illumination, fill, catchlights, and internal highlights from L. Use L/T only for the rear source and background. Omit S/P and write: `The entire subject interior is one continuous black silhouette; retain only the original outline, proportions, pose, and placement.`

## Scope First

| User intent | Required compilation |
| --- | --- |
| Skin realism, plastic-skin removal, texture recovery only | `texture-only`; force `L0 + T0 + A0`, preserve highlight placement/exposure/white balance/focus/DOF, and change only skin response. |
| Explicit relight or L/T/A selection | `relight-and-skin`; authorize the selected light while preserving identity, source focal plane, and depth of field. |
| Ambiguous request | Prefer `texture-only` when the complaint is skin; prefer `relight-and-skin` when the complaint is illumination. |

## Observable Outcomes

| Scene | Specify this result instead of a style adjective |
| --- | --- |
| Texture-only | The same source light and optics remain; plastic smoothness is replaced by faint regional detail and bounded original highlights. |
| Soft window | One broad gradient crosses subject and nearby surfaces; skin retains luminous midtones and soft highlight roll-off. |
| Editorial | One large key produces a short soft nose shadow, one catchlight, gentle far-cheek separation, and bounded facial highlights. |
| Direct flash | Compact source-facing highlights remain separated, the cheeks retain tonal shape, and the room falls off with distance. |
| Golden hour | Warm side-backlight defines hair and shoulders; the camera-facing side follows highlight-priority exposure without global orange tint. |
| Neon | One colored key and one weaker opposite rim remain directionally distinct; skin reflects color only on illuminated planes. |
| A6 | Against the bright rear source, the complete subject interior is black and only the original outline/pose is readable. |

## Six Production Prompts

### Texture-Only Fidelity Recovery

```text
EDIT: Enhance skin fidelity only; retain the same identity, facial proportions, feature placement, natural asymmetry, expression, pose, focal plane, depth of field, light, color, camera view, and composition.
LIGHT: Preserve the source exposure, highlight placement, shadow transitions, white balance, and background exactly as photographed.
SKIN: Keep continuous source skin tone and natural satin response; add faint region-specific microdetail only where face scale, focus, and illumination resolve it.
AVOID: facial redesign, whole-face gloss, repeated texture, or global sharpening.
```

### Soft Window Naturalism

```text
EDIT: Relight this portrait; retain source identity, facial proportions, feature size and placement, natural asymmetry, expression, pose, focal plane, depth of field, and composition.
LIGHT: Use one large soft window key above camera-left, creating a broad left-to-right falloff across skin, clothing, and the nearby wall; keep midtones luminous with weak room bounce and natural highlight roll-off.
SKIN: Use clean continuous tone, a satin-matte balance, and faint focus-aware regional microdetail.
AVOID: identity drift, uniform facial shine, texture overlay, or scene redesign.
```

### Balanced Editorial

```text
EDIT: Relight this portrait; retain source identity, facial proportions, feature placement, natural asymmetry, expression, pose, focal plane, depth of field, and composition.
LIGHT: Place one large soft key above camera-left for restrained Rembrandt modeling, a short soft nose shadow, one catchlight, gentle far-cheek separation, and a neutral background response; preserve clear midtones rather than forcing dramatic darkness.
SKIN: Keep source-consistent tone, bounded T-zone highlights, softer cheek reflectance, and scale-aware detail.
AVOID: facial idealization, whole-face gloss, repeated pores, or background redraw.
```

### Direct-Flash Snapshot

```text
EDIT: Relight this portrait as a direct-flash photograph; retain source identity, facial geometry, expression, pose, focal plane, camera view, and composition.
LIGHT: Use one small on-camera flash with rapid room falloff. Keep compact highlights on light-facing convexities, separated rather than joined across the face; retain cheek and jaw tonal shape and one flash-consistent catchlight.
SKIN: Use a natural satin-matte base with subtle focus-resolved detail and clean color continuity.
AVOID: flat facial exposure, a continuous shine layer, texture overlay, or cutout edges.
```

### Golden-Hour Side Backlight

```text
EDIT: Relight this portrait; retain source identity, facial proportions, feature placement, natural asymmetry, pose, focal plane, depth of field, and composition.
LIGHT: Place warm sunset light behind and to one side, outlining hair and shoulders. Expose for the rim; let the camera-facing side follow natural reflected fill, and align background warmth, long shadows, and one restrained flare with the source.
SKIN: Keep illuminated tone continuous with bounded warm reflections and focus-aware regional detail.
AVOID: facial redesign, global orange tint, artificial fill, or cutout halos.
```

### A6 Full-Black Silhouette

```text
EDIT: Relight this portrait; retain the subject's original outline, proportions, pose, placement, camera view, and composition.
LIGHT: Expose for one bright source behind the subject. Remove fill, catchlights, and all internal illumination; render the complete subject as one continuous black silhouette while the background responds naturally to the rear source.
SKIN: No facial, skin, hair, clothing, accessory, or body detail is visible inside the silhouette.
AVOID: outline drift, gray interior fill, cutout halos, or residual facial light.
```

## Skin Clauses

### Scale S

| Recipe | Model-facing clause |
| --- | --- |
| S0 `<256 px` | Maintain continuous source skin tone and natural light response; the visible face scale does not resolve added surface detail. |
| S1 `256–511 px` | Render faint regional microdetail only on illuminated in-focus skin; preserve clean eye-area and lip boundaries. |
| S2 `≥512 px` | Render fine camera-resolved detail: softer cheek pores, slightly clearer nose pores, natural lip texture, and sparse vellus detail only where source focus resolves it. |

### Finish P

| Recipe | Model-facing clause |
| --- | --- |
| P0 Source finish | Preserve the source diffuse/specular balance and the exact location, area, and intensity of existing highlights. |
| P1 Natural satin-matte | Use a soft diffuse base with small bounded highlights on key-facing convexities; keep cheeks and eye area less reflective. |
| P2 Soft-daylight finish | Use luminous clean midtones, broad soft roll-off, and restrained highlights that follow the window or sky source. |
| P3 Editorial satin | Keep controlled T-zone highlights, smooth cheek separation, and visible but low-amplitude optical detail. |
| P4 Direct-flash finish | Keep compact flash-facing highlights with clear boundaries; do not connect them into a continuous facial shine. |
| P5 Clean beauty finish | Keep even broad color, natural three-dimensional reflection, and fine optical detail without porcelain smoothness. |
| P6 Available-light finish | Preserve source-driven highlight irregularity and focus falloff without adding marks, grain, or stronger color variation. |

## Priming-Safe Wording

Do not place these shortcuts in a default model prompt; use the replacement behavior instead:

| Risky shortcut | Safer behavior |
| --- | --- |
| `real skin`, `ultra-real skin` | Specify tone continuity, regional microdetail, and bounded reflection separately. |
| `visible pores`, `8K pores` | `faint region-specific pores only where scale, focus, and light resolve them` |
| `skin color variation` | `continuous source-consistent tone with gentle local transitions` |
| `minor imperfections`, freckles, blemishes, blackheads | `preserve source-identifying skin anchors without adding or amplifying marks` |
| oily/dewy/wet skin | `small bounded specular highlights on key-facing convexities` |
| fully matte skin | `natural satin-matte balance with soft highlight roll-off` |
| raw/coarse/gritty texture | `fine low-amplitude optical microdetail` |
| film grain | Omit by default; never use grain to create skin realism. |
| high contrast, deep shadows | State only the physical exposure consequence of an explicitly selected dramatic light. |
| sharper, ultra-detailed, crisp everywhere | `detail follows the source focal plane, depth of field, distance, and illumination` |

## Replace One Failed Line

| Failure | Replacement strategy |
| --- | --- |
| Nearly unchanged | Rewrite LIGHT or SKIN with one explicit visible result; remove `subtle`, `minimal`, and `change as little as possible` from that line only. |
| Identity drift | Reduce EDIT to `retain source identity, face outline/proportions, feature size/placement, hairline, expression, and composition`; do not describe beauty traits. |
| Plastic smoothness remains | Replace SKIN with `continuous source tone; bounded source-shaped highlights; faint regional detail only where focus and light resolve it`. |
| Skin becomes artificial | Remove all imperfection, color-variation, grain, roughness, and line-emphasis terms; use P0/P1 plus the scale-appropriate S clause. |
| Image becomes dim without intent | Switch exposure to `source-matched` or `balanced`, restore luminous midtones, and remove dramatic-shadow words. |
| Competing lights | Keep one key, only necessary environmental fill, and one background response. |
| Artificial flare/shadow patch | State the source, landing surface, edge transition, and continuous response across subject and environment. |
| A6 retains interior detail | Remove ordinary S/P and all subject lighting; require one continuous black interior. |

## Forbidden Prompt Construction

- generic beauty or realism stacks such as `beautiful, premium, cinematic, ultra-real, 8K, highly detailed`;
- exhaustive identity descriptions that invite the model to reconstruct a new face;
- default imperfection bundles, global grain, uniform pores, or whole-face shine;
- camera/lens/aperture changes during an edit unless explicitly requested;
- multiple key-light styles in one prompt;
- dramatic darkness language when the user did not request a dramatic exposure;
- A6 combined with visible subject texture, catchlights, fill, or garment detail.
