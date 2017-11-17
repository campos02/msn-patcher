import os
import re
from itertools import groupby

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

prefixes = list(reversed([
	(1,), (2,), (3,), (4,), (5,), (6,), (7, 0), (7, 5), (8, 1, 178),
]))

print('langcode,patched_installer,installer')
all = sorted(all.values(), key = lambda m: (m.langcode, m.version))
for langcode, msns in groupby(all, key = lambda m: m.langcode):
	msns = list(msns)
	for pre in prefixes:
		msns2 = list(sorted(filter((lambda m: m.version[:len(pre)] == pre), msns), key = (lambda m: m.version), reverse = True))
		installer = None
		patched_installer = None
		for m in msns2:
			installer = installer or m.installer
			patched_installer = patched_installer or m.patched_installer
		if installer or patched_installer:
			print(','.join([langcode, patched_installer or '', installer or '']))
