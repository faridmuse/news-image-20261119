# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/faridmuse/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/faridmuse/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the [make.fun bounty "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119).

A one-page newspaper front page for Thursday 19 November 2026: the 35 top
stories of the day, drawn with PIL into a single 1024×1024 PNG.

## What is on the page

- Masthead: **Thursday 19 November 2026**, with the day's coverage line.
- Three original drawings (no photographs): the Vice City skyline at sunset,
  a night sea in the Gulf, and Cyclone Akvan spiralling over the Bay of Bengal.
- Stories 1–10 with a short summary each: GTA VI's worldwide launch, Iran's
  widened attacks on Kuwait and Bahrain, the Trump–Xi–Putin meeting in
  Shenzhen, Jeffries nominated Speaker, Cyclone Akvan, the Fed minutes,
  Peltola's Alaska win, Pew's faith projection, Voyager 1 one light-day out,
  and Nvidia halting H200 shipments to China.
- Stories 11–35 as headlines, from the India–Japan 2+2 talks to the GTA VI
  verdict piece.
- A dotted world map with numbered dots for stories 1–10, a "By the numbers"
  box, and a footer listing the sources.

Every item carries its date, place, and source outlet. Sources: Reuters, AP,
BBC, CNN, FT, IMD, NASA, Pew, The Hindu, PTI, and others listed in
`sources.md`.

## Build

```sh
python3 draw-20261119.py   # renders entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # copies it to out/
```

`draw-20261119.py` needs Pillow (`pip install pillow`). The artwork is drawn
programmatically with PIL primitives — no external images are used.
