# Public Python book examples

- Keep this repository public and reader-facing. Do not copy manuscript chapters,
  local reference books, credentials or publishing account records here.
- Add runnable examples with behaviour tests, documented expected output and
  setup instructions for Windows, macOS and Linux. Keep commands current when
  dependencies or supported Python versions change.
- Run `python -m unittest discover -s tests -v` before committing. GitHub Actions
  must pass on the supported OS/Python matrix before calling an example verified
  across platforms. Disclose untested platform-specific behaviour.
- Keep code cross-platform where practical: pathlib, UTF-8 text, temporary test
  files, and no hardcoded personal paths. Document deliberate error examples.
- Commit and push coherent, tested increments as work proceeds. Review changes
  before publishing them to this public repository.
- On the author's workstation follow `C:/Users/georg/.codex/RTK.md` and prefix
  shell commands with `rtk` (use `rtk proxy` when needed).
- Initial compatibility target: Python 3.11–3.14. Book scope and title remain
  provisional. Runnable examples for all 18 first-draft chapters and reference
  exercise behaviours are available. Documented command cases are in
  `examples/cases.json`; `python -m examples.verification` executes them in
  temporary directories. Chapter 17's long-running server is checked by the
  live HTTP integration tests instead of a one-shot command expectation.
