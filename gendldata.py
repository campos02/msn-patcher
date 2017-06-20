import os
import re
from itertools import groupby

code = {
	'English - United States': 'en',
	'Spanish': 'es',
	'Arabic': 'ar',
	'China': 'zh-cn',
	'Twi': 'zh-tw',
	'Danish': 'da',
	'Czech'    : 'CS',
	'Danish'   : 'DA',
	'Dutch'    : 'NL',
	'English'  : 'EN',
	'Finnish'  : 'FI',
	'French'   : 'FR',
	'German'   : 'DE',
	'Greek'    : 'EL',
	'Hebrew'   : 'HE',
	'Hungarian': 'HU',
	'Italian'  : 'IT',
	'Japanese' : 'JA',
	'Korean'   : 'KO',
	'Norwegian': 'NO',
	'Polish'   : 'PL',
	'Russian'  : 'RU',
	'Slovak'   : 'SK',
	'Slovene': 'SL',
	'Spanish'  : 'ES',
	'Swedish'  : 'SV',
	'Turkish'  : 'TR',
	'Portuguese - Brazil': 'PT-BR',
	'Portuguese': 'PT-PT',
}

def parse_name(name):
	m = re.search(r'-(\d+(?:\.\d+)*)-(.+)\.', name)
	if not m:
		raise Exception("can't parse name `{}`".format(name))
	v = tuple(map(int, m.group(1).split('.')))
	l = m.group(2)
	return v, l

def extract_version_str(name):
	if name is None:
		return None
	m = re.search(r'-(\d+(?:\.\d+)*)-(.+)\.', name)
	if not m:
		raise Exception("can't parse name `{}`".format(name))
	return m.group(1)

class MSNVersion:
	def __init__(self, version, langcode):
		self.version = version
		self.langcode = langcode
		self.installer = None
		self.patched_installer = None

all = {}

for name in os.listdir('input'):
	v, l = parse_name(name)
	k = (v, l)
	if k not in all:
		all[k] = MSNVersion(v, l)
	m = all[k]
	m.installer = name

for name in os.listdir('final'):
	v, l = parse_name(name)
	k = (v, l)
	if k not in all:
		all[k] = MSNVersion(v, l)
	m = all[k]
	m.patched_installer = name

print('langcode,patched_installer,installer')
all = sorted(all.values(), key = lambda m: (m.langcode, m.version))
for langcode, msns in groupby(all, key = lambda m: m.langcode):
	msns = sorted(msns, key = (lambda m: m.version), reverse = True)
	
	for m in msns:
		print(','.join([langcode, m.patched_installer or '', m.installer or '']))
