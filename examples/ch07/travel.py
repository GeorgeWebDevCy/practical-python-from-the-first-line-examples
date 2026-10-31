def travel_minutes(distance_km, speed_kmh=12):
    """Estimate minutes for a nonnegative distance and positive speed."""
    if distance_km < 0:
        raise ValueError("Distance cannot be negative")
    if speed_kmh <= 0:
        raise ValueError("Speed must be positive")
    return distance_km / speed_kmh * 60


if __name__ == "__main__":
    estimate = travel_minutes(18)
    print(f"Estimated minutes: {estimate:.0f}")
