# Optional AI task planner

The default mode is a deterministic demonstration. It makes no network
requests and needs no API key, account or paid service. Its fixed suggestions
are explicitly labelled as a demonstration, not as AI-generated results.

From the repository root, with your environment selected:

```console
python -m examples.ch21.planning "Prepare a workshop"
python -m examples.ch21.assistant_gui --data requests.json
```

On Windows without activation, replace `python` with `.\.venv\Scripts\python.exe`.
On macOS/Linux, use `./.venv/bin/python`. The GUI requires working Tkinter.

Enter a goal, choose Suggest steps, then review the candidates. No candidate
is saved automatically. Select a suggestion and choose Add selected suggestion
to save only its title into the existing request store. Categories remain
advisory display information. The interface remains responsive during provider
work because only the main Tk thread updates widgets.

## Optional live mode

Read [GUI and AI setup](../../docs/gui-and-ai-setup.md). Configure
`OPENAI_API_KEY` securely in the process environment and `OPENAI_MODEL` with an
available model supporting Responses API structured outputs. No model is silently
chosen and no key is read from a committed file. Never paste keys into issues,
screenshots, source code, the goal field or chat. Only the goal and fixed
instructions/schema are sent; your JSON request file is not uploaded.

```console
python -m examples.ch21.assistant_gui --data requests.json --live
```

Live mode is visibly labelled. Review the goal and select the consent box
before requesting suggestions. Requests may incur API charges. There are no
automatic retries. `store: false` is included in the request; this is not a
claim that all provider retention is disabled. Review provider data controls
before supplying sensitive material. Use fictitious goals while learning.

The client bounds response size, checks completed/refused/incomplete responses,
validates task structure and length, and masks raw provider errors. Suggested
text is never executed. It cannot run commands or access your files.

## What was tested

Offline behaviour, real Tk callbacks, review-before-save, close during worker
execution, HTTP request shape through a local fixture, refusal, incomplete
responses, malformed output, missing configuration, quotas, timeouts and error
redaction are covered by automated tests. These tests do not make paid API
requests. An authenticated live-provider request has not been performed on the
author's machine because no provider key is configured. Do not describe those
fixture results as a successful live OpenAI call.
