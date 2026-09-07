# Changelog

Notable changes to `xxg-portrait-rebuild-light` are recorded here. This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and uses [Semantic Versioning](https://semver.org/).

## [2.1.0] - 2026-09-07

### Added

- Added `E0–E7` exposure recipes with explicit highlight, midtone, shadow, and black-point placement.
- Added `G0–G8` color/style grades and `D0–D8` capture-response recipes for modern full-frame, medium-format, 35mm negative, CCD compact, point-and-shoot flash, smartphone computational, instant-film, and disposable-camera looks.
- Added `tone-and-exposure`, `capture-style`, and explicit `optical-restyle` scope boundaries.
- Added source-safe production prompts for tonal correction, medium-format editorial, 35mm documentary, point-and-shoot flash, and smartphone available-light response.

### Changed

- Camera and film labels now compile into observable tonal steps, highlight roll-off, color separation, microcontrast, sharpening, and dynamic-range behavior instead of acting as unsupported style tokens.
- Capture-style edits preserve viewpoint, perspective, crop, focal plane, and depth of field unless an optical restyle is explicitly requested.
- Updated all four README languages, validation gates, strict edit-plan fields, and handoff rules for L/E/S/P/T/G/D/A selection.

## [2.0.0] - 2026-08-29

### Changed

- Rebuilt portrait realism around separate broad tone, bounded reflection, scale/focus-aware microdetail, and optical focus hierarchy instead of dirt, darkness, grain, or random imperfections.
- Added explicit `texture-only` and `relight-and-skin` scopes so skin recovery can preserve source lighting while relighting can produce physically meaningful exposure and shadow changes.
- Added `P0–P6` skin-finish recipes and updated every example to select one L, S, P, T, and optional A recipe.
- Added a six-part identity signature covering face outline, features, hairline, source complexion anchors, styling, and apparent age/demeanor.
- Removed default wording that could provoke whole-face gloss, repeated pore overlays, gritty sharpening, dirty color variation, unintended dimming, or fake local contrast.
- Updated English, Simplified Chinese, Japanese, and Korean documentation for the V2 prompt contract.

## [1.0.4] - 2026-08-24

### Changed

- Rewrote all agent-facing runtime instructions and image-edit prompts in precise production English, using explicit source geometry, exposure behavior, falloff, and observable results instead of literal translation.
- Preserved every lighting, skin, routing, validation, aspect-ratio, and A6 silhouette behavior while standardizing the four-line prompt contract to 40–90 English words.

## [1.0.3] - 2026-08-23

### Changed

- Reduced repeated runtime guidance and shortened model-facing prompts while preserving all lighting, skin, routing, validation, and A6 behaviors.

## [1.0.2] - 2026-08-13

### Added

- `A6` full-black backlit subject silhouette recipe with forced silhouette exposure and dedicated validation rules.
- MIT license and contribution guidelines.
- English, Simplified Chinese, Japanese, and Korean documentation links for ongoing maintenance.
- GitHub discovery topics for agent skills, image editing, prompt engineering, and relighting.

## [1.0.0] - 2026-08-11

### Added

- Initial portrait relighting and clean photographic skin-texture skill.
- Director-style lighting recipes, compact prompt compilation, agent-native image-edit routing, and read-only validation scripts.
