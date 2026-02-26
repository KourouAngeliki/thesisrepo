import requests

DITTO_BASE = "http://localhost:8080/"
USERNAME = "ditto"
PASSWORD = "ditto"

url = f"{DITTO_BASE}/api/2/things"

headers = {
    "Accept": "text/event-stream",
}

def mpe(data_lines):
    data = "\n".join(data_lines)
    print("EVENT:", event_type or "(no type)")
    print("DATA:", data)
    print("-" * 60)


with requests.get(url, headers=headers, auth=(USERNAME, PASSWORD), stream=True) as r:
    r.raise_for_status()  # αν είναι 401/403 θα πετάξει exception με το status

    event_type = None
    data_lines = []

    for raw_line in r.iter_lines(decode_unicode=True):
        if raw_line is None:
            continue

        line = raw_line.strip()

        # SSE: κενή γραμμή σημαίνει "τέλος event"
        if line == "":
            if data_lines:
                mpe(data_lines=data_lines)
                
            event_type = None
            data_lines = []
            continue

        # SSE fields
        if line.startswith("event:"):
            event_type = line[len("event:"):].strip()
        elif line.startswith("data:"):
            data_lines.append(line[len("data:"):].strip())