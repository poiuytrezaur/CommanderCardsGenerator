import json
with open('deck_full_data.json', encoding='utf-8') as f:
    data = json.load(f)
for d in data['decks']:
    if d['verified_combos']:
        print(f"=== {d['id']} ===")
        for combo in d['verified_combos'][:4]:
            cards_str = ' + '.join(c['fr'] for c in combo['cards'])
            res = ', '.join(str(r) for r in combo['results'][:2])
            print(f"  {cards_str}")
            print(f"    => {res}")
