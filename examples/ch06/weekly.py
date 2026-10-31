sessions = [15, 20, 10]
total_minutes = 0

for number, minutes in enumerate(sessions, start=1):
    total_minutes = total_minutes + minutes
    print(f"Session {number}: {minutes} minutes")

print(f"Weekly total: {total_minutes} minutes")

remaining = 3
while remaining > 0:
    print(f"Countdown: {remaining}")
    remaining = remaining - 1
