# Backend Capability and Clean Realism

## Delivery Modes

| Mode | Entry condition and delivery |
| --- | --- |
| `strict-final` | Verified `strict-local` backend, valid edit plan, and every applicable gate passes; may be presented as a strict final. |
| `best-effort` | Native full-frame semantic edit without verified mask or pixel passthrough; label as non-strict best effort and never claim frozen pixels. |
| `invocation-handoff` | Tool discovery completed and no compatible callable exists; return a complete compact prompt without claiming that invocation failed. |
| `prompt-only` | The correct image tool produced a real error; summarize that error and return a complete compact prompt. |
| `prompt-handoff` | A generated image misses the target, changes identity/protected content, or breaks framing; report failure and recompile from the source. |

A small face, complex scene, visible text, edge contact, or weak backend capability can only trigger `best-effort`; none permits refusal. Uniform downscaling is acceptable.

## Native Tool Routing

1. Read the host's native image skill, inspect the source, and search the registered tools. In Codex, inspect `ALL_TOOLS` and prefer `image_gen__imagegen` when actually present.
2. For a local source in Codex, call `tools.image_gen__imagegen({referenced_image_paths: [absolute_path], prompt})`.
3. Treat a wrong member, function name, argument, or `TypeError` as a dispatch error. Correct it from the registered signature and retry.
4. After a real result, classify the backend as `strict-local` or `full-frame-generative`. Do not bypass the host with a CLI or separate API by default.

Never guess `tools.image_gen` or `input_image`. Reading a skill, inspecting an image, creating a task, or announcing generation is not a tool invocation.

## Invocation Evidence

| State | Required evidence | Mode |
| --- | --- | --- |
| Image generated | Image-tool call plus image/result ID or accessible output file | `strict-final` or `best-effort` after validation |
| Invocation failed | Correct tool call plus explicit error from the same attempt | `prompt-only` |
| No image tool | `tool_discovery_completed: true`, recorded candidates, and `selected_image_tool_name: null` | `invocation-handoff` |
| Dispatch error | Wrong function or argument caused a local error | Correct and retry; no handoff yet |
| Result failed | Image exists and visual/file validation fails | `prompt-handoff` |

## Backend Classification

Match [backend-capabilities.json](backend-capabilities.json); classify an unknown path as `full-frame-generative`. When a registered profile exists, run `scripts/evaluate_backend_gate.py`.

`strict-local` requires all of these capabilities to be exposed before execution: semantic image editing, editable and protected masks, exact passthrough of unedited pixels, a verifiable fixed canvas, and a local result file. A prompt saying `freeze` does not create a backend capability. If any item is missing, continue with best-effort generation.

Pillow, NumPy, OpenCV, ImageMagick, FFmpeg, `sips`, and temporary filters are not semantic backends. Use them only for read-only measurement and validation, never to produce the delivered image.

## Generation Policy

| Condition | Policy |
| --- | --- |
| Verified `strict-local` | Execute the validated local edit plan; deliver a strict final only after every gate passes. |
| `full-frame-generative` | Generate the full frame as best effort; reduce redraw and texture ambition while preserving the requested lighting change. |
| Face `<256 px` | Disable invented microtexture; retain the full scene-level lighting target. |
| Text, products, complex props, multiple people, or edge contact | Name only the highest-risk protected objects and discourage structural redraw; still allow source-consistent illumination and reflection. |
| A6 | Do not weaken for a small face. Authorize the full subject interior to become black while locking outline, proportion, pose, composition, and background structure. |

For full-frame edits, keep three distinct concepts: `structural_invariants`, `authorized_appearance_changes`, and one `minimum_visible_improvement` observable at normal size. An almost unchanged image cannot pass as a restrained edit.

## Clean Photographic Realism

| Spatial frequency | Pass | Fail |
| --- | --- | --- |
| Low-frequency color | Source skin baseline remains continuous; luminance follows the light; face, ear, neck, and chest transition broadly. | Red/yellow/gray patches, muddy areas, local whitening, or face-neck separation. |
| Mid-frequency form | Cheekbone, nose, jaw, neck, and shoulder volume comes from illumination, occlusion, and cast shadow. | Deepened eye bags, smile lines, or alar grooves; local clarity, HDR, or aggressive dodge-and-burn. |
| High-frequency surface | Pores, vellus hair, shallow lines, and lip texture remain low-contrast, sparse, and nonrepeating. | Black-dot pores, global grain, chroma noise, sharpening grit, powder flakes, or tiled texture. |

Preserve blackheads, moles, freckles, powder separation, flaking, and dry skin only when present in the source. If the user explicitly requests new blackheads, allow only a few low-contrast points in a high-resolution close-up. Under A6, replace skin visibility checks with a clean continuous black interior free of grain, color contamination, gray patches, and residual facial light.

## Lighting Boundaries

- Set `exposure_intent` before fill, shadow, and highlight policy. Use fill only when the intended exposure requires readable shadows.
- Broad sources create broad transitions; small sources create crisp edges. Never add a second nose shadow or catchlight, and never create volume by burning facial lines.
- Preserve bright sources, background, and rim under backlight. Low-key and silhouette may approach black; highlight-priority may permit controlled bloom or clipping.
- Indoor window light must explain subject, clothing, wall/furniture, reflective objects, and room falloff together. With insufficient evidence, use `match-source`.
- A6 forces `silhouette + fill none`; the subject interior is black, with only a narrow source-consistent rim that stays outside it.

Off-camera window-light confidence: `high` requires a visible window or at least three consistent evidence classes and permits explicit relighting; `medium` requires two and permits only low-amplitude correction; `low` uses `match-source`. Never present an inference as a visible fact.

## Failure Mapping

| Failure | Action |
| --- | --- |
| Backend lacks strict capability | Continue as `best-effort` and disclose the missing capability. |
| No compatible tool / real tool error | Use `invocation-handoff` / `prompt-only`, respectively. |
| Nearly unchanged, target missed, identity/protection/framing failed | Use `prompt-handoff`; never repair locally. |
| Skin becomes dirty, coarse, or artificially sculpted | Replace SKIN with clean continuity plus low-contrast reflection; remove local darkening and grain. |
| A6 retains interior detail or gray fill | Remove ordinary S, fill, catchlights, and subject lighting; require a continuous black interior. |
