import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/alvar/Documents/AlvGolf/output/ux_temp.json', encoding='utf-8') as f:
    d = json.load(f)

c = d.get('content', {})
raw = c.get('raw_content', '')
if raw.startswith('```'):
    raw = raw.split('\n', 1)[1]

lines = raw.split('\n')
print(f"Total lineas: {len(lines)} | Total chars: {len(raw)}")
print()
print("Ultimas 5 lineas:")
for i, l in enumerate(lines[-5:], start=len(lines)-4):
    print(f"  L{i}: {l}")
print()
print("Secciones encontradas en el JSON parcial:")
for section in ['hero_statement', 'dna_profile', 'chart_titles', 'insight_boxes', 'quick_wins', 'roi_cards', 'stat_cards', 'trend_narratives', 'course_cards', 'club_cards']:
    found = f'"{section}"' in raw
    marker = ' ✅' if section in ('hero_statement','dna_profile','chart_titles','insight_boxes','quick_wins','roi_cards') else ''
    print(f"  {section}: {'PRESENT' if found else 'MISSING'}{marker}")
