# Repo Ready Check

> A zero-dependency Python CLI that scores whether a repository is ready to publish, collaborate on, and maintain.

面向个人开发者和小团队的仓库体检工具：运行一次检查，得到 0–100 分、具体缺口和可直接修复的下一步。

[![CI](https://github.com/chengyangguang47-cloud/repo-ready-check/actions/workflows/ci.yml/badge.svg)](https://github.com/chengyangguang47-cloud/repo-ready-check/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/chengyangguang47-cloud/repo-ready-check)](https://github.com/chengyangguang47-cloud/repo-ready-check/releases)
[![License](https://img.shields.io/github/license/chengyangguang47-cloud/repo-ready-check)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)

Repo Ready Check scans the files and automation people expect before they contribute to or ship a project. It never uploads source code, has no runtime dependencies, and works locally or in GitHub Actions.

## Why it exists

A project can run correctly and still be difficult to trust. Missing documentation, tests, licensing, security guidance, or CI creates friction for contributors and future customers. This tool turns those gaps into a small, repeatable quality gate.

## Features

- Scores ten repository essentials on a 100-point scale.
- Prints actionable fixes instead of only reporting failures.
- Supports strict mode for CI quality gates.
- Supports JSON output for scripts and dashboards.
- Uses only the Python standard library at runtime.
- Includes unit tests, issue forms, pull request guidance, and automated releases.

## Install

### Install the latest published wheel

```powershell
python -m pip install "https://github.com/chengyangguang47-cloud/repo-ready-check/releases/download/v0.1.0/repo_ready_check-0.1.0-py3-none-any.whl"
```

### Install from source

```powershell
git clone https://github.com/chengyangguang47-cloud/repo-ready-check.git
cd repo-ready-check
python -m pip install -e .
```

## Usage

Run the audit from the root of the repository you want to inspect:

```powershell
repo-ready-check .
```

Use strict mode when a score below 80 should fail the command:

```powershell
repo-ready-check . --strict
```

Generate machine-readable output:

```powershell
repo-ready-check . --json
```

You can also run it without installing the console script:

```powershell
python -m repo_ready_check .
```

## Example output

```text
Repo Ready Check
Path: C:\projects\demo
Score: 85/100

[PASS] README.md                 15/15
[PASS] License                  10/10
[PASS] Tests                    15/15
[PASS] CI workflow              15/15
[FAIL] Pull request template     0/5

Next actions:
- Add .github/pull_request_template.md
```

## Checks

| Check | Weight |
| --- | ---: |
| README.md | 15 |
| LICENSE | 10 |
| .gitignore | 10 |
| Project manifest | 10 |
| Tests | 15 |
| GitHub Actions workflow | 15 |
| Issue template | 10 |
| Pull request template | 5 |
| SECURITY.md | 5 |
| CHANGELOG.md | 5 |

The total is 100 points. Strict mode passes at 80 points or above.

## CI and releases

Every push and pull request runs the test suite and a strict repository audit in [GitHub Actions](.github/workflows/ci.yml). Pushing a `v*` tag builds a wheel and source archive, then creates a GitHub Release through [the release workflow](.github/workflows/release.yml).

- [Latest release](https://github.com/chengyangguang47-cloud/repo-ready-check/releases/latest)
- [CI runs](https://github.com/chengyangguang47-cloud/repo-ready-check/actions)
- [Changelog](CHANGELOG.md)

## Development

This project targets Python 3.10+ and keeps runtime dependencies at zero.

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python -m repo_ready_check . --strict
```

## Portfolio use cases

Repo Ready Check is also a small example of a service that can be delivered to a client:

- repository health and release-readiness audits;
- README, issue template, and contribution-flow setup;
- GitHub Actions CI and automated release configuration;
- lightweight Python automation for recurring maintenance work.

The goal is to make a repository easier to trust, easier to contribute to, and easier to maintain.

## Roadmap

- [ ] Markdown content quality checks
- [ ] GitHub Actions permission checks
- [ ] HTML report export
- [ ] Generated repair patches
- [ ] Standalone GitHub Action distribution

## License

MIT. See [LICENSE](LICENSE).
