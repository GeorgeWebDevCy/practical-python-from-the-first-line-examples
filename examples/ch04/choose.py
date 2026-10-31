minutes = 20

if minutes < 0:
    message = "Minutes cannot be negative."
elif minutes == 0:
    message = "No session planned."
elif minutes < 20:
    message = "Review one example."
else:
    message = "Complete a practice exercise."

print(message)
