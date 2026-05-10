# PR Checks Design

**Date:** 2026-05-10  
**Status:** Approved  

## Overview

Add automated PR checks to `chat-explore` covering code quality (linting + formatting) and tests. Checks run both locally via pre-commit hooks and remotely via GitHub Actions.

## Tooling

- **ruff** — linting and formatting (replaces black + flake8)
- **pre-commit** — runs ruff hooks on every local commit
- **pytest** — existing test suite, no coverage threshold

## Pre-commit Hooks

File: `.pre-commit-config.yaml`

Two hooks on every `git commit`:
1. `ruff check .` — lint; fails on violations
2. `ruff format --check .` — formatting; fails if code is not formatted

Developers run `pre-commit install` once after cloning. ruff version is pinned in the config for reproducibility.

## GitHub Actions Workflow

File: `.github/workflows/pr-checks.yml`

Triggers: `pull_request` targeting `master`, and `push` to `master`.

Single job on `ubuntu-latest`:
1. Checkout code
2. Set up Python 3.11
3. Install `uv`
4. Install dev dependencies via `uv sync --group dev`
5. Run `ruff check .`
6. Run `ruff format --check .`
7. Run `pytest`

All steps must pass for the PR check to be green.

## Dependency Changes

In `pyproject.toml`:
- Remove `black` from `[project] dependencies` (was incorrectly in prod deps; ruff replaces it)
- Add `ruff` to `[dependency-groups] dev`
- Add `pre-commit` to `[dependency-groups] dev`
