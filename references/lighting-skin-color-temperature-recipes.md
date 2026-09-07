# V2.1 Lighting, Skin, Finish, Color, and Atmosphere Recipes

## Contents

[Protocol](#selection-protocol) · [Scope](#operation-scope) · [Exposure](#exposure-handoff) · [Combinations](#quick-combinations) · [Key lights](#key-light-recipes-l) · [Skin scale](#skin-scale-recipes-s) · [Skin finish](#skin-finish-recipes-p) · [Atmosphere](#atmosphere-recipes-a) · [Color](#color-temperature-recipes-t)

## Selection Protocol

Choose exactly `one L + one E + one S + one P + one T + one G + one D + zero or one A`. Decide internally as `Scope → Key L → Exposure E → Fill/Shadow → Skin S/P → Light color T → Look G → Capture D → Atmosphere A`, then send only model-facing behavior without codes.

- Set operation scope first. A texture-only request must not change lighting or optics.
- Define one key by direction, apparent size, landing area, and falloff. Select E from [the tone/exposure/device reference](tone-exposure-style-device-recipes.md) before fill.
- Make skin finish inherit the key; never add an independent gloss or texture layer.
- Preserve source focal plane and depth of field. Detail visibility must follow scale, focus, distance, and illumination.
- Use at most one atmosphere. A1–A5 inherit the key; A6 overrides exposure and suppresses S/P.

## Operation Scope

| Scope | Required behavior |
| --- | --- |
| `texture-only` | Force `L0 + E0 + T0 + G0 + D0 + A0`; preserve source highlight placement, exposure, white balance, shadow transitions, focal plane, depth of field, and environment. Use S + P0/P1 only. |
| `tone-and-exposure` | Keep L0 and source optics; authorize only the requested E/T/G corrections. |
| `relight-and-skin` | Apply selected L/E/T/A consistently to subject and environment; preserve source optics and identity while adapting S/P. |
| `capture-style` | Keep physical light unless requested; apply G/D and only a logically required E while preserving viewpoint, crop, focus, and DOF. |

## Exposure Handoff

Select exactly one E from [Tone, Exposure, Look, and Capture Recipes](tone-exposure-style-device-recipes.md). E—not L—places highlights, midtones, shadows, and black point. L defines only the physical source and its geometry.

Default to E0 for preservation and E1 for natural relighting. E5/E6/E7 require an explicit low-key, silhouette, or direct-flash intent.

## Quick Combinations

| Requested result | Combination |
| --- | --- |
| Skin fidelity only | `L0 + E0 + Sx + P0/P1 + T0 + G0 + D0 + A0` |
| Tone/exposure correction | `L0 + E1/E2/E3 + Sx + P0 + T0/T7 + G0/G1 + D0 + A0` |
| Natural backlight | `L1 + E2 + Sx + P2 + T1 + G0 + D0 + A0` |
| Soft window light | `L2 + E1 + Sx + P2 + T1 + G0/G1 + D0/D2 + A0/A1` |
| Commercial studio softness | `L3 + E1/E4 + Sx + P5 + T1 + G2 + D1/D2 + A0` |
| Point-and-shoot flash | `L6 + E7 + Sx + P4 + T0/T1 + G8 + D5 + A0` |
| Low-key diagonal beam | `L7 + E5 + Sx + P3 + T0/T2 + G0/G4 + D0 + A0/A5` |
| Fashion editorial | `L8 + E1 + Sx + P3 + T1 + G1 + D1/D2 + A0` |
| Cinematic warm/cool low-key | `L9 + E5 + Sx + P3 + T3 + G4 + D1 + A0/A5` |
| Golden hour | `L10 + E2 + Sx + P2 + T2 + G0/G1 + D0/D1 + A4` |
| Full-black silhouette | `Lx + E6 + Sx + Px + Tx + Gx + Dx + A6` |
| Cyberpunk neon | `L11 + E5 + Sx + P6 + T4 + G4 + D1 + A3` |
| Clean commercial high-key | `L12 + E4 + Sx + P5 + T1 + G2 + D1/D2 + A0` |

## Key-Light Recipes L

| Code | Model-facing behavior |
| --- | --- |
| L0 Source lock | Preserve source direction, apparent source size, highlight/shadow landing geometry, falloff, and environmental response. E0 separately preserves tonal placement. |
| L1 Natural backlight | Keep one rear source, source-shaped hair/shoulder rim, and plausible environmental reflection on camera-facing planes. Pair with E2 unless the user requests face fill. |
| L2 Soft window key | Place one large soft window source above and to one side for a broad directional gradient. Carry the same direction, roll-off, and room bounce across skin, clothing, wall, and furniture. |
| L3 Commercial soft key | Place one large soft source above and camera-side with low-level frontal fill. Produce a short soft nose shadow, readable eye socket, gentle cheek/jaw separation, and restrained background response. |
| L4 Open-sky light | Use broad skylight plus location bounce for soft curvature, wide transitions, and source-consistent ambient direction. Avoid artificial studio hotspots or added hair rims. |
| L5 Practical mixed light | Let each visible practical affect only plausible nearby planes and decay with distance. Retain ambient fill only when supported by the room; make subject and environment agree. |
| L6 Direct flash or hard point | Use one small source from the requested direction. Create compact bounded highlights and clean cast-shadow edges; align nose, neck, clothing, and background shadow geometry. Let E set their tonal depth. |
| L7 Diagonal light beam | For an explicit low-key request, place one slightly softened narrow beam across eye, nose, and cheek following facial curvature. Keep the beam edge continuous and let out-of-beam areas recede according to the chosen exposure. |
| L8 Rembrandt editorial | Place one large soft key above and to one side, with minimal fill preserving the eye socket. Create a short nose shadow, gentle far-cheek separation, and exactly one source-consistent catchlight. |
| L9 Cinematic low-key | For an explicit low-key request, use one warm side key for selective facial illumination and no frontal fill. Confine any cool component to background/rim; pair with E5. |
| L10 Golden-hour side backlight | Place one warm sunset source behind and to one side, outlining hair and shoulders. Derive camera-facing illumination from natural reflected fill and align background direction and long shadows; pair with E2. |
| L11 Dual-tone neon | Use one colored side key and one weaker opposite-rear rim with distinct directions. Keep saturation controlled and restrict each color to illuminated planes rather than washing the full face. |
| L12 Minimal high-key soft light | Use one large top-front diffused source with slight frontal fill, broad source-shaped highlights, soft directional shadows, and nonflat separation; pair with E4 for high key. |

## Skin Scale Recipes S

| Code | Scale and model-facing behavior |
| --- | --- |
| S0 `<256 px` | Maintain continuous source skin tone and natural light response; the visible scale does not resolve added surface detail. |
| S1 `256–511 px` | Render faint regional microdetail only on illuminated in-focus skin; preserve clean eye-area and lip boundaries. |
| S2 `≥512 px` | Render fine camera-resolved detail: softer cheek pores, slightly clearer nose pores, natural lip texture, and sparse vellus detail only where source focus resolves it. |

Apply S only where scale, focus, and light support it. Never lift shadows, sharpen the whole face, or tile a uniform pore field to reveal texture. Preserve source identity anchors without naming, adding, or amplifying marks. A6 suppresses S.

## Skin Finish Recipes P

P controls diffuse/specular balance, not complexion or makeup.

| Code | Model-facing behavior |
| --- | --- |
| P0 Source finish | Preserve the exact source diffuse/specular balance and existing highlight location, area, and intensity. Use by default for texture-only work. |
| P1 Natural satin-matte | Use a soft diffuse base with small bounded highlights on key-facing convexities; keep cheeks, jaw, and eye area less reflective without making skin flat. |
| P2 Soft-daylight finish | Use luminous clean midtones, broad roll-off, and restrained window/sky-shaped highlights with continuous face-neck color. |
| P3 Editorial satin | Use controlled T-zone highlights, smooth cheek separation, and low-amplitude optical detail; keep the face dimensional without local line darkening. |
| P4 Direct-flash finish | Keep compact flash-facing highlights with clear boundaries, distinct cheek/jaw tones, and one flash-consistent catchlight; never connect highlights into a facial film. |
| P5 Clean beauty finish | Keep even broad tone, natural three-dimensional reflection, and fine focus-aware detail; retain skin character without porcelain uniformity. |
| P6 Available-light finish | Preserve source-driven highlight placement and optical falloff with restrained detail; do not add marks, grain, stronger color variation, or global sharpening. |

A whole-face gloss layer fails every P. A fully dead-matte result also fails unless the source or user explicitly requires it.

## Atmosphere Recipes A

| Code | Model-facing behavior |
| --- | --- |
| A0 None | Add no atmosphere effect. |
| A1 Window shadow | Add one low-amplitude soft window shadow across subject and an adjacent surface; perspective, direction, penumbra, and falloff must follow the key. |
| A2 Tree shadow | Add sparse foliage shadows that break naturally across facial/clothing curvature and continue onto nearby background surfaces in the same direction. |
| A3 Bokeh | Add only a few light circles in optically defocused background regions. Derive color from scene lighting and never place them over the subject. |
| A4 Sunset flare | Add one restrained flare aligned with the sunset source. Permit slight bloom only near that source, never across the full frame or face. |
| A5 Volumetric light | Add faint source-aligned haze only where a visible or strongly inferred beam crosses air/background; do not veil the subject or add decorative dust. |
| A6 Full-black silhouette | Place the subject against one bright rear source or luminous background with no fill, catchlight, or internal illumination. Render the entire subject interior black while retaining outline, proportions, pose, and placement. |

### A6 Override

- Force `E6`, `exposure_intent: silhouette`, `fill_policy: none`, and `shadow_policy: silhouette`.
- Retain from L only the rear source and background treatment; remove all subject-facing illumination.
- Omit both S and P. Apply T, G, and D only to the source/background; none may restore subject detail.
- Fail if any facial feature, skin color, catchlight, lit hair strand, garment texture, accessory shading, or gray fill remains inside.

## Color-Temperature Recipes T

| Code | Model-facing behavior |
| --- | --- |
| T0 Source white balance | Preserve source white balance and the skin neutral point; correct only a localized discontinuous cast when requested. |
| T1 Neutral daylight | Use neutral natural daylight; keep skin and nominally white objects from drifting blue or yellow. |
| T2 Golden warm light | Concentrate warmth on directly illuminated planes and nearby bounce; retain neutral transitions and avoid a global orange cast. |
| T3 Warm key, cool background | Put warm color in the subject key and cool color only in background/rim; keep face-neck transitions continuous. |
| T4 Cyan/magenta relationship | Give cyan and magenta distinct directions, roles, and intensities; preserve plausible skin reflection and controlled saturation. |
| T5 Cool overcast or blue hour | Use cool-neutral ambient light with preserved skin neutrality, smooth sky-to-subject color continuity, and no full-frame blue wash. |
| T6 Tungsten practical | Keep visible tungsten sources warm and let their color decay with distance; retain believable skin hue and neutral reference separation. |
| T7 Mixed-light balance | Preserve distinct daylight and practical-light regions while neutralizing only conflicting casts on skin and nominally neutral objects. |

## Optional Control Clauses

| Need | Add only this clause |
| --- | --- |
| One catchlight | `one source-consistent catchlight` |
| Balanced fill | `low-level environmental fill retaining directional shadow separation` |
| Soft source | `large diffused key with broad highlight and shadow transitions` |
| Hard source | `small directional key with bounded highlights and a clean cast-shadow edge` |
| Focus realism | `detail follows the source focal plane, depth of field, distance, and illumination` |
| Highlight placement | `small bounded specular highlights only on key-facing convexities` |
| Clean midtones | `luminous clean midtones with directional shadow separation` |
| Highlight priority | `expose for the source and rim; derive subject brightness from available reflected fill` |
| Low-key | `low-key exposure with selected illuminated planes` — explicit dramatic requests only |
| Silhouette | `no subject-facing fill; preserve the outer silhouette while the entire interior falls to black` |
