def parse_minutes(text):
    """Return a nonnegative integer duration from text."""
    value = int(text.strip())
    if value < 0:
        raise ValueError("Minutes cannot be negative")
    return value


if __name__ == "__main__":
    for sample in [" 25 ", "0", "-2", "many"]:
        try:
            minutes = parse_minutes(sample)
        except ValueError:
            print(f"{sample!r}: enter a nonnegative whole number")
        else:
            print(f"{sample!r}: {minutes} minutes")
