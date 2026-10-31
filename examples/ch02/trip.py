destination = "Harbour"
distance_km = 18
speed_kmh = 12
stop_minutes = 10

travel_minutes = distance_km / speed_kmh * 60
total_minutes = travel_minutes + stop_minutes

print(f"Destination: {destination}")
print(f"Travel minutes: {travel_minutes:.0f}")
print(f"Including stop: {total_minutes:.0f}")
