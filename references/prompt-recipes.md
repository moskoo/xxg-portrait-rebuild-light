# Compact Prompt Compiler

## Contents

[Output contract](#output-contract) · [Observable outcomes](#observable-outcomes) · [Production prompts](#six-production-prompts) · [Skin clauses](#scale-aware-skin-clauses) · [Failure rewrites](#replace-one-failed-line) · [Forbidden language](#forbidden-prompt-language)

## Output Contract

Send only the information needed to perform the edit: one structural lock, one key/exposure system, one scale-aware skin target, one color-temperature relationship, and at most one atmosphere. Target `40–90` English words; allow up to `120` for dense text or product scenes.

```text
EDIT: Relight this portrait; retain the same person's identity, facial proportions, feature size and placement, natural asymmetry, expression, pose, camera view, and composition.
LIGHT: {L + exposure/shadow behavior + background response} {A} {T}.
SKIN: {S}.
AVOID: identity drift, beauty smoothing, dirty or grainy skin, and structural background redraw.
```

Compile by these rules:

1. Select one L, one S, one T, and zero or one A from [the recipe library](lighting-skin-color-temperature-recipes.md); copy behavior, never recipe codes.
2. Express direction, apparent source size, falloff, landing area, shadow depth, and background response as one observable lighting result.
3. Lock identity once. Name no more than three protected object categories. Omit audits, confidence, backend details, and reasoning.
4. Remove synonymous adjectives and conflicting instructions. Keep only the four failure modes most likely for the source.
5. On retry, replace the failed line; never append a corrective paragraph.

### A6 Override

For A6, force silhouette exposure. Remove all frontal/side illumination, fill, catchlights, and internal highlights from L. Use L and T only to design the backlight and background. State `the entire subject interior forms one continuous black silhouette; retain only the original outline, proportions, and pose`. Replace the SKIN line with `No facial, skin, hair, clothing, accessory, or body detail is visible inside the silhouette.`

## Observable Outcomes

| Scene | Specify this result instead of style adjectives |
| --- | --- |
| Backlight | Retain the bright source and hair rim; let the camera-facing side fall naturally into deep shadow, partial silhouette, or low-level reflected fill according to exposure intent. |
| Window light | A broad directional luminance gradient crosses both the subject and nearby wall or furniture. |
| Editorial | A short soft nose shadow, one source-consistent catchlight, and deep but smooth far-cheek modeling. |
| Low-key beam | A narrow beam follows facial curvature across the eye, nose, and cheek; areas outside it remain deep and clean. |
| Golden hour | Warm side-backlight defines hair and shoulders; the camera-facing side remains naturally darker. |
| Neon | One colored key and one secondary rim have distinct directions and intensities. |
| A6 | Against a luminous background, the complete subject interior is black; only the original outline and pose remain readable. |

## Six Production Prompts

### Classic Editorial

```text
EDIT: Relight this portrait; retain the same person's identity, facial proportions, feature size and placement, natural asymmetry, expression, pose, camera view, and composition.
LIGHT: Use a large soft key above camera-left for restrained Rembrandt modeling, minimal fill in the eye socket, a deep soft far-cheek shadow, one source-consistent catchlight, and a low-contrast neutral-daylight background.
SKIN: Keep fair, healthy skin with clean low-contrast microtexture and the original lip and eye-area detail.
AVOID: identity drift, beauty smoothing, added grain, or background redesign.
```

### Cinematic Low-Key Warm/Cool

```text
EDIT: Relight this portrait; retain the same person's identity, facial proportions, feature size and placement, natural asymmetry, expression, pose, camera view, and composition.
LIGHT: Use a warm side key with low-key exposure and no frontal fill; let the far side approach black. Confine cool ambience to the background and rim, with only faint source-aligned atmospheric light.
SKIN: Keep illuminated skin clean and continuous with low-contrast microtexture; do not deepen eye bags or smile lines.
AVOID: identity drift, muddy gray skin, duplicate shadows, or a global orange-teal grade.
```

### Golden-Hour Backlight

```text
EDIT: Relight this portrait; retain the same person's identity, facial proportions, feature size and placement, natural asymmetry, pose, camera view, and composition.
LIGHT: Place warm sunset light behind and to one side, outlining hair and shoulders. Expose for the bright rim with no frontal fill; let the camera-facing side fall into natural deep shadow, and align one restrained flare and the background's warm response with the source.
SKIN: Show clean low-contrast microtexture only where light genuinely reaches the skin.
AVOID: identity drift, flat fill, global orange tint, or cutout halos.
```

### Cyan/Magenta Neon

```text
EDIT: Relight this portrait; retain the same person's identity, facial proportions, feature size and placement, natural asymmetry, expression, pose, wardrobe, and composition.
LIGHT: Use a magenta side key and a weaker cyan rim from the opposite rear direction. Keep exposure low-key with no white fill; unlit planes remain deep, while bokeh stays only in the optically defocused background.
SKIN: Preserve natural reflective response and low-contrast microtexture under the colored light.
AVOID: identity drift, full-face color wash, duplicate nose shadows, or light covering the eyes.
```

### Soft Window Light

```text
EDIT: Relight this portrait; retain the same person's identity, facial proportions, feature size and placement, natural asymmetry, pose, scene objects, and composition.
LIGHT: Use a soft window key above camera-left to create a broad left-to-right falloff. Add only weak room bounce on the shadow side; carry the same direction and decay across skin, clothing, and the nearby wall, with one continuous soft window shadow if requested.
SKIN: Keep clean healthy tone, low-contrast microtexture, and the original lip and eye-area detail.
AVOID: identity drift, pasted-on patches, muddy shadows, or scene redesign.
```

### A6 Full-Black Silhouette

```text
EDIT: Relight this portrait; retain the subject's original outline, proportions, pose, camera view, and composition.
LIGHT: Expose for the bright source behind the subject. Remove fill, catchlights, and all internal illumination; render the entire subject as one continuous black silhouette while the background responds naturally to the backlight.
SKIN: No facial, skin, hair, clothing, accessory, or body detail is visible inside the silhouette.
AVOID: outline drift, gray fill, cutout halos, or residual facial light.
```

## Scale-Aware Skin Clauses

| Recipe | Model-facing clause |
| --- | --- |
| S0 `<256 px` | Render clean continuous skin tone and source-consistent reflection; do not invent pores, blackheads, vellus hair, moles, or fine lines. |
| S1 `256–511 px` | Keep fair, healthy skin with low-contrast irregular microtexture; retain source lip texture, eye-area transitions, and restrained forehead sheen. |
| S2 `≥512 px` | Render clean camera-resolved microtexture: softer cheek pores, slightly crisper nose pores, plus original fine lines, vellus hair, and identifying marks. |

## Replace One Failed Line

| Failure | Replacement strategy |
| --- | --- |
| Nearly unchanged | Rewrite LIGHT with one explicit direction, landing area, exposure consequence, and visible result; remove `subtle`, `minimal`, and `change as little as possible`. |
| Identity drift | Reduce EDIT to `retain the same subject, original facial geometry, expression, and composition`; never describe a more attractive feature shape. |
| Dirty skin | Replace SKIN with `clean continuous skin tone and low-contrast reflective microtexture`. |
| Competing lights | Keep one key, only the necessary fill, and one background response. |
| Artificial patch or flare | State the source, physical landing area, edge behavior, and continuous response across subject and nearby surface. |
| Unintended shadow loss | Add fill only for `balanced` or `source-matched`; never lift low-key, highlight-priority, or silhouette shadows by default. |
| A6 retains interior detail | Remove ordinary S and subject lighting; require `continuous black interior with no fill, catchlight, skin color, hair detail, or garment texture`. |

## Forbidden Prompt Language

- `change nothing`, `minimal pixel change`, or exhaustive per-object locking;
- perfect symmetry, idealized features, golden facial proportions, or flawless porcelain skin;
- ultra-sharp pores, abundant blackheads, coarse raw skin, strong grain, HDR, or local-clarity sculpting;
- stacking soft window light, hard light, Rembrandt light, neon, sunset, and volumetric rays in one edit;
- demanding a fully readable face, no clipped highlights, and complete shadow detail under every lighting intent;
- combining A6 with visible skin texture, catchlights, facial fill, hair strands, or garment detail;
- vague terms such as `premium`, `cinematic`, or `atmospheric` without source direction and landing behavior.
