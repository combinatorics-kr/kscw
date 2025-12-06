import yaml
from pathlib import Path

# CONFIG
BASE_TIME = (10, 0)      # grid starts at 10:00
STEP_MIN = 10           # 10-minute slots

# repo root: one level up from _scripts/
ROOT = Path(__file__).resolve().parent.parent

SRC = ROOT / "_data" / "schedule" / "source_overall_2026w.yml"
DST = ROOT / "_data" / "schedule" / "schedule_overall_2026w.yml"


def to_minutes(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def slot_index(hhmm: str) -> int:
    base_minutes = BASE_TIME[0] * 60 + BASE_TIME[1]
    t = to_minutes(hhmm)
    diff = t - base_minutes
    if diff < 0 or diff % STEP_MIN != 0:
        raise ValueError(f"time {hhmm} not aligned to {STEP_MIN}-min grid starting at {BASE_TIME}")
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

    if "remark" in t or "opening" in t:
        return "plenary"

    if "invited" in t:
        return "invited"

    if "special session" in t:
        return "special"

    if "contributed" in t:
        return "contributed"

    if "coffee" in t:
        return "coffee"

    if "break" in t:
        return "break"

    if "lunch" in t or "dinner" in t or "banquet" in t:
        return "meal"

    if "open problem" in t or "problem session" in t:
        return "problem"

    if "excursion" in t or "social event" in t:
        return "excursion"

    return "default"


def main():
    print(f"ROOT: {ROOT}")
    print(f"SRC:  {SRC}")
    print(f"DST:  {DST}")

    if not SRC.exists():
        raise SystemExit(f"Source YAML not found: {SRC}")

    with SRC.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    out_days = []
    for day in data:
        out_sessions = []
        for sess in day["sessions"]:
            start = sess["start"]
            end = sess["end"]
            title = sess["title"]
            speaker = sess.get("speaker")

            s_idx = slot_index(start)
            rs = rowspan(start, end)
            etype = infer_type(title)

            out = {
                "slot": s_idx,
                "rowspan": rs,
                "time": f"{start}–{end}",
                "title": title,
                "type": etype,
            }
            if speaker:
                out["speaker"] = speaker

            out_sessions.append(out)

        out_days.append({
            "date": day["date"],
            "sessions": out_sessions,
        })

    DST.parent.mkdir(parents=True, exist_ok=True)
    with DST.open("w", encoding="utf-8", newline="\n") as f:
        yaml.dump(out_days, f, sort_keys=False, allow_unicode=True)

    print(f"Wrote {DST}")


if __name__ == "__main__":
    main()
