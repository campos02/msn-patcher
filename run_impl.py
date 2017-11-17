from pathlib import Path
import os
from os.path import abspath
import shutil
import re
import subprocess

PATCH_NAME = 'escargot-msn'
PATCH_VERSION = 1

DIR_INPUT = Path('input')
DIR_VERSIONS = Path('versions')
DIR_FINAL = Path('final')

def main():
	mkdirp(DIR_INPUT)
	mkdirp(DIR_VERSIONS)
	mkdirp(DIR_FINAL)
	
	for p in DIR_INPUT.iterdir():
		name = p.stem
		print(name)
		mkdirp(DIR_VERSIONS / name)
		extract_installer(name)
		v, _ = parse_name(name)
		if v[0] < 5:
			# Figure it out later
			pass
		elif v[0:2] < (8, 5):
			extract_msi(name)
			patch_extracted_msi(name)
			pack_patched_msi(name)
		else:
			# Doesn't work yet
			pass

def mkdirp(p):
	p.mkdir(parents = True, exist_ok = True)

def patch_extracted_msi(name):
	outdir = DIR_VERSIONS / name / 'msi-patched'
	if outdir.exists():
		return
	shutil.copytree(str(DIR_VERSIONS / name / 'msi'), str(outdir))
	
	try:
		msi_files = outdir / 'files'
		
		v, _ = parse_name(name)
		msn = find_file(msi_files, r'msnmsgr.*')
		assert msn is not None
		
		with msn.open('rb') as fh:
			msn_content = fh.read()
		msn_content = replace(msn_content, b'messenger.hotmail.com', b'm1.escargot.log1p.xyz')
		if v[0:2] < (7, 5):
			msn_content = replace(msn_content, b'nexus.passport.com/rdr/pprdr.asp', b'm1.escargot.log1p.xyz/nexus-mock')
			msn_content = replace(msn_content, b'PassportURLs', b'Passporturls')
		if v[0] >= 6:
			msn_content = replace(msn_content, b'http://config.messenger.msn.com/Config/MsgrConfig.asmx', b'https://escargot.log1p.xyz/etc/MsgrConfig?padding=qqqq')
		if (8, 0) <= v[0:2] <= (8, 1):
			msn_content = replace(msn_content, b'byrdr.omega.contacts.msn.com', b'ebyrdromegactcsmsn.log1p.xyz')
			msn_content = replace(msn_content, b'tkrdr.storage.msn.com', b'etkrdrstmsn.log1p.xyz')
			msn_content = replace(msn_content, b'//ows.messenger.msn.com', b'//eowsmsgrmsn.log1p.xyz')
			msn_content = replace(msn_content, b'//rsi.hotmail.com', b'//ersih.log1p.xyz')
		
		with msn.open('wb') as fh:
			fh.write(msn_content)
		
		if v[0:2] == (7, 5):
			msidcrl = find_file(msi_files, r'msidcrl.dll')
			assert msidcrl is not None
		elif v[0:3] == (8, 1, 178):
			msidcrl = find_file(msi_files, r'msidcrl40.dll')
			assert msidcrl is not None
		else:
			msidcrl = None
		
		if msidcrl:
			os.remove(str(msidcrl))
			shutil.copyfile('msidcrl.dll', str(msidcrl))
	except:
		shutil.rmtree(str(outdir))
		raise

def replace(content, src, dst):
	assert len(src) == len(dst)
	return content.replace(src, dst)

def find_file(dir, regex):
	for p in dir.iterdir():
		if re.search(regex, p.name.lower()):
			return p
	return None

def pack_patched_msi(name):
	outfile = DIR_FINAL / 'escargot-{}.msi'.format(name)
	if outfile.exists():
		return
	
	xml2msi = abspath('msi2xml/xml2msi.exe')
	xml = abspath('versions/{}/msi-patched/MsnMsgs.xml'.format(name))
	
	#v, langcode = parse_name(name)
	#product_guid = gen_code(PATCH_NAME, v[0], langcode)
	#product_version_guid = gen_code(PATCH_NAME, v[0], langcode, PATCH_VERSION)
	
	subprocess.call([
		xml2msi, '-q', '-m',
		#'-d', product_version_guid, # --product-code
		#'-g', product_guid, # --upgrade-code
		'-o', str(outfile),
		xml
	])

def gen_code(*parts):
	import hashlib
	h = hashlib.sha256()
	for p in parts:
		p = str(p)
		h.update(str(len(p)).encode('utf-8'))
		h.update(b' ')
		h.update(p.encode('utf-8'))
	hex = ''.join('{:02x}'.format(c) for c in h.digest())
	return '{}-{}-{}-{}'.format(
		hex[0:8], hex[8:12], hex[12:16], hex[16:20], hex[20:32],
	)

def extract_msi(name):
	outdir = DIR_VERSIONS / name / 'msi'
	if outdir.exists(): return
	outdir.mkdir(parents = True)
	
	here = abspath('.')
	
	try:
		msi2xml = abspath('msi2xml/msi2xml.exe')
		msi = abspath('versions/{}/extracted/MsnMsgs.msi'.format(name))
		
		os.chdir(str(outdir))
		subprocess.call([
			msi2xml, '-q', '-b', 'streams', '-c', 'files',
			'-o', 'MsnMsgs.xml', msi
		])
	except:
		shutil.rmtree(str(outdir))
		raise
	finally:
		os.chdir(here)

def parse_name(name):
	m = re.search(r'-(\d+(?:\.\d+)*)-(.+)$', name)
	if not m:
		raise Exception("can't parse name `{}`".format(name))
	v = tuple(map(int, m.group(1).split('.')))
	l = m.group(2)
	return v, l

def extract_installer(name):
	outdir = DIR_VERSIONS / name / 'extracted'
	if outdir.exists(): return
	outdir.mkdir(parents = True)
	
	exefile = DIR_INPUT / '{}.exe'.format(name)
	msifile = DIR_INPUT / '{}.msi'.format(name)
	try:
		if exefile.exists():
			subprocess.run([str(exefile), '/T:{}'.format(abspath(str(outdir))), '/C', '/Q'], check = True, stdout = subprocess.PIPE)
		elif msifile.exists():
			shutil.copy(str(msifile), str(outdir / 'MsnMsgs.msi'))
		else:
			assert False
	except:
		shutil.rmtree(str(outdir))
		raise

if __name__ == '__main__':
	main()
