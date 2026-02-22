import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/alvar/Documents/AlvGolf/output/ux_temp.json', encoding='utf-8') as f:
    d = json.load(f)

c = d.get('content', {})

# Deswrappear raw_content si necesario
if isinstance(c, dict) and c.get('raw_content') and not c.get('hero_statement'):
    raw = c['raw_content']
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    c = json.loads(raw)
    print('raw_content deswrappeado OK')

print('Secciones generadas:', list(c.keys()))
for k, v in c.items():
    sz = len(json.dumps(v, ensure_ascii=False))
    marker = ' ✅ (usada)' if k in ('hero_statement','dna_profile','chart_titles','insight_boxes','quick_wins','roi_cards') else ''
    print(f'  {k}: {sz} chars{marker}')

with open('C:/Users/alvar/Documents/AlvGolf/output/ai_content.json', 'w', encoding='utf-8') as f:
    json.dump(c, f, ensure_ascii=False, indent=2)

print()
print('ai_content.json guardado correctamente')
