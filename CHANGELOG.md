# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CICD: CI workflow
- CICD: Changelog workflow
- Complete API documentation
- Set precision of time legends to the millisecond

### Changed

- **Breaking:** Rename `timestamped` argument of `plot2` to `time`

### Fixed

- Clean up dead code
- Correct type annotations
- Format values in axes to update ticks when zooming
- Update `resources.path` to `resources.files`

### Removed

- Intermediate `array2string` utility function

## [1.0.0] - 2024-10-29

- Extract this project from [foxplot](https://github.com/stephane-caron/foxplot)
- Start this changelog

[unreleased]: https://github.com/stephane-caron/foxplot/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/stephane-caron/foxplot/releases/tag/v1.0.0
