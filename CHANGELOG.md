# Changelog

Notable changes to `xxg-portrait-rebuild-light` are recorded here. This project follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and uses [Semantic Versioning](https://semver.org/).

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
