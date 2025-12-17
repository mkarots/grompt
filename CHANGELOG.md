# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Hash-based change detection in commit command
- `load_variables()` helper function for loading test inputs from YAML files
- Basic prompt validation (syntax and rendering checks)
- Validation integrated into commit command

### Changed
- Commit command now only increments version when content actually changes
- Added `--force` flag to commit command to override change detection

## [0.2.1] - 2024-01-XX

### Added
- Initial release
- Prompt storage as YAML files
- Version tracking
- CLI commands (init, add, commit, test)
- Python API for loading and rendering prompts
- Template rendering with Jinja2
- System message support
- Parameters and metadata support

[Unreleased]: https://github.com/mkarots/grompt/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/mkarots/grompt/releases/tag/v0.2.1

