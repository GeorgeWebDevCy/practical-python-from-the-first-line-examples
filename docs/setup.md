# Setup on Windows, macOS and Linux

These instructions run the repository's setup example and automated tests.
Use Python 3.11–3.14 for the initial examples. No third-party Python packages
are currently needed. Commands run in a terminal from the repository root.

## Download the examples

Open <https://github.com/GeorgeWebDevCy/python-book-examples>, select **Code →
Download ZIP**, extract it and open a terminal in the extracted folder.
Alternatively, if Git is installed:

```console
git clone https://github.com/GeorgeWebDevCy/python-book-examples.git
cd python-book-examples
```

## Windows — PowerShell

Install Python from [python.org](https://www.python.org/downloads/windows/).
The Python install manager is an option; an existing compatible installation
also works. Open a new PowerShell window and check the version:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m examples.hello
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

If `python` is unavailable but the `py` launcher works, replace the first two
commands with `py --version` and `py -m venv .venv`. Check that the selected
version is in the supported range. Directly calling the environment's Python
avoids PowerShell activation policy issues; no policy changes are required.

## macOS — Terminal (zsh or bash)

Install a compatible Python 3 release using the installer from
[python.org](https://www.python.org/downloads/macos/). Open a new Terminal window:

```bash
python3 --version
python3 -m venv .venv
./.venv/bin/python --version
./.venv/bin/python -m examples.hello
./.venv/bin/python -m unittest discover -s tests -v
```

If several versions are installed, use the versioned command, such as
`python3.14 -m venv .venv`, to choose the environment's interpreter.

## Linux — bash or a similar shell

Check `python3 --version`. Install Python and virtual environment support
through your distribution's package manager if needed. For Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-venv
```

For Fedora:

```bash
sudo dnf install python3
```

The available Python version depends on your distribution and release. Verify
it is 3.11–3.14; use a distribution-supported compatible interpreter if it is
outside that range. Then, in the downloaded repository:

```bash
python3 --version
python3 -m venv .venv
./.venv/bin/python --version
./.venv/bin/python -m examples.hello
./.venv/bin/python -m unittest discover -s tests -v
```

## Confirm setup

The example prints one line:

```text
Hello, Python!
```

The test command should finish with `OK`. A failing test or traceback means
setup or code needs investigation; do not treat it as successful execution.
If Python cannot find `examples` or reports zero tests, ensure the terminal is
in the repository root, where `README.md`, `examples/` and `tests/` are present.
If environment creation fails on Debian/Ubuntu, confirm `python3-venv` is installed.

Activation is optional. Use the explicit Python paths above consistently.
To use `python` as shorthand, run `.\.venv\Scripts\Activate.ps1` on Windows
(if local policy permits), or `source .venv/bin/activate` on macOS/Linux.
Run `deactivate` when finished. When future examples add dependencies, install
them with this environment's `python -m pip` and the example's documented
requirements file. Never install them into the operating system's Python.

References: Python's official [Windows guide](https://docs.python.org/3/using/windows.html),
[macOS guide](https://docs.python.org/3/using/mac.html),
[Unix guide](https://docs.python.org/3/using/unix.html), and
[virtual environments guide](https://docs.python.org/3/library/venv.html).
