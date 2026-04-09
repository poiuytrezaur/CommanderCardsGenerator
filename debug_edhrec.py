import json, urllib.request, ssl
ctx = ssl.create_default_context()
url = 'https://json.edhrec.com/pages/combos/ayara-first-of-locthwain.json'
req = urllib.request.Request(url, headers={'User-Agent':'MTGDeckDesc/1.0','Accept':'application/json'})
with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
    data = json.loads(r.read().decode('utf-8'))
cl = data['container']['json_dict']['cardlists']
for i, combo in enumerate(cl[:8]):
    names = [cv['name'] for cv in combo.get('cardviews',[])]
    sep = ' + '
    print(f'Combo {i}: {sep.join(names)}')
    print(f'  tag: {combo.get("tag","")}')
    print(f'  header: {combo.get("header","")}')
    cb = combo.get('combo',{})
    if cb:
        print(f'  combo keys: {list(cb.keys())}')
        print(f'  combo: {json.dumps(cb)[:400]}')
    print()
