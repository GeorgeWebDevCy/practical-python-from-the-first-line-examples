name = input("Your name: ").strip()
minutes_text = input("Practice minutes: ").strip()
practice_minutes = int(minutes_text)
break_minutes = 5
total_minutes = practice_minutes + break_minutes

print(f"Plan for {name}")
print(f"Total including break: {total_minutes} minutes")
