"""Validate local links and reported metrics. No network or live-service mutations."""
from pathlib import Path
import csv,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for p in ROOT.rglob('*.md'):
    text=p.read_text()
    targets=re.findall(r'\]\(([^)]+)\)',text)+re.findall(r'(?:src|href)="([^"]+)"',text)
    for target in targets:
        if target.startswith(('https://','http://','mailto:','#','$')):continue
        target=target.split('#')[0]
        if target and not (p.parent/target).exists():errors.append(f'{p.relative_to(ROOT)}: {target}')
for p in (ROOT/'assets').glob('*.svg'):ET.parse(p)
rows=list(csv.DictReader((ROOT/'data/interview-metrics.csv').open()))
assert len(rows)==10
assert sum(int(r['questions']) for r in rows)==223
assert abs(sum(int(r['discovery_percent']) for r in rows)/10-58.8)<1e-9
assert json.loads((ROOT/'data/evaluation-summary.json').read_text())['official_rank'] is None
assert not list(ROOT.rglob('.env'))
if errors:raise SystemExit('Broken local links: '+str(errors))
print('OK: local links, SVG XML, 10 stakeholders, 223 questions, 58.8 mean, evaluation labels')
