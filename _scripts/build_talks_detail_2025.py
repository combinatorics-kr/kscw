import yaml
from pathlib import Path

# Paths (assuming this file is in _scripts/ under the repo root)
ROOT = Path(__file__).resolve().parent.parent

SRC_SCHEDULE = ROOT / "_data" / "schedule" / "source_overall_2025.yml"
SRC_TALKS    = ROOT / "_data" / "schedule" / "talks_2025.yml"
DST_DETAILS  = ROOT / "_data" / "schedule" / "talks_detail_2025.yml"


def load_yaml(path: Path):
    if not path.exists():
        raise SystemExit(f"YAML file not found: {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    print(f"ROOT:        {ROOT}")
    print(f"SCHEDULE:    {SRC_SCHEDULE}")
    print(f"TALKS:       {SRC_TALKS}")
    print(f"DESTINATION: {DST_DETAILS}")

    schedule = load_yaml(SRC_SCHEDULE)
    talks = load_yaml(SRC_TALKS)

    # Build index of talks by id
    talk_by_id = {}
    for talk in talks:
        tid = talk.get("id")
        if not tid:
            continue
        if tid in talk_by_id:
            print(f"WARNING: duplicate talk id '{tid}' in talks_2025.yml, overriding previous.")
        talk_by_id[tid] = talk

    details = []

    # Go through all sessions in the schedule, pick ones with an 'id'
    for day in schedule:
        date = day.get("date", "")
        for sess in day.get("sessions", []):
            tid = sess.get("id")
            if not tid:
                continue  # skip sessions without ids (e.g., lunch, breaks, etc.)

            start = sess.get("start")
            end = sess.get("end")

            if not start or not end:
                print(f"WARNING: session with id '{tid}' on date '{date}' missing start/end.")
                continue

            # Format time with an en dash
            time_str = f"{start}–{end}"

            talk = talk_by_id.get(tid)
            if talk is None:
                print(f"WARNING: no talk meta found for id '{tid}' (date {date}, {time_str}). Skipping.")
                continue

            # Build output record
            rec = {
                "id": tid,
                "date": date,
                "time": time_str,
            }

            # Copy all other fields from talk (type, title, speaker, affiliation, abstract, etc.)
            for key, value in talk.items():
                if key == "id":
                    continue
                if key == "abstract" and isinstance(value, str):
                    value = value.rstrip()
                rec[key] = value

            details.append(rec)

    # Ensure destination directory exists
    DST_DETAILS.parent.mkdir(parents=True, exist_ok=True)

    # Write YAML
    with DST_DETAILS.open("w", encoding="utf-8", newline="\n") as f:
        yaml.dump(details, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {len(details)} records to {DST_DETAILS}")


if __name__ == "__main__":
    main()
