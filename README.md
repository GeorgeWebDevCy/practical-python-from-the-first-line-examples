# Python Book — Code Examples

Public companion code for George Nicolaou's Python book (working title).
Runnable examples now cover all 18 chapters of the first book draft. Begin
with the setup check, then [Chapter 1's saved programs](examples/ch01/README.md).

Start with the [Windows, macOS and Linux setup guide](docs/setup.md).
The initial compatibility target is Python 3.11–3.14. The book's final supported
versions will be documented as its scope is established.

From the repository root, using your virtual environment's Python:

```console
python -m examples.hello
python -m unittest discover -s tests -v
```

Expected example output: `Hello, Python!`

## Examples and tests

- `examples/hello.py`: confirms that Python can run the downloaded code.
- `tests/test_hello.py`: checks greeting behaviour and exact command output.
- `examples/ch02/` through `examples/ch18/`: chapter code and per-OS run instructions.
- `examples/solutions.py`: tested reference exercise behaviours.
- `examples/verification.py`: documented command checks with temporary files and local HTTP fixtures.
- GitHub Actions runs tests on Windows, macOS and Linux with Python 3.11–3.14.
  Check the Actions tab for actual results; a configured matrix is not evidence
  that every platform has passed.

Future chapter examples must include a README with commands, expected output,
dependencies and any platform limits, plus tests for the behaviour being taught.
Tests must use local fixtures or temporary directories rather than real
credentials, paid services or a reader's personal files. Tests must run the
examples, not just check their syntax. Dependency additions require explicit
installation instructions and reproducible version constraints.

Only reader-facing code, tests and documentation belong here. The manuscript
and the author's local reference materials are maintained separately.

## Project commands

With the environment active, from this root:

| Project | Command | Effect |
|---|---|---|
| File organiser | `python examples/ch12/organise.py SOURCE NEW_DESTINATION` | Preview; add `--apply` to copy files |
| CSV report | `python examples/ch13/report.py` | Print known sample totals and rejected rows |
| SVG chart | `python examples/ch14/chart.py` | Create a new `costs.svg` in the current directory |
| Local HTTP fixture | `python -m examples.toolkit.fixture` | Serve controlled data until Ctrl+C |
| HTTP client | `python examples/ch16/fetch.py http://127.0.0.1:8765/sessions` | Fetch from that running fixture |
| Local board | `python -m examples.ch17.board --data requests.json` | Serve read-only at http://127.0.0.1:8766/ until Ctrl+C |
| Request updater | `python -m examples.ch18.requests_cli --data requests.json add "A task"` | Create or update the selected JSON file |

Use the chapter READMEs for preparation, output and limits. Run servers locally
only; the teaching HTTP server is not a public deployment configuration.
The request updater assumes a single writer. The organiser creates grouped
copies and retains originals; a failed run can leave partial output.
