"""Prompt privately for a key, then launch the optional billable live GUI."""
import getpass
import os
import subprocess
import sys
import warnings


def main():
    print("Optional live API mode: requests may incur charges.")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", getpass.GetPassWarning)
            key = getpass.getpass("OpenAI API key (hidden): ").strip()
    except (getpass.GetPassWarning, EOFError, KeyboardInterrupt):
        print("Hidden input was unavailable or cancelled. No request made.")
        return 1
    model = input("Model available to your project: ").strip()
    if not key or not model:
        print("Both values are required. No request made.")
        return 1
    environment = os.environ.copy()
    environment.update(OPENAI_API_KEY=key, OPENAI_MODEL=model)
    return subprocess.run(
        [sys.executable, "-m", "examples.ch21.assistant_gui", "--live"],
        env=environment,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
