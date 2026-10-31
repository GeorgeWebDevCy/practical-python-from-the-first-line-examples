# GUI and optional AI setup

The core projects use Python 3.11–3.14 and the standard library. Tkinter is
an optional component of a Python distribution, not a package to install
with `pip install tkinter`.

## Windows

In the official traditional Python installer, select **tcl/tk and IDLE**.
If you previously omitted it, use the installer's supported modification
workflow. Your organisation may manage installation permissions. The book's
separate custom installation directory was used only for demonstration;
readers can retain the default installation location.

From the companion repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m tkinter
.\.venv\Scripts\python.exe -m examples.ch19.timer
.\.venv\Scripts\python.exe -m examples.ch20.tracker --data requests.json
.\.venv\Scripts\python.exe -m examples.ch21.assistant_gui --data requests.json
```

Close the Tk demonstration window and each application before running the
next command if your terminal is waiting for it to finish. Use `py` or an
explicit Python path for environment creation if that selects your intended
installation. No PowerShell execution-policy changes are needed.

## macOS

Use a compatible python.org installation with its supplied Tcl/Tk support,
or follow your distributor's specific Tk instructions. Do not assume every
system or package-manager interpreter includes the same optional components.

```bash
python3 -m venv .venv
./.venv/bin/python -m tkinter
./.venv/bin/python -m examples.ch19.timer
./.venv/bin/python -m examples.ch20.tracker --data requests.json
./.venv/bin/python -m examples.ch21.assistant_gui --data requests.json
```

## Linux desktop

On Debian/Ubuntu, install matching distribution components with
`sudo apt install python3-tk python3-venv`. On Fedora, the matching Tk package
is commonly `python3-tkinter`; follow your distribution's documentation and
ensure it matches the interpreter used for your environment. A separately
installed Python may need a different build or package.

Use the same environment/application commands as macOS above. A graphical
desktop session is required to see the windows. For automated GUI tests on
a headless Debian/Ubuntu host, install `xvfb` and `xauth`, then run:

```bash
xvfb-run -a ./.venv/bin/python -m unittest discover -s tests -v
```

Xvfb supplies a test display. It does not turn a remote shell into a visible
interactive desktop for a reader. A missing display and a missing Tk module
are different setup failures; neither should be hidden by skipping every test.

## AI: keep the no-account path first

Run the planner without `--live` to use a fixed local demonstration. To opt
into live requests, create/manage your own API access through the provider's
official platform and review its current billing and data controls. An API
subscription/account is separate from access to a chat product. No account
creation or purchase is required for the offline chapters.

Set `OPENAI_API_KEY` through your local secret-management or process-environment
workflow and `OPENAI_MODEL` to an available structured-output-capable model.
For example, to set the nonsensitive model variable for this shell, replacing
the value with your chosen available model:

```powershell
$env:OPENAI_MODEL = "your-available-model"
```

```bash
export OPENAI_MODEL="your-available-model"
```

The shown value is a placeholder, not a real model identifier. Keys must not
be committed or photographed; this guide intentionally does not ask you to
type a key into a command that may be saved in terminal history. Launch the
live application only after both variables are set in the environment that
will start Python. The consent control applies to the particular goal request.

The live HTTP shape follows the official [Responses API structured-output
guide](https://developers.openai.com/api/docs/guides/structured-outputs).
Model access, prices and account limits can change; check the official platform
before a live run. Output limits constrain generated tokens, not the entire
bill. Review results as suggestions, not verified facts or completed work.

For interactive private input, run `python -m examples.ch21.live_launcher`
from a real terminal at the repository root. It prompts for a key with hidden
input and then a model identifier. It stops if hidden input is unavailable.
The values are passed only in the child process environment, not command-line
arguments. The launched live GUI still requires its goal-send confirmation.
