from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable


@dataclass(frozen=True)
class CheckResult:
    key: str
    label: str
    passed: bool
    points: int
    max_points: int
    advice: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _has_any_file(root: Path, names: Iterable[str]) -> bool:
    return any((root / name).is_file() for name in names)


def _has_license(root: Path) -> bool:
    return any(path.is_file() for path in root.glob("LICENSE*"))


def _has_manifest(root: Path) -> bool:
    return _has_any_file(
        root,
        (
            "pyproject.toml",
            "package.json",
            "Cargo.toml",
            "go.mod",
            "pom.xml",
            "requirements.txt",
        ),
    )


def _has_tests(root: Path) -> bool:
    for name in ("tests", "test", "spec"):
        path = root / name
        if path.is_dir() and any(path.iterdir()):
            return True
    return False


def _has_workflow(root: Path) -> bool:
    workflow_dir = root / ".github" / "workflows"
    return workflow_dir.is_dir() and any(
        path.suffix.lower() in {".yml", ".yaml"} for path in workflow_dir.iterdir()
    )


def _has_issue_template(root: Path) -> bool:
    template_dir = root / ".github" / "ISSUE_TEMPLATE"
    if not template_dir.is_dir():
        return False
    return any(path.suffix.lower() in {".yml", ".yaml", ".md"} for path in template_dir.iterdir())


def _has_pull_request_template(root: Path) -> bool:
    candidates = (
        root / ".github" / "pull_request_template.md",
        root / ".github" / "PULL_REQUEST_TEMPLATE.md",
        root / "PULL_REQUEST_TEMPLATE.md",
    )
    return any(path.is_file() for path in candidates)


def _check(
    key: str,
    label: str,
    root: Path,
    predicate: Callable[[Path], bool],
    max_points: int,
    advice: str,
) -> CheckResult:
    passed = predicate(root)
    return CheckResult(
        key=key,
        label=label,
        passed=passed,
        points=max_points if passed else 0,
        max_points=max_points,
        advice="" if passed else advice,
    )


def audit_repo(root: str | Path) -> dict[str, object]:
    repo = Path(root).expanduser().resolve()
    if not repo.is_dir():
        raise ValueError(f"Not a directory: {repo}")

    checks = [
        _check("readme", "README.md", repo, lambda p: (p / "README.md").is_file(), 15, "Add a README with the problem, setup, usage, and examples."),
        _check("license", "License", repo, _has_license, 10, "Add a LICENSE file so people know how the project can be used."),
        _check("gitignore", ".gitignore", repo, lambda p: (p / ".gitignore").is_file(), 10, "Add a .gitignore for generated files and local secrets."),
        _check("manifest", "Project manifest", repo, _has_manifest, 10, "Add a package manifest such as pyproject.toml or package.json."),
        _check("tests", "Tests", repo, _has_tests, 15, "Add a tests/ directory with at least one meaningful test."),
        _check("workflow", "CI workflow", repo, _has_workflow, 15, "Add a GitHub Actions workflow that runs tests on pushes and pull requests."),
        _check("issue_template", "Issue template", repo, _has_issue_template, 10, "Add a bug report or feature request template under .github/ISSUE_TEMPLATE."),
        _check("pull_request_template", "Pull request template", repo, _has_pull_request_template, 5, "Add .github/pull_request_template.md."),
        _check("security", "Security policy", repo, lambda p: _has_any_file(p, ("SECURITY.md", ".github/SECURITY.md")), 5, "Add SECURITY.md with private vulnerability reporting guidance."),
        _check("changelog", "Changelog", repo, lambda p: _has_any_file(p, ("CHANGELOG.md", "HISTORY.md")), 5, "Add CHANGELOG.md to explain releases and user-visible changes."),
    ]

    score = sum(item.points for item in checks)
    return {
        "path": str(repo),
        "score": score,
        "max_score": 100,
        "percentage": score,
        "checks": [item.as_dict() for item in checks],
        "next_actions": [item.advice for item in checks if item.advice],
    }


def render_text(report: dict[str, object]) -> str:
    lines = [
        "Repo Ready Check",
        f"Path: {report['path']}",
        f"Score: {report['score']}/{report['max_score']}",
        "",
    ]
    for item in report["checks"]:
        mark = "PASS" if item["passed"] else "FAIL"
        lines.append(
            f"[{mark}] {item['label']:<24} "
            f"{item['points']:>2}/{item['max_points']}"
        )
    actions = report["next_actions"]
    if actions:
        lines.extend(["", "Next actions:"])
        lines.extend(f"- {action}" for action in actions)
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit a repository for release and collaboration readiness."
    )
    parser.add_argument("path", nargs="?", default=".", help="Repository path, default: current directory")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 when the score is below 80")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = audit_repo(args.path)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))

    return 1 if args.strict and int(report["score"]) < 80 else 0


if __name__ == "__main__":
    raise SystemExit(main())
