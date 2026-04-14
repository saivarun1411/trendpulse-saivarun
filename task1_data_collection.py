import requests
import json
import os
from datetime import datetime

print("STARTING SCRIPT")

base = "https://hacker-news.firebaseio.com/v0"

# create data folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# file name with date
today = datetime.now().strftime("%Y%m%d")
file_name = "data/trends_" + today + ".json"

# fetch top story ids
try:
    print("Fetching top stories...")
    top = requests.get(base + "/topstories.json", timeout=5)
    ids = top.json()
    print("Top stories fetched")
except:
    print("Error fetching top stories")
    exit()

stories = []

# fetch more but stop at 100
for i in range(200):
    try:
        print("Fetching story", i)

        url = base + "/item/" + str(ids[i]) + ".json"
        res = requests.get(url, timeout=5)
        s = res.json()

        if s is None:
            continue

        item = {
            "id": s.get("id"),
            "title": s.get("title"),
            "author": s.get("by"),
            "score": s.get("score"),
            "time": s.get("time"),
            "url": s.get("url"),
            "comments": s.get("descendants")
        }

        stories.append(item)

        # stop when 100 stories collected
        if len(stories) >= 100:
            break

    except:
        print("Skipping story", i)
        continue

# save JSON file
with open(file_name, "w") as f:
    json.dump(stories, f, indent=4)

print("Collected", len(stories), "stories. Saved to", file_name)