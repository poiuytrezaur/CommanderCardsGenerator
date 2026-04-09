#!/usr/bin/env python3
"""
Fetch comprehensive deck data from Scryfall, Commander Spellbook, and EDHREC.
Parses exported Moxfield decklists from decklists/ folder.
Outputs deck_full_data.json for HTML generation.
"""

import json, re, time, os, sys, unicodedata
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from pathlib import Path
from collections import Counter

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DECKLIST_DIR = BASE_DIR / "decklists"
OUTPUT_FILE = BASE_DIR / "deck_full_data.json"

# Deck configurations
DECKS = {
    "ayara":   {"commander": "Ayara, First of Locthwain",    "colors": ["B"]},
    "ellivere":{"commander": "Ellivere of the Wild Court",   "colors": ["G", "W"]},
    "gargos":  {"commander": "Gargos, Vicious Watcher",      "colors": ["G"]},
    "jasper":  {"commander": "Laughing Jasper Flint",         "colors": ["B", "R"]},
    "terra":   {"commander": "Terra, Herald of Hope",         "colors": ["W", "B", "R"]},
    "suspend": {"commander": "Alaundo the Seer",             "colors": ["U", "G"]},
    "sidisi":  {"commander": "Sidisi, Brood Tyrant",          "colors": ["B", "G", "U"]},
    "ognid":   {"commander": "Ognis, the Dragon's Lash",      "colors": ["B", "R", "G"]},
    "neera":   {"commander": "Neera, Wild Mage",              "colors": ["U", "R"]},
    "Nazegul": {"commander": "Lord of the Nazgûl",            "colors": ["U", "B"]},
    "maarika": {"commander": "Maarika, Brutal Gladiator",     "colors": ["B", "R", "G"]},
    "kuja":    {"commander": "Kuja, Genome Sorcerer",         "colors": ["B", "R"]},
    "gimli":   {"commander": "Gimli, Mournful Avenger",       "colors": ["R", "G"]},
    "cloud":   {"commander": "Cloud, Ex-SOLDIER",             "colors": ["W", "R", "G"]},
}

KEYWORD_FR = {
    "Flying": "Vol", "Trample": "Piétinement", "Haste": "Célérité",
    "Lifelink": "Lien de vie", "Deathtouch": "Contact mortel",
    "First strike": "Initiative", "Double strike": "Double initiative",
    "Vigilance": "Vigilance", "Reach": "Portée", "Menace": "Menace",
    "Hexproof": "Défense talismanique", "Indestructible": "Indestructible",
    "Flash": "Flash", "Ward": "Garde", "Infect": "Infection",
    "Toxic": "Toxique", "Proliferate": "Prolifération", "Cascade": "Cascade",
    "Suspend": "Suspension", "Dredge": "Drague", "Convoke": "Convocation",
    "Undying": "Immortel", "Persist": "Persistance", "Cycling": "Recyclage",
    "Evoke": "Évocation", "Changeling": "Changelin", "Equip": "Équiper",
    "Protection": "Protection", "Mill": "Meule", "Scry": "Regard",
    "Exploit": "Exploitation", "Wither": "Flétrissement",
    "Defender": "Défenseur", "Shroud": "Linceul", "Absorb": "Absorption",
    "Affinity": "Affinité", "Annihilator": "Annihilateur",
    "Flanking": "Débordement", "Morph": "Mue", "Partner": "Partenaire",
}


def parse_decklist(filepath):
    cards = []
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(r'^(\d+)\s+(.+?)\s+\([A-Za-z0-9]+\)\s+\S+', line)
            if m:
                cards.append({"name": m.group(2), "qty": int(m.group(1))})
    return cards


def api_get(url, retries=2):
    time.sleep(0.12)
    headers = {"User-Agent": "MTGDeckDesc/1.0", "Accept": "application/json"}
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=headers)
            resp = urlopen(req, timeout=30)
            return json.loads(resp.read())
        except HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429:
                time.sleep(2)
                continue
            if attempt == retries:
                raise
            time.sleep(0.5)
        except (URLError, TimeoutError):
            if attempt == retries:
                raise
            time.sleep(1)


def api_post(url, data, retries=2):
    time.sleep(0.12)
    headers = {
        "User-Agent": "MTGDeckDesc/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    for attempt in range(retries + 1):
        try:
            req = Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            resp = urlopen(req, timeout=30)
            return json.loads(resp.read())
        except HTTPError as e:
            if e.code == 429:
                time.sleep(2)
                continue
            if attempt == retries:
                raise
            time.sleep(0.5)
        except (URLError, TimeoutError):
            if attempt == retries:
                raise
            time.sleep(1)


def slugify(name):
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_name = nfkd.encode('ascii', 'ignore').decode('ascii')
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_name.lower()).strip('-')
    return slug


def extract_card_info(card):
    if 'card_faces' in card and 'oracle_text' not in card:
        face = card['card_faces'][0]
        oracle_text = face.get('oracle_text', '')
        mana_cost = face.get('mana_cost', '')
    else:
        oracle_text = card.get('oracle_text', '')
        mana_cost = card.get('mana_cost', '')

    return {
        "name": card.get("name", ""),
        "oracle_text": oracle_text,
        "mana_cost": mana_cost,
        "cmc": card.get("cmc", 0),
        "type_line": card.get("type_line", ""),
        "keywords": card.get("keywords", []),
    }


def get_card(name, cache):
    """Look up card info with name variants."""
    if name in cache:
        return cache[name]
    if ' / ' in name:
        alt = name.replace(' / ', ' // ')
        if alt in cache:
            return cache[alt]
        front = name.split(' / ')[0].strip()
        if front in cache:
            return cache[front]
    return None


# ─── PHASE 1: Parse decklists ───
print("=" * 60)
print("PHASE 1: Parsing decklists")
print("=" * 60)

all_decks = {}
all_card_names = set()

for deck_id, config in DECKS.items():
    filepath = DECKLIST_DIR / f"{deck_id}.md"
    if not filepath.exists():
        print(f"  WARNING: {filepath} not found!")
        continue
    cards = parse_decklist(filepath)
    all_decks[deck_id] = {
        "id": deck_id,
        "commander": config["commander"],
        "colors": config["colors"],
        "cards": cards,
    }
    names = set(c["name"] for c in cards)
    all_card_names.update(names)
    print(f"  {deck_id}: {sum(c['qty'] for c in cards)} cards ({len(names)} unique)")

print(f"\nTotal unique card names: {len(all_card_names)}")


# ─── PHASE 2: Scryfall card data ───
print("\n" + "=" * 60)
print("PHASE 2: Fetching Scryfall card data")
print("=" * 60)

scryfall_cache = {}
not_found = []
unique_list = list(all_card_names)

for i in range(0, len(unique_list), 75):
    batch = unique_list[i:i+75]
    identifiers = [{"name": n} for n in batch]
    try:
        result = api_post(
            "https://api.scryfall.com/cards/collection",
            {"identifiers": identifiers}
        )
        for card in result.get("data", []):
            scryfall_cache[card["name"]] = extract_card_info(card)
        nf = [x.get("name", "") for x in result.get("not_found", [])]
        not_found.extend(nf)
        print(f"  Batch {i//75+1}: {len(result.get('data',[]))} found, {len(nf)} not found")
    except Exception as e:
        print(f"  Batch {i//75+1} ERROR: {e}")

# Retry not-found: try front face for DFCs, then fuzzy search
retry_dfc = [(n, n.split(' / ')[0].strip()) for n in not_found if ' / ' in n]
retry_other = [n for n in not_found if ' / ' not in n]

for orig, front in retry_dfc:
    try:
        r = api_get(f"https://api.scryfall.com/cards/named?fuzzy={quote(front)}")
        if r:
            scryfall_cache[orig] = extract_card_info(r)
            scryfall_cache[r["name"]] = extract_card_info(r)
        else:
            retry_other.append(orig)
    except:
        retry_other.append(orig)

for name in retry_other:
    try:
        r = api_get(f"https://api.scryfall.com/cards/named?fuzzy={quote(name)}")
        if r:
            scryfall_cache[name] = extract_card_info(r)
            scryfall_cache[r["name"]] = extract_card_info(r)
    except:
        print(f"  NOT FOUND: {name}")

print(f"\nScryfall cache: {len(scryfall_cache)} entries")


# ─── PHASE 3: French card names ───
print("\n" + "=" * 60)
print("PHASE 3: Fetching French card names from Scryfall")
print("=" * 60)

french_names = {
    "Forest": "Forêt", "Mountain": "Montagne", "Island": "Île",
    "Swamp": "Marais", "Plains": "Plaines",
}

# Use oracle names from Scryfall cache for accuracy
names_to_translate = [n for n in scryfall_cache.keys() if n not in french_names]
batch_size = 10
fr_found = 0

for i in range(0, len(names_to_translate), batch_size):
    batch = names_to_translate[i:i+batch_size]
    # For DFCs use front face name in search
    search_names = []
    for n in batch:
        if ' // ' in n:
            search_names.append(n.split(' // ')[0].strip())
        else:
            search_names.append(n)

    or_parts = " or ".join(f'!"{sn}"' for sn in search_names)
    query = f'lang:fr ({or_parts})'
    url = f'https://api.scryfall.com/cards/search?q={quote(query)}&unique=cards'

    try:
        result = api_get(url)
        if result:
            for card in result.get("data", []):
                pname = card.get("printed_name", card.get("name", ""))
                oname = card.get("name", "")
                french_names[oname] = pname
                fr_found += 1
            while result and result.get("has_more"):
                result = api_get(result["next_page"])
                if result:
                    for card in result.get("data", []):
                        pname = card.get("printed_name", card.get("name", ""))
                        oname = card.get("name", "")
                        french_names[oname] = pname
                        fr_found += 1
    except:
        pass

    if (i // batch_size) % 10 == 0:
        print(f"  Progress: {min(i+batch_size, len(names_to_translate))}/{len(names_to_translate)} ({fr_found} French names)")

print(f"\nFrench names: {len(french_names)} total")


# ─── PHASE 4: Combo data ───
print("\n" + "=" * 60)
print("PHASE 4: Fetching combo data")
print("=" * 60)

combo_data = {}

for deck_id, config in DECKS.items():
    if deck_id not in all_decks:
        continue
    commander = config["commander"]
    deck_card_names = set()
    for c in all_decks[deck_id]["cards"]:
        deck_card_names.add(c["name"])
        # Also add Scryfall oracle name variants
        info = get_card(c["name"], scryfall_cache)
        if info:
            deck_card_names.add(info["name"])

    combos = {"spellbook": [], "edhrec": []}

    # Commander Spellbook
    try:
        url = f'https://backend.commanderspellbook.com/variants/?q=card:"{quote(commander)}"&limit=50&format=json'
        result = api_get(url)
        if result:
            for variant in result.get("results", []):
                cards = [u.get("card", {}).get("name", "") for u in variant.get("uses", [])]
                results = [r.get("feature", {}).get("name", "") for r in variant.get("produces", [])]
                in_deck = all(c in deck_card_names for c in cards if c)
                combos["spellbook"].append({
                    "cards": cards,
                    "results": results,
                    "in_deck": in_deck,
                })
            verified = sum(1 for c in combos["spellbook"] if c["in_deck"])
            print(f"  {deck_id} Spellbook: {len(combos['spellbook'])} total, {verified} verified")
    except Exception as e:
        print(f"  {deck_id} Spellbook error: {e}")

    # EDHREC
    slug = slugify(commander)
    try:
        url = f'https://json.edhrec.com/pages/combos/{slug}.json'
        result = api_get(url)
        if result:
            container = result.get("container", {})
            json_dict = container.get("json_dict", {})
            cardlists = json_dict.get("cardlists", [])
            for entry in cardlists:
                cardviews = entry.get("cardviews", [])
                combo_cards = [cv.get("name", "") for cv in cardviews]
                combo_results = entry.get("combo", {}).get("results", [])
                in_deck = all(c in deck_card_names for c in combo_cards if c)
                combos["edhrec"].append({
                    "cards": combo_cards,
                    "results": combo_results,
                    "in_deck": in_deck,
                })
            verified = sum(1 for c in combos["edhrec"] if c["in_deck"])
            print(f"  {deck_id} EDHREC: {len(combos['edhrec'])} total, {verified} verified")
    except Exception as e:
        print(f"  {deck_id} EDHREC error: {e}")

    combo_data[deck_id] = combos


# ─── PHASE 5: Compile output ───
print("\n" + "=" * 60)
print("PHASE 5: Compiling deck statistics")
print("=" * 60)

output = {"decks": []}

for deck_id in DECKS:
    if deck_id not in all_decks:
        continue
    deck = all_decks[deck_id]
    cards = deck["cards"]

    # Mana curve (0–7+)
    curve = [0] * 8
    total_mv = 0
    nonland_count = 0
    kw_counter = Counter()

    for c in cards:
        info = get_card(c["name"], scryfall_cache)
        if info:
            tl = info.get("type_line", "")
            if "Land" not in tl:
                cmc = int(info.get("cmc", 0))
                curve[min(cmc, 7)] += c["qty"]
                total_mv += cmc * c["qty"]
                nonland_count += c["qty"]
            for kw in info.get("keywords", []):
                kw_counter[kw] += c["qty"]

    avg_mv = round(total_mv / nonland_count, 2) if nonland_count else 0

    # Top keywords
    top_kw = []
    for kw, count in kw_counter.most_common(10):
        top_kw.append({"en": kw, "fr": KEYWORD_FR.get(kw, kw), "count": count})

    # Verified combos (deduplicated)
    verified_combos = []
    seen_keys = set()
    for src in ["spellbook", "edhrec"]:
        for combo in combo_data.get(deck_id, {}).get(src, []):
            if combo["in_deck"]:
                key = frozenset(combo["cards"])
                if key not in seen_keys:
                    seen_keys.add(key)
                    # Get French names for combo cards
                    cards_fr = []
                    for cn in combo["cards"]:
                        fr = french_names.get(cn, cn)
                        cards_fr.append({"en": cn, "fr": fr})
                    verified_combos.append({
                        "cards": cards_fr,
                        "results": combo["results"],
                        "source": src,
                    })

    # French commander name
    commander_fr = french_names.get(deck["commander"], deck["commander"])

    deck_data = {
        "id": deck_id,
        "commander": deck["commander"],
        "commander_fr": commander_fr,
        "colors": deck["colors"],
        "card_count": sum(c["qty"] for c in cards),
        "unique_cards": len(set(c["name"] for c in cards)),
        "mana_curve": curve,
        "avg_mv": avg_mv,
        "top_keywords": top_kw,
        "verified_combos": verified_combos,
    }
    output["decks"].append(deck_data)
    print(f"  {deck_id}: curve={curve} avg={avg_mv} kw={len(top_kw)} combos={len(verified_combos)}")

# Save
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"Output saved to {OUTPUT_FILE}")
print(f"{'='*60}")
