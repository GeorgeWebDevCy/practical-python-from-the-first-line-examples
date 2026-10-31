from examples.toolkit.durations import session_total


def main():
    total = session_total(practice_minutes=25, break_minutes=5)
    print(f"Session including break: {total} minutes")


if __name__ == "__main__":
    main()
