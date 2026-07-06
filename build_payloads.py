#!/usr/bin/env python3
"""Generate packs/<slug>.json payloads and packs.json manifest for the Dice Pack Gallery.

Pattern follows myllm-assets/build_language.py: a static spec table here supplies
the variable bits (materials, physics, icons, prices); langs/<code>.json supply
every human-readable string. Run after updating either:

    python3 build_payloads.py

Asserts data integrity (every pack/style/game key present in every language)
so a bad language file fails loudly instead of shipping broken.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = "https://raw.githubusercontent.com/TeamDzX/dice-assets/main"
LANG_CODES = ["en", "ja", "zh-Hans", "ar", "he", "fr", "de", "es", "pt"]
UPDATED = "2026-07-06"

# IAP structure (decided 2026-07-05): section bundles + per-game-pack products,
# plus an Everything bundle handled app-side (it unlocks every pack regardless
# of the pack's own product id — see PackStore.allAccessProductId).
#   dice styles (all dice packs, incl. future)  £1.99
#   table surfaces (all table packs)            £0.99
#   each game pack                              £1.99
#   everything bundle                           £4.99
DICE_STYLES_ID = "TeamDZX.dice.pack.dicestyles"
TABLES_ID = "TeamDZX.dice.pack.tables"
PARTY_NIGHT_ID = "TeamDZX.dice.pack.partynight"
TAVERN_ID = "TeamDZX.dice.pack.tavernclassics"

# ---------------------------------------------------------------- spec tables

DICE_PACKS = {
    "sakura-set": {
        "emoji": "🌸", "iconSymbol": "leaf.fill", "iconColor": "pink",
        "featured": True, "productId": None, "tags": ["japan", "seasonal", "free"],
        "styles": [
            ("sakura",      "Sakura",      "#F6CCD8", "#A63D5C", 0.30, 0.0, None),
            ("wisteria",    "Wisteria",    "#C5B3E6", "#4B3A78", 0.30, 0.0, None),
            ("matcha",      "Matcha",      "#A8C686", "#3D5226", 0.35, 0.0, None),
        ],
    },
    "metal-works": {
        "emoji": "⚙️", "iconSymbol": "gearshape.2.fill", "iconColor": "teal",
        "featured": False, "productId": DICE_STYLES_ID,
        "tags": ["metal", "premium"],
        "styles": [
            ("silver",      "Silver",      "#D9DBDE", "#2A2A2E", 0.25, 0.90, None),
            ("gunmetal",    "Gunmetal",    "#4A4E57", "#E8E8EC", 0.35, 0.85, None),
            ("rose-gold",   "Rose Gold",   "#E3A98F", "#5C2E22", 0.30, 0.80, None),
            ("copper",      "Copper",      "#B4653F", "#F2E7DC", 0.40, 0.85, None),
        ],
    },
    "gemstones": {
        "emoji": "💎", "iconSymbol": "diamond.fill", "iconColor": "indigo",
        "featured": False, "productId": DICE_STYLES_ID,
        "tags": ["gems", "premium"],
        "styles": [
            ("jade",        "Jade",        "#4FA173", "#F5F2E8", 0.15, 0.05, None),
            ("obsidian",    "Obsidian",    "#17171C", "#E0DEE6", 0.05, 0.10, None),
            ("sapphire",    "Sapphire",    "#1F3C88", "#DCE4F7", 0.12, 0.05, None),
            ("ruby",        "Ruby",        "#8C1F35", "#F7DCDF", 0.12, 0.05, None),
        ],
    },
    "neon-glow": {
        "emoji": "🌈", "iconSymbol": "bolt.fill", "iconColor": "purple",
        "featured": False, "productId": DICE_STYLES_ID,
        "tags": ["neon", "glow", "premium"],
        "styles": [
            ("neon-pink",   "Neon Pink",   "#1A0A14", "#FFD9EC", 0.40, 0.0, "#FF2E93"),
            ("cyber-cyan",  "Cyber Cyan",  "#061418", "#D7FCFF", 0.40, 0.0, "#22D3EE"),
            ("laser-lime",  "Laser Lime",  "#0D1406", "#F2FFE0", 0.40, 0.0, "#A3E635"),
            ("ultraviolet", "Ultraviolet", "#12081F", "#EFE4FF", 0.40, 0.0, "#8B5CF6"),
        ],
    },
    "kyoto-nights": {
        "emoji": "🏮", "iconSymbol": "moon.stars.fill", "iconColor": "indigo",
        "featured": False, "productId": DICE_STYLES_ID,
        "tags": ["japan", "premium"],
        "styles": [
            ("indigo",     "Indigo",     "#1B2C58", "#EFE9DC", 0.35, 0.0, None),
            ("vermilion",  "Vermilion",  "#C43A28", "#FFF6EA", 0.30, 0.0, None),
            ("gold-leaf",  "Gold Leaf",  "#C9A227", "#231C0A", 0.30, 0.90, None),
            ("sumi",       "Sumi",       "#26262B", "#E8E4DA", 0.50, 0.0, None),
        ],
    },
    "deep-sea": {
        "emoji": "🌊", "iconSymbol": "water.waves", "iconColor": "cyan",
        "featured": False, "productId": DICE_STYLES_ID,
        "tags": ["ocean", "premium"],
        "styles": [
            ("pearl",     "Pearl",     "#EDE8E0", "#4A4238", 0.15, 0.10, None),
            ("coral",     "Coral",     "#E86A5E", "#FFF5ED", 0.30, 0.0, None),
            ("turquoise", "Turquoise", "#2AB5A5", "#063B36", 0.20, 0.0, None),
            ("abyss",     "Abyss",     "#04121F", "#BFE9FF", 0.35, 0.0, "#2E9BFF"),
        ],
    },
}

TABLE_PACKS = {
    "tatami-room": {
        "emoji": "🎋", "iconSymbol": "square.grid.3x3.square", "iconColor": "green",
        "featured": True, "productId": None, "tags": ["japan", "free"],
        # id, name-key, bg, floor, rough, metal, normal, refl, friction, restitution, accent
        "surfaces": [
            ("tatami", "Tatami", "#3E3F2A", "#8F8F5E", 0.92, 0.0, 0.35, 0.03, 1.0, 0.08, "#3E3F2A"),
        ],
    },
    "casino-night": {
        "emoji": "🎰", "iconSymbol": "suit.club.fill", "iconColor": "red",
        "featured": False, "productId": TABLES_ID,
        "tags": ["casino", "premium"],
        "surfaces": [
            ("red-baize",  "Red Baize",  "#3A0D12", "#7A1622", 0.95, 0.0, 0.15, 0.05, 1.0, 0.12, "#3A0D12"),
            ("navy-baize", "Navy Baize", "#0C1630", "#1B2C5C", 0.95, 0.0, 0.15, 0.05, 1.0, 0.12, "#0C1630"),
            ("walnut",     "Walnut",     "#241209", "#5C3A22", 0.50, 0.0, 0.40, 0.08, 0.55, 0.28, "#3A2113"),
        ],
    },
    "zen-garden": {
        "emoji": "🪨", "iconSymbol": "circle.hexagongrid.circle", "iconColor": "mint",
        "featured": False, "productId": TABLES_ID,
        "tags": ["japan", "zen", "premium"],
        "surfaces": [
            ("sand-garden", "Sand Garden", "#4A4436", "#CBBFA3", 0.95, 0.0, 0.50, 0.02, 1.0, 0.06, "#6B6250"),
            ("slate",       "Slate",       "#1E2226", "#3E464D", 0.60, 0.0, 0.30, 0.06, 0.70, 0.20, "#2E363D"),
            ("moss",        "Moss",        "#26301C", "#55703B", 0.95, 0.0, 0.45, 0.02, 1.0, 0.05, "#3A4A28"),
        ],
    },
}

GAME_PACKS = {
    "party-night": {
        "emoji": "🏮", "iconSymbol": "lanternfestival.fill" if False else "flame.fill",
        "iconColor": "orange", "featured": False,
        "productId": PARTY_NIGHT_ID, "tags": ["party", "japan", "premium"],
        "version": 2,  # v2 (2026-07-06): +Bunco, +Sevens Out — free update for owners
        # id, icon, diceNeeded, players
        "games": [
            ("chinchirorin",    "sparkles",                3, "2+"),
            ("cee-lo",          "flame.fill",              3, "2+"),
            ("drop-dead",       "heart.slash.fill",        5, "2+"),
            ("bunco",           "person.3.fill",           3, "4+"),
            ("sevens-out",      "7.square.fill",           2, "2+"),
        ],
    },
    "tavern-classics": {
        "emoji": "🍺", "iconSymbol": "mug.fill", "iconColor": "yellow",
        "featured": False, "productId": TAVERN_ID,
        "tags": ["classic", "premium"],
        "version": 2,  # v2 (2026-07-06): +Chicago, +Help Your Neighbor — free update for owners
        "games": [
            ("shut-the-box",    "square.grid.3x3.fill",    2, "2+"),
            ("threes",          "3.circle.fill",           5, "1+"),
            ("going-to-boston", "arrow.right.circle.fill", 3, "2+"),
            ("chicago",         "building.2.fill",         2, "2+"),
            ("help-your-neighbor", "person.2.wave.2.fill", 3, "2+"),
        ],
    },
}

# ---------------------------------------------------------------- load langs

langs = {}
for code in LANG_CODES:
    path = os.path.join(ROOT, "langs", f"{code}.json")
    with open(path) as f:
        langs[code] = json.load(f)

def localized(section, *keys):
    """Build a {code: value} dict for a nested key path, asserting completeness."""
    out = {}
    for code in LANG_CODES:
        node = langs[code][section]
        for k in keys:
            assert k in node, f"lang {code}: missing {section}/{'/'.join(keys)}"
            node = node[k]
        assert isinstance(node, str) and node.strip(), \
            f"lang {code}: empty value at {section}/{'/'.join(keys)}"
        out[code] = node
    return out

def localized_rules(game_id):
    n = len(langs["en"]["games"][game_id]["rules"])
    for code in LANG_CODES:
        got = len(langs[code]["games"][game_id]["rules"])
        assert got == n, f"lang {code}: {game_id} has {got} rules, expected {n}"
    return [
        {code: langs[code]["games"][game_id]["rules"][i] for code in LANG_CODES}
        for i in range(n)
    ]

# ---------------------------------------------------------------- payloads

os.makedirs(os.path.join(ROOT, "packs"), exist_ok=True)
manifest_packs = []

def emit(slug, ptype, spec, payload_body):
    version = spec.get("version", 1)
    payload = {"id": slug, "type": ptype, "version": version, **payload_body}
    path = os.path.join(ROOT, "packs", f"{slug}.json")
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    size_kb = max(1, os.path.getsize(path) // 1024)
    manifest_packs.append({
        "id": slug,
        "type": ptype,
        "emoji": spec["emoji"],
        "name": localized("packs", slug, "name"),
        "tagline": localized("packs", slug, "tagline"),
        "description": localized("packs", slug, "description"),
        "tags": spec["tags"],
        "iconSymbol": spec["iconSymbol"],
        "iconColor": spec["iconColor"],
        "version": version,
        "featured": spec["featured"],
        "productId": spec["productId"],
        "banner": f"{RAW}/banners/{slug}.jpg",
        "payload": f"{RAW}/packs/{slug}.json",
        "sizeKB": size_kb,
    })

for slug, spec in DICE_PACKS.items():
    styles = []
    for sid, name_key, body, pip, rough, metal, emission in spec["styles"]:
        styles.append({
            "id": sid,
            "name": localized("styles", name_key),
            "body": body, "pip": pip,
            "roughness": rough, "metalness": metal,
            "emission": emission,
        })
    emit(slug, "dice", spec, {"styles": styles})

for slug, spec in TABLE_PACKS.items():
    surfaces = []
    for (sid, name_key, bg, floor, rough, metal, normal, refl,
         friction, restitution, accent) in spec["surfaces"]:
        surfaces.append({
            "id": sid,
            "name": localized("styles", name_key),
            "background": bg, "floor": floor,
            "roughness": rough, "metalness": metal, "normalIntensity": normal,
            "reflectivity": refl, "friction": friction, "restitution": restitution,
            "accent": accent,
        })
    emit(slug, "table", spec, {"surfaces": surfaces})

for slug, spec in GAME_PACKS.items():
    games = []
    for gid, icon, dice_needed, players in spec["games"]:
        games.append({
            "id": gid,
            "icon": icon,
            "diceNeeded": dice_needed,
            "players": players,
            "name": localized("games", gid, "name"),
            "summary": localized("games", gid, "summary"),
            "rules": localized_rules(gid),
        })
    emit(slug, "games", spec, {"games": games})

manifest = {
    "updated": UPDATED,
    "categories": ["dice", "table", "games"],
    "packs": manifest_packs,
}
with open(os.path.join(ROOT, "packs.json"), "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

print(f"OK: {len(manifest_packs)} packs -> packs.json + packs/*.json "
      f"({len(LANG_CODES)} languages each)")
