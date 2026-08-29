# V2 Backend Capability and Clean Realism

## Delivery Modes

| Mode | Entry condition and delivery |
| --- | --- |
| `strict-final` | Verified `strict-local` backend, valid edit plan, and every applicable gate passes. |
| `best-effort` | Native full-frame semantic edit without verified mask/pixel passthrough; label non-strict and never claim frozen pixels. |
| `invocation-handoff` | Discovery completed and no compatible callable exists; return a complete compact prompt without claiming invocation failed. |
| `prompt-only` | The correct image tool returned a real error; summarize it and return a complete compact prompt. |
| `prompt-handoff` | A generated image misses the target, changes identity/protected content, or breaks framing; report failure and recompile from source. |

A small face, complex scene, visible text, edge contact, or limited backend can only trigger `best-effort`; none permits refusal. Uniform downscaling is acceptable.

## Native Tool Routing

1. Read the host's native image skill, inspect the source, and search registered tools. In Codex, inspect `ALL_TOOLS` and prefer `image_gen__imagegen` when actually present.
2. For a local source in Codex, call `tools.image_gen__imagegen({referenced_image_paths: [absolute_path], prompt})`.
3. Treat a wrong member, function name, argument, or `TypeError` as a dispatch error. Correct it from the registered signature and retry.
4. Classify a real backend as `strict-local` or `full-frame-generative`. Do not bypass the host with a CLI or separate API by default.

Never guess `tools.image_gen` or `input_image`. Reading a skill, inspecting an image, creating a task, or announcing generation is not a tool invocation.

## Invocation Evidence

| State | Required evidence | Mode |
| --- | --- | --- |
| Image generated | Image-tool call plus image/result ID or accessible output file | `strict-final` or `best-effort` after validation |
| Invocation failed | Correct tool call plus explicit error from the same attempt | `prompt-only` |
| No image tool | `tool_discovery_completed: true`, recorded candidates, `selected_image_tool_name: null` | `invocation-handoff` |
| Dispatch error | Wrong function or argument caused a local error | Correct and retry; no handoff |
| Result failed | Image exists and visual/file validation fails | `prompt-handoff` |

## Backend Classification

Match [backend-capabilities.json](backend-capabilities.json); classify an unknown path as `full-frame-generative`. When a registered profile exists, run `scripts/evaluate_backend_gate.py`.

`strict-local` requires all of these capabilities before execution: semantic image editing, editable/protected masks, exact passthrough of unedited pixels, verifiable fixed canvas, and a local result file. Prompt language cannot create backend capability. If any item is missing, continue with best-effort generation.

Pillow, NumPy, OpenCV, ImageMagick, FFmpeg, `sips`, and temporary filters are not semantic backends. Use them only for read-only measurement and validation.

## Operation Scope and Generation Policy

| Condition | Policy |
| --- | --- |
| `texture-only` | Preserve source light, highlight map, color, optics, and environment; authorize only skin reflectance/microdetail. |
| `relight-and-skin` | Authorize selected lighting and scene-wide response; preserve source identity, focal plane, DOF, framing, and object structure. |
| Verified `strict-local` | Execute the validated local edit plan; deliver a strict final only after every gate passes. |
| `full-frame-generative` | Generate the full frame as best effort; keep one clear visible target and reduce redraw/detail ambition. |
| Face `<256 px` | Disable added microdetail; retain tone/reflection and the full scene-level lighting target. |
| Text, products, complex props, multiple people, or edge contact | Name only the highest-risk protected objects; still allow source-consistent illumination/reflection. |
| A6 | Authorize the full subject interior to become black while locking outline, proportion, pose, placement, composition, and background. |

For full-frame edits, separate `structural_invariants`, `authorized_appearance_changes`, and one `minimum_visible_improvement` observable at normal size. An almost unchanged result cannot pass as restrained processing.

## V2 Clean Optical Realism

| Signal | Pass | Fail |
| --- | --- | --- |
| Broad tone | Source complexion remains continuous across face, ear, neck, and visible chest; transitions are gentle and light-driven. | Patch-like hue/luminance changes, localized whitening, or face-neck separation. |
| Reflectance/form | Diffuse base and bounded highlights follow key direction and facial curvature; volume comes from illumination and occlusion. | Whole-face gloss, dead-matte flattening, duplicate highlights, or local line darkening used as sculpting. |
| Microdetail | Region-specific detail is faint, nonrepeating, and limited by face scale, focus, distance, and illumination. | Uniform pore fields, texture overlays, global sharpening, or equally crisp skin/hair/clothing/background. |
| Optics | Source focal plane and depth of field remain; edges and background transition optically. | Artificial blur, focus relocation, oversharpened edges, or cutout separation. |

Treat source marks as identity anchors without naming or amplifying them in the generation prompt. Do not create realism by adding imperfections, color variation, grain, or darker facial lines. Under A6, replace skin checks with one continuous black interior.

## Prompt-Priming Safety

- Default to positive photographic behavior: tone continuity, bounded reflection, regional detail, and source focus.
- Keep imperfection bundles, film grain, roughness, gritty texture, and high-contrast language out of default prompts.
- Preserve the source complexion; do not inject `fair`, `whiter`, or beauty-grade terminology.
- Use dramatic darkness only for an explicitly selected backlight, hard-light, low-key, neon, or silhouette recipe.
- If a model becomes artificial, rewrite the SKIN line from scratch; never append more defect terms.

## Lighting Boundaries

- Set `exposure_intent` before fill, shadow, and highlight policy. For unspecified relight, default to `source-matched` or `balanced` with luminous midtones.
- Derive highlight/shadow edge from apparent source size. Never add a second nose shadow/catchlight or create volume by darkening facial lines.
- Preserve bright sources and rims under backlight. Use dramatic shadow loss only when the selected exposure requires it.
- Indoor window light must explain subject, clothing, wall/furniture, reflective objects, and room falloff together. With insufficient evidence, use `match-source`.
- A6 forces `silhouette + fill none`; the interior is black and any narrow rim stays outside it.

Off-camera window confidence: `high` requires a visible window or at least three consistent evidence classes and permits explicit relighting; `medium` requires two and permits low-amplitude correction; `low` uses `match-source`.

## Failure Mapping

| Failure | Action |
| --- | --- |
| Backend lacks strict capability | Continue as `best-effort` and disclose the missing capability. |
| No compatible tool / real tool error | Use `invocation-handoff` / `prompt-only`, respectively. |
| Nearly unchanged, target missed, identity/protection/framing failed | Use `prompt-handoff`; never repair locally. |
| Plastic smoothness remains | Use scale-aware S plus P0/P1; specify bounded highlights and focus-aware regional detail. |
| Skin becomes artificial or the image dims unintentionally | Remove realism-by-defect/darkness terms; reset to clean source tone, bounded reflection, and `source-matched`/`balanced` exposure. |
| A6 retains interior detail or gray fill | Remove S/P, fill, catchlights, and subject lighting; require one continuous black interior. |
