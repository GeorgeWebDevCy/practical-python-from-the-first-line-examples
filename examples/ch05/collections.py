topics = ["files", "loops", "tests"]
topics.append("functions")
first_topic = topics[0]

session = {"topic": first_topic, "minutes": 25}
session["minutes"] = 30

tags = {"beginner", "practical", "beginner"}
time_slot = (9, 30)

print(f"First topic: {first_topic}")
print(f"Last topic: {topics[-1]}")
print(f"Duration: {session['minutes']} minutes")
print(f"Unique tags: {len(tags)}")
print(f"Start: {time_slot[0]:02d}:{time_slot[1]:02d}")
