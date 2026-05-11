# KSCW
조합론 학생 워크샵(Korean Student Combinatorics Workshop; KSCW)은 조합론을 공부하는 한국 대학원생, 학부생 및 박사후연구원들이 서로 친목을 다지고 연구 분야를 공유하며 공동 연구를 진행할 수 있는 기틀을 마련하는 것을 목적으로 합니다. [홈페이지](https://kscw.combinatorics.kr/)에서 더 많은 정보를 확인할 수 있습니다.

- 2024년: 7월 29일~8월 2일, 공주한옥마을
- 2025년: 8월 20~24일, 더케이 호텔 경주
- 2026년 동계: 2월 2~6일, 신라스테이 여수
- 2026년: 7월 27~31일, 공주한옥마을

## A very short guide
Suppose you are managing the event page for the year of 2000.
1. In `_data/kscw_years.yml`, add an item with `key: 2000` and `label: 2000`. The label is essentially the short Korean name of the event, for example `2000 동계`.
2. Create a folder `2000` with files `index.md` and `schedule.md` inside.
3. Create `slots_2000.yml` inside `_data/schedule` as a copy of `slots_2025.yml`, if every session has a duration that is a multiple of 10 minutes (in 2024, the durations were multiples of 5 minutes.)
4. Create `talks_2000.yml` and `source_overall_2000.yml` inside `_data/schedule`.
5. Run `python _scripts/build_schedule_overall.py 2000` and `python _scripts/build_talk_details.py 2000`.
