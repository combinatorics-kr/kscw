import sys
import yaml
from pathlib import Path

# repo root: one level up from _scripts/
ROOT = Path(__file__).resolve().parent.parent


def load_yaml(path: Path):
    if not path.exists():
        raise SystemExit(f"YAML file not found: {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_for_year(year: str):
    src_schedule_path = ROOT / "_data" / "schedule" / f"source_overall_{year}.yml"
    src_talks_path    = ROOT / "_data" / "schedule" / f"talks_{year}.yml"
    dst_details_path  = ROOT / "_data" / "schedule" / f"talk_details_{year}.yml"

    print(f"ROOT:              {ROOT}")
    print(f"SRC_SCHEDULE:      {src_schedule_path}")
    print(f"SRC_TALKS:         {src_talks_path}")
    print(f"DST_TALK_DETAILS:  {dst_details_path}")

    schedule = load_yaml(src_schedule_path)
    talks = load_yaml(src_talks_path)

    # Build index of talks by id
    talk_by_id = {}
    for talk in talks or []:
        tid = talk.get("id")
        if not tid:
            continue
        if tid in talk_by_id:
            print(f"WARNING: duplicate talk id '{tid}' in talks_{year}.yml, overriding previous.")
        talk_by_id[tid] = talk

    details = []

    # Go through all sessions in the schedule, pick ones with an 'id'
    for day in schedule or []:
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

            time_str = f"{start}–{end}"

            talk = talk_by_id.get(tid)
            if talk is None:
                print(f"WARNING: no talk meta found for id '{tid}' (date {date}, {time_str}). Skipping.")
                continue

            rec = {
                "id": tid,
                "date": date,
                "time": time_str,
            }

            # Copy other fields from talk (type, title, speaker, affiliation, abstract, etc.)
            for key, value in talk.items():
                if key == "id":
                    continue

                # Clean trailing whitespace on abstract
                if key == "abstract" and isinstance(value, str):
                    value = value.rstrip()

                rec[key] = value

            details.append(rec)

    dst_details_path.parent.mkdir(parents=True, exist_ok=True)

    with dst_details_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.dump(details, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {len(details)} records to {dst_details_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        year_arg = sys.argv[1]
        build_for_year(year_arg)
    else:
        print("Please provide a year key as an argument, e.g.:")
        print("  python _scripts/build_talk_details.py 2025")
        print("  python _scripts/build_talk_details.py 2026w")
