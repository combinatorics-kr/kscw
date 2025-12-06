import sys
import yaml
from pathlib import Path

# repo root: one level up from _scripts/
ROOT = Path(__file__).resolve().parent.parent

# CONFIG: grid start hour per year-key
YEAR_BASE_TIME = {
    "2025": 9,    # grid starts at 09:00
    "2026w": 10,  # grid starts at 10:00
}

STEP_MIN = 10  # 10-minute slots

# This will be set in build_for_year(year)
BASE_TIME = (0, 0)


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def slot_index(hhmm: str) -> int:
    """Convert HH:MM to a 1-based slot index using global BASE_TIME."""
    base_minutes = BASE_TIME[0] * 60 + BASE_TIME[1]
    t = to_minutes(hhmm)
    diff = t - base_minutes
    if diff < 0 or diff % STEP_MIN != 0:
        raise ValueError(
            f"time {hhmm} not aligned to {STEP_MIN}-min grid starting at {BASE_TIME}"
        )
    return diff // STEP_MIN + 1  # 1-based index


def rowspan(start: str, end: str) -> int:
    s = to_minutes(start)
    e = to_minutes(end)
    diff = e - s
    if diff <= 0 or diff % STEP_MIN != 0:
        raise ValueError(f"invalid duration {start}–{end} for step {STEP_MIN}")
    return diff // STEP_MIN


def infer_type(title: str) -> str:
    """Infer event type from its title (lowercased)."""
    t = title.lower()

    if "registration" in t:
        return "registration"

    if "remark" in t or "opening" in t or "introduction" in t:
        return "plenary"

    if "invited" in t:
        return "invited-talk"

    if "special session" in t or "special talk" in t:
        return "special-session"

    if "contributed" in t:
        return "contributed-talk"

    if "coffee" in t:
        return "coffee"

    if "break" in t:
        return "break"

    if "lunch" in t or "dinner" in t or "banquet" in t:
        return "meal"

    if "open problem" in t or "problem session" in t or "group discussion" in t:
        return "problem"

    if "excursion" in t or "social event" in t:
        return "excursion"

    return "default"


def load_yaml(path: Path):
    if not path.exists():
        raise SystemExit(f"Source YAML not found: {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_for_year(year: str) -> None:
    global BASE_TIME

    if year not in YEAR_BASE_TIME:
        raise SystemExit(
            f"Unknown year key '{year}'. "
            f"Known keys: {', '.join(YEAR_BASE_TIME.keys())}"
        )

    # Set base time for this year
    BASE_TIME = (YEAR_BASE_TIME[year], 0)

    src_schedule_source_path = ROOT / "_data" / "schedule" / f"source_overall_{year}.yml"
    src_talks_path = ROOT / "_data" / "schedule" / f"talks_{year}.yml"
    dst_path = ROOT / "_data" / "schedule" / f"schedule_overall_{year}.yml"

    print(f"ROOT: {ROOT}")
    print(f"SRC_SCHEDULE_SOURCE:  {src_schedule_source_path}")
    print(f"SRC_TALKS:           {src_talks_path}")
    print(f"DST:                 {dst_path}")
    print(f"BASE_TIME: {BASE_TIME[0]:02d}:00  (STEP_MIN={STEP_MIN})")

    # Load schedule source and talks metadata
    data = load_yaml(src_schedule_source_path)
    talks_data = load_yaml(src_talks_path)

    # Index talks by id
    talk_by_id = {}
    for talk in talks_data or []:
        tid = talk.get("id")
        if not tid:
            continue
        if tid in talk_by_id:
            print(f"WARNING: duplicate talk id '{tid}' in talks_{year}.yml; overriding previous.")
        talk_by_id[tid] = talk

    out_days = []
    for day in data:
        out_sessions = []
        for sess in day.get("sessions", []):
            start = sess["start"]
            end = sess["end"]
            title = sess["title"]
            sess_id = sess.get("id")

            # Base type from session title / explicit type
            etype = sess.get("type") or infer_type(title)

            speaker = None # sess.get("speaker")
            affiliation = None
            homepage = None

            # If this session is linked to a talk, use talk metadata
            if sess_id:
                talk = talk_by_id.get(sess_id)
                if talk is None:
                    print(
                        f"WARNING: no talk meta found for id '{sess_id}' "
                        f"(date {day.get('date')}, {start}–{end})."
                    )
                else:
                    # If talk has a specific type, override
                    if talk.get("type"):
                        etype = talk["type"]

                    # Prefer explicit speaker in talk meta
                    if talk.get("speaker"):
                        speaker = talk["speaker"]

                    affiliation = talk.get("affiliation")
                    homepage = talk.get("homepage")

            s_idx = slot_index(start)
            rs = rowspan(start, end)

            out = {
                "slot": s_idx,
                "rowspan": rs,
                "time": f"{start}–{end}",
                "title": title,
                "type": etype,
            }

            # Keep id for linking from schedule → talk details
            if sess_id:
                out["id"] = sess_id

            if speaker:
                out["speaker"] = speaker
            if affiliation:
                out["affiliation"] = affiliation
            if homepage:
                out["homepage"] = homepage

            out_sessions.append(out)

        out_days.append(
            {
                "date": day["date"],
                "sessions": out_sessions,
            }
        )

    dst_path.parent.mkdir(parents=True, exist_ok=True)
    with dst_path.open("w", encoding="utf-8", newline="\n") as f:
        yaml.dump(out_days, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {dst_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        year_arg = sys.argv[1]
        build_for_year(year_arg)
    else:
        print("Please provide a year key as an argument, e.g.:")
        print("  python _scripts/build_schedule_overall.py 2025")
        print("  python _scripts/build_schedule_overall.py 2026w")
