# Dice Pack Gallery — Handover & Integration Guide

How the Dice app's **Pack Gallery** (cosmetic + content IAP) works, how this
repo is wired to the app, and how to ship a new pack. Follows the same model
as `TeamDzX/myllm-assets` (see its GALLERY_HANDOVER.md): a public git repo is
the store backend — **push to `main` = live**, no server, no rebuild.

> **Audience:** anyone adding packs to the Dice iOS app. You only touch this
> repo, plus (for paid packs) App Store Connect for the IAP product.

---

## 1. The one-paragraph mental model

A *pack* is *pure JSON*: dice styles are PBR material parameters, table
surfaces are colours + physics, game packs are localized rulebooks. The app
renders everything with its own SceneKit/SwiftUI engine — there are no
binary assets to ship except the 800×400 gallery banner. The app downloads
`packs.json` (the manifest), renders the gallery, and on **Get/Buy**
downloads `packs/<slug>.json` and stores it locally. Paid packs are gated by
StoreKit 2 with the product id named in the manifest; free packs install
directly.

---

## 2. Git wiring

- **Repo:** `github.com/TeamDzX/dice-assets` (public). ⚠️ Not yet pushed —
  create the repo and `git push origin main` to go live.
- **Hot-linked raw URLs:**
  `https://raw.githubusercontent.com/TeamDzX/dice-assets/main/<path>`
- **CDN cache** ~5 minutes, same as myllm-assets.
- **Publishing an update to an existing pack:** bump its `version` int in
  BOTH `packs.json` and the payload (`build_payloads.py` keeps them in sync).
  The app shows an **Update** button only when the manifest version is
  higher than the installed payload's.
- **Dev override:** the app reads UserDefaults key `galleryBaseURL` — point
  it at a local `python3 -m http.server` serving this folder to test packs
  before pushing.

## 3. Repository layout

```
packs.json                  ← THE manifest (generated — do not hand-edit)
packs/<slug>.json           ← pack payloads (generated)
banners/<slug>.jpg          ← 800×400 gallery banner
langs/<code>.json           ← ALL human-readable strings, 9 languages
build_payloads.py           ← generator: langs + spec tables → packs.json + packs/
make_placeholder_banners.py ← temporary gradient banners (see §6)
```

Languages: `en ja zh-Hans ar he fr de es pt` — the same nine the app ships.
`build_payloads.py` **asserts** every string exists in every language and
that rule counts match, so a bad language file fails loudly.

## 4. Manifest schema (per pack)

| field | notes |
|---|---|
| `id` | slug, must match payload/banner filenames. Never change it. |
| `type` | `dice` \| `table` \| `games` — drives the gallery section and payload shape |
| `name`/`tagline`/`description` | localized dicts `{code: string}` — from `langs/` |
| `emoji`, `iconSymbol`, `iconColor` | tile art (emoji shown in rows + banner fallback) |
| `version` | int — bump to prompt installed users to update |
| `featured` | surfaces in the horizontal Featured rail; use sparingly |
| `productId` | `null` = free; else an IAP id. Structure (2026-07-05, see IAP_METADATA.md): `…dicestyles` £1.99 covers all dice packs, `…tables` £0.99 covers all table packs, each game pack has its own id at £1.99, and `…allaccess` £4.99 (never on a pack — app-side special case) unlocks everything. |
| `banner` / `payload` | raw URLs into this repo |
| `sizeKB`, `tags` | cosmetic metadata |

## 5. Payload shapes

- **dice:** `styles[]` — `id`, localized `name`, `body`/`pip` hex colours,
  `roughness`, `metalness` (0–1), optional `emission` hex (neon glow).
- **table:** `surfaces[]` — `background` (UI bg), `floor` colour,
  `roughness`/`metalness`/`normalIntensity`/`reflectivity` (render),
  `friction`/`restitution` (physics feel), `accent`.
- **games:** `games[]` — `id`, SF Symbol `icon`, `diceNeeded`, `players`,
  localized `name`/`summary`, `rules` as an array of localized dicts.

In the app, unlocked dice styles/surfaces appear automatically in Settings
(namespaced ids `pack/<packId>/<styleId>`), and pack games are appended to
the Game Library, all resolved to the user's selected app language.

## 6. Banners

- **Size:** 800×400 JPG at `banners/<slug>.jpg`. **House style:** clean,
  premium, soft glowing shapes on a themed gradient — **no text, no people**
  (FLUX garbles text).
- Current files are real FLUX renders (regenerated 2026-07-05/06 once the
  ComfyUI server came back). To generate or replace a banner:
  ```
  python3 ~/.claude/scripts/imagegen/comfy_gen.py banners/<slug>.jpg \
    "PROMPT" SEED --size 1216x608 --max 800
  ```
  Suggested prompts (append "no text, no letters, no words, no people" to each):
  - sakura-set: premium product photo of three pastel dice (pink, lavender, matcha green) on dark silk, floating cherry blossom petals, soft studio glow
  - metal-works: macro photo of four metallic dice (silver, gunmetal, rose gold, copper) on brushed steel, dramatic rim lighting
  - gemstones: four gem-carved dice (jade, obsidian, sapphire, ruby) on black velvet, jewellery product lighting, sparkling facets
  - neon-glow: four glowing translucent dice (hot pink, cyan, lime, violet) on wet black acrylic, neon reflections, dark room
  - tatami-room: dice cup and two ivory dice on woven tatami mat, warm paper-lantern light, japanese minimalist interior
  - casino-night: dice on deep red casino baize beside a polished walnut rail, moody low-key lighting, bokeh chips
  - party-night: red izakaya lantern glow over a ceramic bowl with three dice on a wooden counter, warm night atmosphere
  - tavern-classics: worn oak pub table with leather dice cup, brass details, candlelight, rustic cozy atmosphere
  - The app falls back to an emoji-on-gradient card whenever a banner 404s,
    so shipping before the art is ready is safe.
- The banner **URL never changes**, so replacing the JPG needs no version
  bump (CDN cache ≈5 min).

## 7. Adding a new pack — checklist

1. Add the spec entry to the right table in `build_payloads.py`
   (materials/physics/icons/productId/tags).
2. Add `name`/`tagline`/`description` (+ style names / game content) to
   **all nine** `langs/<code>.json` files.
3. `python3 build_payloads.py` — regenerates `packs.json` + `packs/`.
4. Banner: generate `banners/<slug>.jpg` (or ship without; fallback covers it).
5. Paid pack? Dice/table packs: stamp `DICE_STYLES_ID` / `TABLES_ID` in
   `build_payloads.py` — covered by the existing section IAP, no ASC work.
   Game packs: new product id + new ASC non-consumable at £1.99 (template in
   IAP_METADATA.md); the Everything bundle covers it automatically. Until a
   product is live in ASC, the app shows **Coming Soon** — safe to
   pre-publish here.
6. Test locally: serve this folder over HTTP, set `galleryBaseURL`.
7. Commit named files, push `main`, verify raw URL returns 200.

## 8. Gotchas

- **`packs.json` is generated** — edit `build_payloads.py` + `langs/`, not
  the output files.
- **Never rename a pack `id` or style `id`** — user selections and installed
  payload files are keyed on them.
- **Bump `version`** or installed users never see content updates.
- Free packs (`productId: null`) are the pipeline smoke test — keep at least
  one per section so reviewers and new users always have something to Get.
- The app keeps working fully offline from its cached manifest + installed
  payloads; the gallery just can't fetch new packs.
