import json

with open('deck_full_data.json', encoding='utf-8') as f:
    data = json.load(f)

for d in data['decks']:
    print(f"\n=== {d['id']} ({d['commander']}) ===")
    print(f"  FR: {d['commander_fr']}")
    print(f"  Curve: {d['mana_curve']}  Avg: {d['avg_mv']}")
    kws = [k['en'] + '(' + k['fr'] + ')' for k in d['top_keywords'][:6]]
    print(f"  Keywords: {', '.join(kws)}")
    if d['verified_combos']:
        for i, combo in enumerate(d['verified_combos'][:5]):
            cards = ' + '.join(c['en'] for c in combo['cards'])
            res = ', '.join(str(r) for r in combo['results'][:2])
            print(f"  Combo {i+1}: {cards} => {res}")
    else:
        print('  No verified combos')
