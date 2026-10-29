# falkOSS – brand kit

**falkOSS** is short for **Falcon Lake Open Source Software** – the non-profit behind free software from Falkensee
(Brandenburg, next to Berlin).

> **FA**lcon **L**a**K**e → **FALK** → **FALK**ensee · + **OSS** = **falkOSS**
> (and *Falcon Lake Open Source Software* spells **FLOSS**)

This repository is the one source of the falkOSS and falkOSS labs brand. Everything here is generated: edit
`generate.py`, then run `python3 generate.py` (needs `rsvg-convert` from Homebrew `librsvg`). It writes `svg/`, `png/`
and the head assets of the two websites, `web/` and `web-labs/`.

## Marks

The look is a terminal, not a postcard: near-black, one amber like an amber-phosphor monitor, straight edges,
monospace type. No gradients, no soft curves, no stock-photo nature.

- **Mark** – a falcon seen from below, all straight edges (wings bent at the wrist, swept back to a point, faceted body,
  squared tail), over the lake drawn as a flat waveform and a line. Amber falcon, steel lake.
- **Wordmark** – angular, chamfered strokes like a terminal font, no font file needed: `falk` in light, `OSS` in
  amber. Always written **falkOSS** in text (lowercase `falk`, uppercase `OSS`); in domains and handles `falkoss`.
- **Lockup** – mark left, wordmark right.
- **Icon** – the mark on near-black; **small icon** (16–48 px) with the lake as one heavy line.
- **Social preview** – a prompt: `$ whoami` → falkOSS, on a faint grid, with a block cursor.

## Where to use what

| Use | File |
|---|---|
| GitHub org avatar | `png/social/github-avatar-500.png` |
| GitHub social preview, link previews | `png/social/falkoss-social-1280x640.png` |
| Website head (falkoss.org) | `web/` – favicon.svg (follows light/dark), favicon.ico, apple-touch-icon.png, icon-192/512.png, social.png, site.webmanifest, the lockup and mark; `web/projects/falkoss-labs.png` for the project list |
| Headers, documents on dark / light | `svg/falkoss-lockup-on-dark.svg`, `-on-light.svg` (PNG: `png/lockup/`) |
| Wordmark alone | `svg/falkoss-wordmark-on-dark.svg`, `-on-light.svg` |
| Mark alone (transparent) | `svg/falkoss-mark-on-dark.svg`, `-on-light.svg`; one colour: `-black.svg`, `-white.svg` |
| App-like icon | `png/icon/` (rounded), `png/icon-square/` (edge to edge), `png/icon-small/` (16–48 px) |
| Print, stickers | the SVGs (vector); one-colour marks for single-colour print |

## falkOSS labs

**falkoss-labs** is the GitHub organisation for small projects – plugins, forks, tools, experiments – that don't need
an organisation of their own. It is not a separate brand: same falcon, same colours, plus the word **labs** in steel.

| Use | File |
|---|---|
| GitHub org avatar | `png/social/github-avatar-labs-500.png` |
| Headers on dark / light | `svg/falkoss-labs-lockup-on-dark.svg`, `-on-light.svg` (PNG: `png/labs/`) |
| Icon | `svg/falkoss-labs-icon.svg` (rounded), `-icon-square.svg` (PNG: `png/labs/`) |
| Website head (labs.falkoss.org) | `web-labs/` – the same favicon, the labs icons, lockup, mark, social preview and web manifest |

In text: **falkOSS labs** (lowercase `labs`); in handles `falkoss-labs`.

## Colours

| Name | Hex | Use |
|---|---|---|
| Night | `#0B0D10` | backgrounds |
| Amber | `#FFB000` | the falcon, `OSS`, the one accent (links, cursor, highlights) |
| Steel | `#5B7083` | the lake, rules, secondary marks |
| Mist | `#E6EDF3` | text on dark |
| Reed | `#7D8590` | muted text, comments |
| Ink | `#0B0D10` | text on light |
| Amber (on light) | `#B87800` | falcon and `OSS` on light backgrounds |
| Steel (on light) | `#4A5D70` | lake on light backgrounds |

One accent only: amber. Steel and grey do the rest.

## Type

Monospace for headings, labels, navigation and code (`ui-monospace, "SF Mono", Menlo, Consolas, …`), the system sans
stack for longer text. Nothing is loaded from other servers (no Google Fonts: privacy). The wordmark is drawn, so it
looks the same everywhere.

## Don'ts

- Don't recolour the falcon or add more accent colours; don't put the bright amber on a light background (use the
  on-light variant).
- No glow, neon, matrix rain or gradients – the restraint is the point.
- Don't stretch, rotate or add effects; keep clear space around the mark of at least the width of the falcon's head.
- Don't write *Falkoss*, *FalkOSS* or *FALKOSS* in running text – it is **falkOSS**.

## Relation to the projects

falkOSS carries projects that keep their own identity – e.g. **omaflake** with its own brand (`omaflake/brand`). Use
“a falkOSS project” plus the small mark in project footers, not the falkOSS colours in a project's own design.

## Where it is used

The other repositories carry copies of what they show and are updated by copying, never edited there:

| Repository | Copies |
|---|---|
| `falkoss/website` | `web/*` → `assets/` (the project icons in `assets/projects/` come from each project's brand) |
| `falkoss-labs/website` | `web-labs/*` → `assets/` |
| `falkoss/.github` | `svg/falkoss-lockup-on-dark.svg`, `-on-light.svg` → `profile/assets/` |
| `falkoss-labs/.github` | `svg/falkoss-labs-lockup-on-dark.svg`, `-on-light.svg` → `profile/assets/` |
| `falkoss/starterpack` | nothing – projects have their own brand; “a falkOSS project” stays text |

## Licences and rights

| Files | Licence |
|---|---|
| `generate.py`, this README | [MIT](LICENSES/MIT.txt) |
| the artwork: `svg/`, `png/`, `web/`, `web-labs/` | [CC BY-ND 4.0](LICENSES/CC-BY-ND-4.0.txt) |

The artwork may be copied and passed on as it is, naming falkOSS; changed versions may not be passed on. The licence
covers the artwork's copyright, not the name: the name falkOSS and its brand belong to falkOSS – Falcon Lake Open Source
Software gUG (haftungsbeschränkt) i. G. They may be used to refer to falkOSS, not for other products or in a way that
suggests endorsement. **OPEN**: trademark registration (word mark “falkoss”, classes 9 and 42), and a review of these
terms by someone who knows the law.
