def session_total(practice_minutes, break_minutes=5):
    """Return a total for nonnegative whole-minute durations."""
    for value in (practice_minutes, break_minutes):
        if type(value) is not int or value < 0:
            raise ValueError("Durations must be nonnegative whole minutes")
    return practice_minutes + break_minutes
