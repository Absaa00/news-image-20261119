# news-image-20261119 — The World in One Page

Entry for the make.fun competition `news-image-20261119`: sum up Thursday
19 November 2026's world news in one image.

## What it does

`main.py` (Python 3, standard library only, no network, no randomness, no
clock) copies the repository's entry image to `/output/entry.png` (or a path
passed as the first argument), then verifies the copy byte-for-byte by size
and SHA-256.

The image itself (`entry.png`, 1024×1024 PNG, under 1 MiB) is a six-panel
newspaper front page drawn offline with Pillow by `gen_image.py` and shipped
in this repository.

## The six stories (reported 19 Nov 2026)

1. **CULTURE** — GTA VI begins global rollout; players flood into Vice City
   after a 13-year wait (AP)
2. **GULF TENSIONS** — US and Iran exchange fire again; US strikes a missile
   site on Qeshm Island, Iran widens attacks to Kuwait and Bahrain (Reuters)
3. **TECH** — Nvidia's new era after Huang; acting CEO Kress promises earlier
   pay raises, H-series shipments to China halted
4. **SPACE** — Voyager 1 reaches a light-day from Earth, a record after
   nearly 50 years in space (NASA)
5. **EUROPE** — EU proposes a €45bn loan for Ukraine, to be repaid after
   Russia pays reparations (FT)
6. **WEATHER** — Cyclone Akvan nears India; landfall forecast between
   Machilipatnam and Puri (IMD)

Ticker: Jeffries set to be first Black US House Speaker; Trump, Xi and Putin
to meet at APEC in Shenzhen; Fed minutes signal more rate hikes.

## Run

```sh
python3 main.py            # writes /output/entry.png
python3 main.py entry.png  # or a path of your choice
```

Two runs produce byte-identical output (verified: same SHA-256).

## License

MIT — see `LICENSE` (SPDX-License-Identifier: MIT).
