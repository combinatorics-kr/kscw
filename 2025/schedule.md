---
title: 2025년 조합론 학생 워크샵 
description: 더케이 호텔 경주, 2025년 8월 20~24일
---

<!-- Simple navigation between years -->
<nav class="page-nav">
  <!-- <strong>탐색:</strong> -->
  <a href="{{ site.baseurl }}/">Home</a> ·
  <a href="{{ site.baseurl }}/2024/">2024</a> ·
  <span style="font-weight:bold;">2025</span> ·
  <a href="{{ site.baseurl }}/2026w/">2026년 동계</a>
</nav>

<nav class="page-nav">
  <span>(행사)</span>
  <a href="{{ site.baseurl }}/2025/">Home</a> ·
  <span style="font-weight:bold;">일정</span>
</nav>

# 일정

{% include schedule_overall.html
   data = site.data.schedule.schedule_overall_2025
   slots = site.data.schedule.slots_2025 %}

## 강연 세부 정보

{% include talks_detail.html
   data = site.data.schedule.talks_detail_2025 %}