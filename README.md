# Python Book — Code Examples

Public companion code for George Nicolaou's Python book (working title).
Chapter examples will be added as the book is written. The current example is
a setup check, not a drafted chapter.

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
