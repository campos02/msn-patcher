import os
import re
from itertools import groupby

from run_impl import DIR_INPUT, DIR_FINAL

def parse_name(name):
	m = re.search(r'(.+)-(\d+(?:\.\d+)*)-(.+)\.', name)
	if not m:
		raise Exception("can't parse name `{}`".format(name))
	c = m.group(1)
	if c and c.startswith('escargot-'):
		c = c[9:]
	v = tuple(map(int, m.group(2).split('.')))
	l = m.group(3)
	return c, v, l

def extract_version_str(name):
	if name is None:
		return None
	m = re.search(r'-(\d+(?:\.\d+)*)-(.+)\.', name)
	if not m:
		raise Exception("can't parse name `{}`".format(name))
	return m.group(1)

def create_prefixes(*values):
	return list(reversed(values))

class ClientVersion:
	def __init__(self, client, version, langcode):
		self.client = client
		self.version = version
		self.langcode = langcode
		self.installer = None
		self.patched_installer = None

all = {}

for c in DIR_INPUT.iterdir():
	if not c.is_dir(): continue
	cl = c.name
	
	for f in c.iterdir():
		if f.is_dir(): continue
		name = f.name
		_, v, l = parse_name(name)
		k = (cl, v, l)
		if cl == 'msn' and v[0] >= 14:
			stem = f.stem
			e_name = '{}.exe'.format(stem)
			e = DIR_INPUT / 'msn' / 'wle' / e_name
			if e.exists():
				name = e_name
			else:
				name = None
		if k not in all:
			all[k] = ClientVersion(cl, v, l)
		m = all[k]
		m.installer = name

for c in DIR_FINAL.iterdir():
	if not c.is_dir(): continue
	cl = c.name
	
	for f in c.iterdir():
		if f.is_dir(): continue
		name = f.name
		_, v, l = parse_name(name)
		k = (cl, v, l)
		if k not in all:
			all[k] = ClientVersion(cl, v, l)
		m = all[k]
		m.patched_installer = name

prefixes = {
	'msn': create_prefixes(
		(1,), (2,), (3,), (4,), (5,), (6,), (7, 0), (7, 5), (8, 1, 178), (8, 5,), (9,), (14,),
	),
	
	'yahoo': create_prefixes(
		(5, 0), (5, 5),
	),
}

print('client,version,langcode,patched_installer,installer,recommended')
all = sorted(all.items(), key = lambda m: m[0][0])
all = sorted([tpl[1] for tpl in all], key = lambda m: (m.client, m.langcode, m.version))
by_client = groupby(all, key = lambda m: m.client)
for client, clients in by_client:
	for langcode, clients_by_langcode in groupby(clients, key = lambda m: m.langcode):
		clients_by_langcode = list(clients_by_langcode)
		for pre in prefixes[client]:
			clients_by_langcode2 = list(sorted(filter((lambda m: m.version[:len(pre)] == pre), clients_by_langcode), key = (lambda m: m.version), reverse = True))
			installer = None
			patched_installer = None
			version = None
			for m in clients_by_langcode2:
				installer = installer or m.installer
				patched_installer = patched_installer or m.patched_installer
				version = version or ''.join((str(m.version[0]), str(m.version[1])))
			if installer or patched_installer:
				print(','.join([client, version, langcode, patched_installer or '', installer or '', 'false']))
