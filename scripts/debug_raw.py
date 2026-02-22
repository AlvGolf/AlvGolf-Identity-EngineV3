import json

with open('C:/Users/alvar/Documents/AlvGolf/output/ux_temp.json', encoding='utf-8') as f:
    d = json.load(f)

c = d.get('content', {})
raw = c.get('raw_content', '')
if raw.startswith('```'):
    raw = raw.split('\n', 1)[1]

lines = raw.split('\n')
print(f'Total lineas: {len(lines)}')
print(f'Char count total: {len(raw)}')
print()

# Mostrar lineas alrededor del truncamiento (170-177)
print('Lineas 169-177:')
for i, l in enumerate(lines[168:177], start=169):
    print(f'  L{i} ({len(l)} chars): {l[:120]}')
    for j, ch in enumerate(l):
        if ord(ch) > 127:
            print(f'    pos {j}: U+{ord(ch):04X} = {repr(ch)}')

print()
print('Ultima linea:')
print(f'  L{len(lines)}: {repr(lines[-1][:200])}')
