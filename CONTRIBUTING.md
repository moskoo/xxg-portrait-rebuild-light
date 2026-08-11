# Contributing

Thanks for helping improve `xxg-portrait-rebuild-light`. Contributions that make portrait relighting more reliable, prompts more concise, or agent compatibility clearer are welcome.

## Good contribution areas

- Lighting, skin, color-temperature, and atmosphere recipes.
- Prompt compilation and failure-handoff behavior.
- Compatibility with Codex, Claude Code, OpenClaw, and other agent runtimes.
- Read-only validation scripts and backend capability checks.
- Documentation fixes and English, Chinese, Japanese, or Korean translations.

## Before opening a change

- Search existing issues and pull requests to avoid duplicate work.
- Open an issue first for substantial workflow or behavior changes.
- Never commit private portraits, biometric data, credentials, or images without clear redistribution rights.
- Keep model-facing prompts concise and physically specific. Avoid large synonym lists and conflicting constraints.
- Preserve identity, natural facial asymmetry, source composition, clean skin-tone continuity, and physically coherent lighting as the default behavior.
- Do not add local Pillow, NumPy, OpenCV, ImageMagick, or filter-based rendering as a substitute for an image-edit model.

## Local setup

```bash
git clone https://github.com/moskoo/xxg-portrait-rebuild-light.git
cd xxg-portrait-rebuild-light
python3 -m pip install -r requirements.txt
```

## Validation

Before submitting a pull request:

1. Run any script you changed with representative, non-sensitive fixtures.
2. Confirm all four README files keep equivalent recipe codes, commands, and behavior boundaries.
3. Check Markdown links and ensure the English `README.md` remains the default entry point.
4. Run `git diff --check` and review the complete diff.
5. Add a concise entry under `Unreleased` in `CHANGELOG.md` for user-visible changes.

For changes to `SKILL.md`, also run the current Agent Skills validator available in your agent environment.

## Pull requests

Keep each pull request focused. Explain the problem, the behavioral change, how it was verified, and any agent or image-edit backend limitations. Screenshots or before/after samples are useful when they are safe to redistribute, but they should not expose private people without permission.

By contributing, you agree that your contribution is licensed under the repository's [MIT License](LICENSE).
