import requests
import json
import os
import csv
import pandas as pd
from datetime import datetime

# ===== CONFIG =====
DITTO_BASE = "http://localhost:8080"
USERNAME = "ditto"
PASSWORD = "ditto"

url = f"{DITTO_BASE}/api/2/things"

headers = {
    "Accept": "text/event-stream",
}

# ===== Twin dictionary =====
# the dictionary for the .json file mapping
twin_name_map = pd.read_csv("dataset/machdict.csv")

# ===== Create folder =====
output_folder = "timestamped_data"
os.makedirs(output_folder, exist_ok=True)


def save_event(event_type, data_lines):
    try:
        raw_data = "\n".join(data_lines)
        json_data = json.loads(raw_data)

        data_values = json_data["features"]["sensors"]["properties"]

        # Extract twin ID
        thing_id = json_data.get("thingId")

        if not thing_id:
            return  # skip if malformed

        # Map to readable name
        file_name = twin_name_map.get(thing_id, thing_id.replace(":", "_"))

        csv_path = os.path.join(output_folder, f"{file_name}.csv")

        # Get timestamp from Ditto or fallback
        timestamp = json_data.get("_metadata", {}).get(
            "timestamp", datetime.utcnow().isoformat()
        )

        # Write row
        file_exists = os.path.exists(csv_path)

        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(["timestamp", "tempC", "vibMms", "dB", "oilLvlpct", "coolLvlpct", "kW", "aiSuperv",
                                "laserIntensity", "hydrPressure",  "coolLvlMin", "heatIndex", "aiOverrideEvents"])

            writer.writerow([
                timestamp,
                data_values.get("tempC"),
                data_values.get("vibMms"),
                data_values.get("dB"),
                data_values.get("oilLvlpct"),
                data_values.get("coolLvlpct"),
                data_values.get("kW"),
                data_values.get("aiSuperv"),
                data_values.get("laserIntensity"),
                data_values.get("hydrPressure"),
                data_values.get("coolLvlMin"),
                data_values.get("heatIndex"),
                data_values.get("aiOverrideEvents"),
            ])

        print(f"Saved event for {file_name}")

    except Exception as e:
        print("Error:", e)


# ===== Stream events =====
with requests.get(url, headers=headers, auth=(USERNAME, PASSWORD), stream=True) as r:
    r.raise_for_status()

    event_type = None
    data_lines = []

    for raw_line in r.iter_lines(decode_unicode=True):
        if raw_line is None:
            continue

        line = raw_line.strip()

        if line == "":
            if data_lines:
                save_event(event_type, data_lines)

            event_type = None
            data_lines = []
            continue

        if line.startswith("event:"):
            event_type = line[len("event:"):].strip()
        elif line.startswith("data:"):
            data_lines.append(line[len("data:"):].strip())
