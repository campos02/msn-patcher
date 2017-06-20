import re
import shutil
from pathlib import Path
from langcode import LANGCODE

dir = Path('e:/data/msn/unorganized/MSN Messenger')
inputdir = Path('input')

def find_installer(p):
	for a in p.glob('*.exe'): return a
	for a in p.glob('*.msi'): return a
	return None

for a in dir.iterdir():
	if a.name.endswith('[Patch]'):
		continue
	m = re.match(r'v(\d\.\d\.\d{4})(?:\.0)? \((.+)\)', a.name)
	assert m
	v = m.group(1)
	l = m.group(2)
	lc = LANGCODE[l.lower()]
	
	inst = find_installer(a)
	assert inst is not None
	
	name = 'msn-{}-{}{}'.format(v, lc, inst.suffix).lower()
	f = inputdir / name
	if f.exists(): continue
	print(f)
	shutil.copy(str(inst), str(f))
