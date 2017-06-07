import os
from os.path import abspath, exists
import shutil
import re
import subprocess

PATCH_NAME = 'escargot-msn'
PATCH_VERSION = 1

def main():
	mkdirp('input')
	mkdirp('versions')
	mkdirp('final')
	
	download_all()
	
	for name in os.listdir('input'):
		name = name.replace('.exe', '')
		print(name)
		mkdirp('versions/' + name)
		extract_installer(name)
		v, _ = parse_name(name)
		if v[0] < 5:
			# Figure it out later
			pass
		elif v[0] < 8:
			extract_msi(name)
			patch_extracted_msi(name)
			pack_patched_msi(name)
		else:
			# Doesn't work yet
			pass

def mkdirp(d):
	os.makedirs(d, exist_ok = True)

def patch_extracted_msi(name):
	outdir = 'versions/{}/msi-patched'.format(name)
	if exists(outdir):
		return
	shutil.copytree('versions/{}/msi'.format(name), outdir)
	
	try:
		msi_files = outdir + '/files'
		
		v, _ = parse_name(name)
		msn = find_file(msi_files, r'msnmsgr.*')
		assert msn is not None
		
		with open(msn, 'rb') as fh:
			msn_content = fh.read()
		msn_content = msn_content.replace(b'messenger.hotmail.com', b'm1.escargot.log1p.xyz')
		if v[0:2] < (7, 5):
			msn_content = msn_content.replace(b'nexus.passport.com/rdr/pprdr.asp', b'm1.escargot.log1p.xyz/nexus-mock')
			msn_content = msn_content.replace(b'PassportURLs', b'Passporturls')
		if v[0] >= 6:
			msn_content = msn_content.replace(b'http://config.messenger.msn.com/Config/MsgrConfig.asmx', b'https://escargot.log1p.xyz/etc/MsgrConfig?padding=qqqq')
		with open(msn, 'wb') as fh:
			fh.write(msn_content)
		
		if v[0:2] >= (7, 5):
			msidcrl = find_file(msi_files, r'msidcrl.dll')
			assert msidcrl is not None
			os.remove(msidcrl)
			shutil.copyfile('msidcrl.dll', msidcrl)
	except:
		shutil.rmtree(outdir)
		raise

def find_file(dir, regex):
	for fn in os.listdir(dir):
		if re.match(regex, fn.lower()):
			return dir + '/' + fn
	return None

def pack_patched_msi(name):
	outfile = 'final/escargot-{}.msi'.format(name)
	if exists(outfile):
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
		'-o', outfile,
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
	outdir = 'versions/{}/msi'.format(name)
	if exists(outdir):
		return
	os.mkdir(outdir)
	
	try:
		msi2xml = abspath('msi2xml/msi2xml.exe')
		msi = abspath('versions/{}/extracted/MsnMsgs.msi'.format(name))
		here = abspath('.')
		
		os.chdir(outdir)
		subprocess.call([
			msi2xml, '-q', '-b', 'streams', '-c', 'files',
			'-o', 'MsnMsgs.xml', msi
		])
	except:
		shutil.rmtree(outdir)
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
	outdir = abspath('versions/{}/extracted'.format(name))
	if exists(outdir):
		return
	os.mkdir(outdir)
	try:
		subprocess.run(['input/{}.exe'.format(name), '/T:{}'.format(outdir), '/C', '/Q'], check = True, stdout = subprocess.PIPE)
	except:
		shutil.rmtree(outdir)
		raise

def download_all():
	import data
	for d in data.DOWNLOADS:
		fn = 'input/msn-{}-{}.exe'.format(d.version, d.langcode)
		_get_to_file(d.installer_official, fn)

def _get_to_file(url, filename):
	import requests
	if exists(filename):
		return
	print("download", filename)
	r = requests.get(url)
	try:
		r.raise_for_status()
	except:
		return
	with open(filename, 'wb') as fh:
		for chunk in r.iter_content(chunk_size = 8192):
			if chunk: fh.write(chunk)

if __name__ == '__main__':
	main()
