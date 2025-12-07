---
title: 조합론 학생 워크샵
description: Korean Student Combinatorics Workshop
hero_kicker: Korean Student Combinatorics Workshop
hero_title: 조합론 학생 워크샵
---

<div class="page-hero hero-{{ page.hero_year_key | default: 'default' }}">
  {% if page.hero_kicker %}
    <p class="hero-kicker">{{ page.hero_kicker }}</p>
  {% endif %}

  {% if page.hero_title %}
    <h1 class="hero-title">{{ page.hero_title }}</h1>
  {% endif %}
</div>

<nav class="breadcrumbs breadcrumbs-years">
  <ol>
    <li class="current">Home</li>

    {%- for y in site.data.kscw_years -%}
      {% if y.key == page.hero_year_key %}
        <li class="current">{{ y.label }}</li>
      {% else %}
        <li><a href="{{ y.key | relative_url }}">{{ y.label }}</a></li>
      {% endif %}
    {%- endfor -%}
  </ol>
</nav>


**조합론 학생 워크샵(Korean Student Combinatorics Workshop; KSCW)**은 조합론을 공부하는 한국 대학원생, 학부생 및 박사후연구원들이 서로 친목을 다지고 연구 분야를 공유하며 공동 연구를 진행할 수 있는 기틀을 마련하는 것을 목적으로 합니다.

- [2024년](2024/): 7월 29일~8월 2일, 공주한옥마을
- [2025년](2025/): 8월 20~24일, 더케이 호텔 경주
- [2026년 동계](2026w/): 2월 2~6일, 신라스테이 여수

