# Changelog

All notable changes to the portfolio site. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.2.0] - 2026-07-22

### Changed

- Switched the site color scheme from labforge's dark "instrument" theme to
  its light "paper" theme (warm paper surfaces, graphite ink, vermilion
  accent; steel-blue secondary, dark-rust highlight for text contrast).

### Added

- LinkedIn and ORCID links on the contact page.

## [0.1.0] - 2026-07-22

### Added

- Initial site: routed Flet SPA with hero, CV, presentations, projects, and
  contact views.
- Project registry (`src/data/projects.py`) featuring labforge and FORESEE
  Lab with screenshot galleries, plus HNLCalc and FORESEE research-software
  cards; conditional GitHub / PyPI / live-demo / docs buttons.
- Dark "instrument" theme adopted from labforge's design system.
- Ph.D. thesis feature card linking to eScholarship.
- GitHub Actions workflow building `flet build web` and deploying to GitHub
  Pages.
- Repo docs: CLAUDE.md (architecture + privacy rule), TASKLOG.md.
