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

# Deck configurations (loaded from decklists/decks.json)
with open(DECKLIST_DIR / "decks.json", encoding="utf-8") as _f:
    DECKS = json.load(_f)

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
                # Normalize DFC/split card names: Moxfield uses ' / ', Scryfall uses ' // '
                name = m.group(2).replace(' / ', ' // ')
                cards.append({"name": name, "qty": int(m.group(1))})
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
            if attempt == retries:
                raise
            if e.code == 429:
                time.sleep(2 ** (attempt + 1))
            else:
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
    ascii_name = ascii_name.replace("'", "")  # apostrophes are dropped, not split (e.g. "Dragon's" -> "dragons")
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
        "oracle_id": card.get("oracle_id", ""),
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
    # Handle front-face-only name when full DFC name (A // B) is in cache
    prefix = name + ' // '
    for key in cache:
        if key.startswith(prefix):
            return cache[key]
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

# Include commanders so they get fetched from Scryfall and translated
for config in DECKS.values():
    all_card_names.add(config["commander"])

print(f"\nTotal unique card names (incl. commanders): {len(all_card_names)}")


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

# Retry not-found: batch DFCs via collection endpoint (front-face names), fuzzy for others
retry_dfc = [(n, n.split(' // ')[0].strip()) for n in not_found if ' // ' in n]
retry_other = [n for n in not_found if ' // ' not in n]

if retry_dfc:
    print(f"\n  Batching {len(retry_dfc)} DFC retries by front face...")
    # Build map: front_face -> [original full names]
    front_to_orig = {}
    for orig, front in retry_dfc:
        front_to_orig.setdefault(front, []).append(orig)

    all_fronts = list(front_to_orig.keys())
    for i in range(0, len(all_fronts), 75):
        batch = all_fronts[i:i+75]
        try:
            result = api_post(
                "https://api.scryfall.com/cards/collection",
                {"identifiers": [{"name": f} for f in batch]}
            )
            if result:
                for card in result.get("data", []):
                    info = extract_card_info(card)
                    card_name = card["name"]
                    scryfall_cache[card_name] = info
                    # Match returned card name back to original DFC names
                    # card_name may be just the front face or "Front // Back"
                    card_front = card_name.split(' // ')[0].strip()
                    for orig in front_to_orig.get(card_front, []):
                        scryfall_cache[orig] = info
                        print(f"    DFC BATCH OK: '{orig}' -> '{card_name}'")
                for nf in result.get("not_found", []):
                    nf_front = nf.get("name", "")
                    for orig in front_to_orig.get(nf_front, []):
                        retry_other.append(orig)
        except Exception as e:
            print(f"  DFC batch retry ERROR: {e}")
            for front in batch:
                retry_other.extend(front_to_orig.get(front, []))

time.sleep(0.5)  # pause before individual retries to avoid 429

for name in retry_other:
    try:
        r = api_get(f"https://api.scryfall.com/cards/named?fuzzy={quote(name)}")
        if r:
            scryfall_cache[name] = extract_card_info(r)
            scryfall_cache[r["name"]] = extract_card_info(r)
            print(f"    FUZZY OK: '{name}' -> '{r['name']}'")
    except Exception as e:
        print(f"    FUZZY ERR: '{name}' -> {e}")

# Report any cards still not found after retries
still_missing = [n for n in all_card_names if n not in scryfall_cache and get_card(n, scryfall_cache) is None]
if still_missing:
    # Build a map of missing card -> list of decks that use it
    missing_in_decks = {}
    for nm in still_missing:
        decks_using = [
            deck_id for deck_id, deck in all_decks.items()
            if any(c["name"] == nm for c in deck["cards"])
            or DECKS[deck_id]["commander"] == nm
        ]
        missing_in_decks[nm] = decks_using
    print(f"\n  WARNING: {len(still_missing)} cards not found on Scryfall:")
    for nm in sorted(still_missing):
        decks_str = ", ".join(missing_in_decks[nm]) if missing_in_decks[nm] else "commander list"
        print(f"    - {nm}  [{decks_str}]")

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


def get_french_name_from_card(card):
    """Extract French printed name, handling DFC card_faces."""
    pname = card.get("printed_name")
    if not pname and "card_faces" in card:
        faces = card["card_faces"]
        if any(f.get("printed_name") for f in faces):
            pname = " // ".join(f.get("printed_name") or f.get("name", "") for f in faces)
    return pname or card.get("name", "")


def fetch_french_batch(url):
    """Fetch all pages for a French search URL, return list of (oname, pname) pairs."""
    pairs = []
    result = api_get(url)
    while result:
        for card in result.get("data", []):
            pairs.append((card.get("name", ""), get_french_name_from_card(card)))
        if result.get("has_more"):
            result = api_get(result["next_page"])
        else:
            break
    return pairs


for i in range(0, len(names_to_translate), batch_size):
    batch = names_to_translate[i:i+batch_size]
    # For DFCs use front face name in search
    search_names = [n.split(' // ')[0].strip() if ' // ' in n else n for n in batch]

    or_parts = " or ".join(f'!"{sn}"' for sn in search_names)
    url = f'https://api.scryfall.com/cards/search?q={quote(f"lang:fr ({or_parts})")}&unique=cards'

    backoff = 2
    for attempt in range(5):
        try:
            for oname, pname in fetch_french_batch(url):
                french_names[oname] = pname
                fr_found += 1
            break
        except Exception as e:
            if '429' in str(e) or '503' in str(e):
                print(f"  Rate limited at batch {i//batch_size+1}, waiting {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                break

    if (i // batch_size) % 10 == 0:
        print(f"  Progress: {min(i+batch_size, len(names_to_translate))}/{len(names_to_translate)} ({fr_found} French names)")

# Second pass: retry remaining untranslated cards individually
# For DFC/split cards (" // ") try the FULL name first (split cards are indexed by full name),
# then fall back to front-face-only search.
second_pass = [n for n in scryfall_cache.keys() if n not in french_names]
if second_pass:
    print(f"\n  Second pass: {len(second_pass)} cards without French name, retrying individually...")
    for name in second_pass:
        front_name = name.split(' // ')[0].strip() if ' // ' in name else name
        # Candidates: for split/DFC try full name first, then front face; others just the name
        candidates = ([name, front_name] if ' // ' in name and name != front_name else [front_name])
        for candidate in candidates:
            query = f'!"{candidate}" lang:fr'
            url = f'https://api.scryfall.com/cards/search?q={quote(query)}&unique=cards'
            backoff = 2
            found = False
            for attempt in range(4):
                try:
                    pairs = fetch_french_batch(url)
                    if pairs:
                        oname, pname = pairs[0]
                        french_names[oname] = pname
                        french_names[name] = pname  # map original key too
                        fr_found += 1
                        found = True
                    break
                except Exception as e:
                    if '429' in str(e) or '503' in str(e):
                        time.sleep(backoff)
                        backoff *= 2
                    else:
                        break
            if found:
                break  # no need to try fallback candidate

# Third pass: oracle_id lookup, then single-result soft name search
third_pass = [n for n in scryfall_cache.keys() if n not in french_names]
if third_pass:
    print(f"\n  Third pass: {len(third_pass)} cards, trying oracle_id + soft-name strategies...")
    for name in third_pass:
        found = False

        # Strategy 1: search by oracle_id — reliable for any language/set variant
        oracle_id = scryfall_cache.get(name, {}).get("oracle_id", "")
        if oracle_id:
            query = f'oracleid:{oracle_id} lang:fr'
            url = f'https://api.scryfall.com/cards/search?q={quote(query)}&unique=cards'
            try:
                pairs = fetch_french_batch(url)
                if pairs:
                    oname, pname = pairs[0]
                    french_names[oname] = pname
                    french_names[name] = pname
                    fr_found += 1
                    found = True
                    print(f"    ORACLE_ID OK: '{name}' -> '{pname}'")
            except Exception:
                pass

        # Strategy 2: soft name search (no ! prefix) — accept only unambiguous single result
        if not found:
            search_name = name.split(' // ')[0].strip() if ' // ' in name else name
            query = f'"{search_name}" lang:fr'
            url = f'https://api.scryfall.com/cards/search?q={quote(query)}&unique=cards'
            try:
                result = api_get(url)
                if result and result.get("total_cards") == 1:
                    for card in result.get("data", []):
                        oname = card.get("name", "")
                        pname = get_french_name_from_card(card)
                        french_names[oname] = pname
                        french_names[name] = pname
                        fr_found += 1
                        found = True
                        print(f"    SOFT_NAME OK: '{name}' -> '{pname}'")
            except Exception:
                pass

# Report cards without French translations
untranslated = [n for n in scryfall_cache.keys() if n not in french_names]
if untranslated:
    print(f"\n  {len(untranslated)} cards without French translation (using English name):")
    for nm in sorted(untranslated):
        print(f"    - {nm}")

print(f"\nFrench names: {len(french_names)} total / {len(scryfall_cache)} cards")


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

    # Mana curve (dynamic, no cap)
    cmc_counts = {}
    total_mv = 0
    nonland_count = 0
    kw_counter = Counter()

    for c in cards:
        info = get_card(c["name"], scryfall_cache)
        if info:
            tl = info.get("type_line", "")
            if "Land" not in tl:
                cmc = int(info.get("cmc", 0))
                cmc_counts[cmc] = cmc_counts.get(cmc, 0) + c["qty"]
                total_mv += cmc * c["qty"]
                nonland_count += c["qty"]
            for kw in info.get("keywords", []):
                kw_counter[kw] += c["qty"]

    max_cmc = max(cmc_counts.keys()) if cmc_counts else 0
    curve = [cmc_counts.get(i, 0) for i in range(max_cmc + 1)]

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
