# V2.1 Tone, Exposure, Look, and Capture Recipes

## Contents

[Protocol](#selection-protocol) · [Scopes](#scope-boundaries) · [Exposure](#exposure-recipes-e) · [Looks](#color-and-style-recipes-g) · [Capture](#capture-response-recipes-d) · [Device aliases](#device-alias-routing) · [Optics](#optics-boundary) · [Failure repair](#failure-repair)

## Selection Protocol

Treat physical illumination, exposure, color rendering, and capture character as separate controls:

- `L/T/A` describe the light that exists in the scene.
- `E` describes where highlights, midtones, shadows, and black point land in the exposure.
- `G` describes the post-capture palette and tone curve.
- `D` describes capture response: tonal steps, highlight behavior, microcontrast, sharpening, and noise character.

Default to `E0 + G0 + D0`. Add a nonzero G or D only when the user asks for a grade, era, style, device, or film/camera character. Translate codes into visible behavior; never send codes to the image model.

Use one E, one G, and one D. Do not combine competing camera systems, eras, color grades, or exposure intents. A named device is not a substitute for exposure, lighting, or color instructions.

## Scope Boundaries

| Scope | Authorized change | Locked by default |
| --- | --- | --- |
| `texture-only` | Skin reflectance and scale-resolved microdetail | `L0 + E0 + T0 + G0 + D0 + A0`; all source light, color, exposure, optics, and scene content |
| `tone-and-exposure` | E, T, and G only | Light direction/source size, identity, geometry, camera view, focal plane, depth of field, objects, and background structure |
| `relight-and-skin` | L, E, T, S, P, optional G/D/A | Identity, geometry, camera position, focal plane, depth of field, framing, and scene structure |
| `capture-style` | G and D; E only when the requested capture logically requires it | Physical light direction, identity, geometry, viewpoint, crop, focal plane, and depth of field |
| `optical-restyle` | Explicitly requested viewpoint, perspective, focal-length feel, or depth-of-field change | Identity and facial feature geometry remain locked; expect more generative reconstruction |

When requests combine scopes, authorize only the named axes. “Make it look shot on a medium-format camera” means capture response, not a new pose, camera position, lens perspective, crop, or background.

## Exposure Recipes E

Each E recipe must state the exposure reference, highlight treatment, midtone placement, and shadow/black behavior.

| Code | Model-facing behavior |
| --- | --- |
| E0 Source exposure | Preserve source highlight headroom, midtone placement, shadow depth, and black point. |
| E1 Balanced natural | Place face and clothing midtones clearly without flattening direction; retain smooth highlight headroom and clean separated shadows with a stable black point. |
| E2 Highlight priority | Expose for a bright window, sunset rim, practical, or reflective highlight; protect its shape and allow unlit subject planes to fall naturally according to available bounce. |
| E3 Shadow priority | Recover only blocked information needed for the subject or room; keep luminous sources controlled and preserve directional separation instead of lifting the full frame. |
| E4 High key | Hold bright skin and background midtones while retaining texture in whites, gentle facial modeling, a soft black point, and no clipped featureless skin. |
| E5 Low key | Place only the selected lit planes in readable midtones; let unlit areas recede toward a clean black point while preserving highlight separation and source direction. |
| E6 Silhouette | Expose for the rear source/background and render the complete subject interior black with no fill or internal highlight. Use only with A6. |
| E7 Direct-flash ambient falloff | Expose the subject cleanly from one on-axis flash and let ambient/background brightness fall rapidly with distance; retain compact highlights and a firm, noncrushed black point. |

Do not use “brighter,” “darker,” “HDR,” or “cinematic exposure” alone. Describe the four tonal zones above. Never recover every highlight and shadow simultaneously; that produces flat tone mapping.

## Color and Style Recipes G

G changes palette and tonal rendering after the physical T relationship is established. Preserve recognizable skin hue unless the user explicitly requests a complexion change.

| Code | Model-facing behavior |
| --- | --- |
| G0 Source look | Preserve source contrast curve, saturation, hue relationships, and neutral reference objects. |
| G1 Neutral editorial | Use a restrained S-curve, clean neutral midtones, controlled saturation, and smooth highlight compression while keeping skin hue stable. |
| G2 Clean commercial | Use bright accurate midtones, neutral whites, low-to-medium contrast, restrained saturation, and clear material/skin separation. |
| G3 Muted documentary | Reduce environmental saturation slightly, preserve skin chroma and practical-light color, and use a gentle toe with natural highlight roll-off. |
| G4 Warm/cool cinematic | Keep illuminated skin mildly warm, move only shadow ambience and background toward cool teal-blue, protect neutral objects, and avoid a global two-color wash. |
| G5 Pastel editorial | Use luminous lifted midtones, softly compressed highlights, low-to-medium chroma, and a stable neutral black point rather than a gray veil. |
| G6 Tonal monochrome | Convert color by luminance, with separated skin, hair, clothing, and background midtones; retain controlled highlights and deep detailed blacks. |
| G7 Restrained 1970s print | Use warm highlights, slightly muted greens/blues, gentle contrast, and soft highlight density; add fine scene-level grain only if explicitly requested. |
| G8 Clean 1990s/Y2K flash | Use neutral-to-cool compact highlights, crisp subject midtones, modest color punch, and darker ambient falloff without added grain by default. |

Do not send bare style labels such as `cinematic`, `editorial`, `vintage`, `film look`, or `premium`. Compile the selected G into observable palette and curve behavior.

## Capture Response Recipes D

D emulates a capture class; it does not claim exact manufacturer color science or physically change the camera used for the source.

| Code | Model-facing behavior |
| --- | --- |
| D0 Source capture | Preserve source tonal response, sharpening, noise character, focal rendering, and dynamic range. |
| D1 Modern full-frame digital | Use clean high-signal detail, moderate optical microcontrast, neutral color separation, restrained edge sharpening, and smooth highlight roll-off. |
| D2 Medium-format digital | Use exceptionally smooth tonal steps, rich but controlled color separation, low sharpening artifacts, gradual highlight compression, and a coherent focal-plane transition. |
| D3 35mm color-negative scan | Use gentle highlight compression, slightly softened microcontrast, restrained film color separation, and no grain unless the user explicitly requests a fine scene-level grain. |
| D4 Compact CCD/digicam | Use direct, slightly crisp tonal response, modest highlight headroom, clear local color, and small-camera immediacy without a texture or color-cast overlay. |
| D5 Point-and-shoot direct flash | Use one small on-axis flash, compact specular highlights, decisive subject exposure, quick ambient falloff, and casual capture character. Pair with L6 + E7. |
| D6 Smartphone computational | Use broad usable dynamic range, restrained local tone mapping, neutral skin, controlled edge sharpening, and no HDR halos; preserve source depth of field unless optical restyle is explicit. |
| D7 Instant film | Use compressed dynamic range, softly rolled highlights, gently softened microcontrast, restrained warm color, and a stable lifted toe; grain/border effects require explicit request. |
| D8 Disposable-camera snapshot | Use uneven but plausible flash-to-ambient exposure, limited highlight headroom, casual color response, and optional low-amplitude scene grain/vignette only when explicitly requested. |

Keep skin microtexture governed by S/P. Sensor noise or film grain is a frame-level capture property and must never be used to create pores, freckles, wrinkles, or facial contrast.

## Device Alias Routing

| User wording | Route | Compilation rule |
| --- | --- | --- |
| DSLR, mirrorless, Canon/Sony/Nikon-like | D1 | Use full-frame behavior. Retain the brand only if the user explicitly requests it; do not invent brand-specific colors. |
| Hasselblad, Phase One, Fujifilm GFX, medium format | D2 | Compile to smooth tonal gradation, color separation, highlight roll-off, and restrained sharpening. |
| Leica, 35mm film, color negative, film camera | D3 | Ask no follow-up when generic; use restrained negative-scan behavior. A named film stock is retained only when supplied by the user. |
| CCD, digicam, early digital compact | D4 | Use compact CCD response without automatic grain, dirt, date stamp, or color cast. |
| compact point-and-shoot, paparazzi, Y2K flash | D5 + E7 + G8 | Use direct-flash physics and ambient falloff; preserve identity and framing. |
| iPhone, Pixel, smartphone | D6 | Use restrained computational response; do not add HDR halos, portrait-mode cutout blur, or excessive sharpening. |
| Polaroid, Instax, instant camera | D7 | Use instant-film tone only; border, print damage, or grain must be explicitly requested. |
| disposable camera | D8 | Allow exposure irregularity only by explicit request; keep skin tone coherent and identity stable. |

## Optics Boundary

Device response and optics are separate. Preserve source camera position, perspective, crop, focal plane, and depth-of-field strength for every scope except explicit `optical-restyle`.

If the user explicitly requests a focal length, aperture, macro view, smartphone-wide perspective, or medium-format depth transition:

1. mark `optical-restyle` explicitly;
2. state the visible optical consequence rather than numbers alone;
3. use only one focal-length/aperture behavior;
4. allow the minimum crop/background reconstruction required;
5. keep facial proportions and feature geometry stable.

Useful translations:

| Request | Observable clause |
| --- | --- |
| 85–105 mm portrait lens | `compressed portrait perspective with undistorted facial proportions and gradual background separation` |
| 50 mm normal lens | `natural perspective with moderate subject-background separation` |
| 24–28 mm smartphone-wide | `wider environmental perspective with deeper focus; keep the face away from edge stretching` |
| wide aperture | `eyes on the retained focal plane with gradual optical falloff behind the face` |
| stopped down | `deeper coherent focus without sharpening every surface equally` |

Never combine a new focal length with “preserve exact perspective.” If optical change was not requested, omit focal length and aperture from the generation prompt.

## Failure Repair

| Failure | Replace only this layer |
| --- | --- |
| Unchanged tone | Replace E with explicit highlight, midtone, shadow, and black-point placement. |
| Flat HDR appearance | Remove global highlight/shadow recovery; return to E1 and preserve directional separation. |
| Color wash over skin | Replace G with skin-neutral regional color placement and protect neutral reference objects. |
| Style is only a tint | Add one curve behavior and one saturation relationship; do not add more style labels. |
| Device look is invisible | Replace the device name with its D response: tonal steps, highlight behavior, microcontrast, sharpening, and dynamic range. |
| Device look changes viewpoint | Restore source perspective/crop/focal plane/DOF and keep only D response. |
| Film look dirties skin | Remove grain/cast/imperfection language; keep G7/D3 tonal response and let S/P define skin. |
| Smartphone look becomes crunchy | Remove HDR and clarity language; use broad DR with restrained local tone mapping and edge sharpening. |
