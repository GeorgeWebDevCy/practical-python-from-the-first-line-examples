"""A dependency-free setup check: python -m examples.hello."""


def greeting(name: str = "Python") -> str:
    """Return a greeting for a name, trimming surrounding whitespace."""
    return f"Hello, {name.strip()}!"


if __name__ == "__main__":
    print(greeting())
