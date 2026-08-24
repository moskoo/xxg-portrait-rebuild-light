# Lighting, Skin, Color, and Atmosphere Recipes

## Contents

[Selection](#selection-protocol) · [Exposure](#exposure-intent) · [Combinations](#quick-combinations) · [Key lights](#key-light-recipes-l) · [Atmosphere](#atmosphere-recipes-a) · [Skin](#skin-recipes-s) · [Color](#color-temperature-recipes-t) · [Controls](#optional-control-clauses)

## Selection Protocol

Choose exactly `one L + one S + one T + zero or one A`. Decide internally as `Key → Exposure → Fill → Shadow → Subject → Background → Atmosphere`, then send only the model-facing behavior without codes or explanations.

- Define key direction, apparent source size, and landing area. Set exposure before fill.
- Derive shadow edge and depth from source size and distance. Apply the same light direction, falloff, and reflected color to subject and environment.
- Use at most one atmosphere. A1–A5 must inherit the selected key.
- A6 overrides ordinary exposure and suspends visible subject lighting and skin texture.

## Exposure Intent

| Intent | Use and behavior |
| --- | --- |
| `source-matched` | Preserve source exposure; repair only discontinuities and illumination with no plausible source. |
| `balanced` | Commercial or window-light work; retain separation in highlights and shadows without making them equally bright. |
| `highlight-priority` | Sunset or strong backlight; retain the bright source and rim while allowing the camera-facing side to become deeply shadowed. |
| `shadow-priority` | Subject readability in a dark room; retain shadow information and allow practical lights to bloom. |
| `low-key` | Dramatic or neon work; keep most of the frame near black and expose only selected planes. |
| `silhouette` | Strong backlight; use no fill, remove internal subject detail, and preserve only outline and pose. |
| `high-key` | E-commerce or minimal work; use bright, soft separation without flat gray shadows. |

`Clean shadow` means free of mottled gray, noise, and source-less darkening; it does not mean shallow shadow.

## Quick Combinations

| Requested result | Combination |
| --- | --- |
| Preserve environment; repair flat light | `L0 + Sx + T0 + A0` |
| Natural backlight | `L1 + Sx + T1 + A0` |
| Soft window light | `L2 + Sx + T1 + A0/A1` |
| Commercial studio softness | `L3 + Sx + T1 + A0` |
| Low-key diagonal beam | `L7 + Sx + T0/T2 + A0/A5` |
| Fashion editorial | `L8 + Sx + T1 + A0` |
| Cinematic warm/cool low-key | `L9 + Sx + T3 + A0/A5` |
| Golden hour | `L10 + Sx + T2 + A4` |
| Full-black subject silhouette | `Lx + Sx + Tx + A6` |
| Cyberpunk neon | `L11 + Sx + T4 + A3` |
| Clean commercial high-key | `L12 + Sx + T1 + A0` |

## Key-Light Recipes L

| Code | Model-facing behavior |
| --- | --- |
| L0 Source match | Preserve the source key and exposure; correct only flatness, discontinuous falloff, and light or shadow with no plausible source. Retain intentional darkness and practical highlights. |
| L1 Natural backlight | Keep the rear source, bright background, and hair rim. Expose for highlights; allow the camera-facing side to deepen naturally, adding only low-level environmental reflection when facial fill is explicitly requested. |
| L2 Soft window key | Place a large soft window source above and to one side for a broad directional gradient. Use weak fill only if needed; carry the same direction and falloff across subject, clothing, wall, and furniture. |
| L3 Commercial soft key | Place a large soft source above and camera-side with low-level frontal fill. Produce a short soft nose shadow, readable eye socket, natural cheek/jaw modeling, and restrained background response. |
| L4 Open-sky light | Use broad skylight plus location bounce to illuminate the subject with low-amplitude curvature and ambient color. Avoid studio hotspots and artificial hair rims. |
| L5 Practical mixed light | Let each visible warm practical affect only plausible nearby surfaces and decay with distance. Retain neutral ambient fill only when the room supports it; make subject and room responses agree. |
| L6 Hard point source | Place one small directional source for crisp curvature-aware shadows. Permit controlled highlight clipping and near-black unlit planes; align nose, neck, clothing, and background cast shadows. |
| L7 Diagonal light beam | Use low-key exposure and one slightly softened narrow beam crossing the eye, nose, and cheek along facial curvature. Keep areas outside the beam near black with a clean outline and a source-aligned background response. |
| L8 Rembrandt editorial | Place a large soft key above and to one side, with minimal fill preserving the eye socket. Keep the far cheek deep but smooth and create exactly one source-consistent catchlight. |
| L9 Cinematic low-key | Use one warm side key for selective facial modeling, low-key exposure, and no frontal fill. Let the far side approach black; confine cool light to background and rim. |
| L10 Golden-hour side backlight | Place warm sunset light behind and to one side, outlining hair and shoulders. Expose for the bright rim with no frontal fill; allow deep camera-facing shadows and align background warmth and long shadows with the source. |
| L11 Dual-tone neon | Use one magenta side key and a weaker cyan rim from a distinct opposite-rear direction. Keep low-key exposure with no white fill; preserve deep unlit planes and avoid a uniform color wash. |
| L12 Minimal high-key soft light | Use a large top-front diffused source with slight frontal fill for clean diffuse highlights, soft directional shadows, and bright but nonflat separation. |

## Atmosphere Recipes A

| Code | Model-facing behavior |
| --- | --- |
| A0 None | Add no new atmosphere effect. |
| A1 Window shadow | Add one low-contrast soft window shadow across the subject and an adjacent wall; perspective, direction, penumbra, and falloff must follow the key rather than appear pasted on. |
| A2 Tree shadow | Add sparse, irregular foliage shadows that break naturally across facial and clothing curvature and continue onto nearby background surfaces with the same direction. |
| A3 Bokeh | Add only a few light circles in optically defocused background regions. Derive their color from visible scene lighting and never place them over the subject. |
| A4 Sunset flare | Add one restrained flare aligned with the sunset source. Permit slight contrast loss or bloom only near that source, never across the entire frame. |
| A5 Volumetric light | Add extremely faint source-aligned haze and sparse dust only where a visible or strongly inferred beam crosses air or background; do not veil the subject. |
| A6 Full-black silhouette | Place the subject against a bright source or luminous background with no fill, catchlight, or internal illumination. Render face, skin, hair, clothing, accessories, and body interior as one continuous black mass while retaining the original outline, proportions, and pose. |

### A6 Override

- Force `exposure_intent: silhouette`, `fill_policy: none`, and `shadow_policy: silhouette`.
- Retain from L only the rear source and background treatment; remove frontal and side illumination from the subject.
- Omit S from the model prompt. Apply T only to the source and background.
- Fail if facial features, skin color, catchlights, lit hair strands, garment texture, accessory shading, or gray fill remains inside. Permit only a very narrow source-consistent rim that does not enter the silhouette.

## Skin Recipes S

| Code | Scale and model-facing behavior |
| --- | --- |
| S0 `<256 px` | Render clean continuous skin tone and source-consistent reflection; do not invent pores, blackheads, vellus hair, moles, or fine lines. |
| S1 `256–511 px` | Keep fair, healthy skin with low-contrast irregular microtexture. Retain source lip texture, eye-area transitions, and restrained forehead sheen; invent no blemishes. |
| S2 `≥512 px` | Render clean camera-resolved microtexture: softer cheek pores, slightly crisper nose pores, original shallow lines, vellus hair, and identifying marks. Keep face, neck, and upper-chest chroma continuous. |

Apply S only to genuinely illuminated skin. Do not lift deep shadows to reveal texture. Preserve blackheads, powder separation, flaking, dryness, freckles, and conspicuous moles only when they exist in the source. A6 suppresses all visible S behavior.

## Color-Temperature Recipes T

| Code | Model-facing behavior |
| --- | --- |
| T0 Source white balance | Preserve the source white balance and skin neutral point; correct only localized discontinuous color casts. |
| T1 Neutral daylight | Use neutral natural daylight; keep healthy skin and nominally white objects from drifting blue or yellow. |
| T2 Golden warm light | Concentrate warmth on directly lit planes and nearby bounce. Retain healthy neutral transitions in skin; do not apply a global orange filter. |
| T3 Warm key, cool background | Put warm color in the subject key and cool color only in background or rim. Keep transitions continuous and avoid a face-to-neck color break. |
| T4 Cyan/magenta relationship | Give cyan and magenta distinct directions, roles, and intensities. Preserve plausible skin reflection on lit planes, deep shadows elsewhere, and controlled saturation. |

## Optional Control Clauses

| Need | Add only this clause |
| --- | --- |
| One catchlight | `one source-consistent catchlight` |
| Recover shadow detail | `subtle environmental fill retaining shadow separation` — only for `balanced` or `source-matched` |
| Soft light | `large diffused key with a broad shadow transition` |
| Hard light | `small hard key with a clean cast-shadow edge` |
| Contact depth | `very subtle ambient occlusion at contact points` — never use as fill |
| Film grain | `very fine uniform film grain across the full frame` — only when explicitly requested |
| Clean shadow | `clean shadow without muddy gray patches` |
| Highlight priority | `expose for highlights; allow naturally deep backlit shadows` |
| Shadow priority | `expose for subject shadows; allow practical highlights to bloom` |
| Low-key | `low-key exposure with deep clean shadows and sparse highlights` |
| Silhouette | `no frontal fill; preserve the outer silhouette while the interior falls to black` |
