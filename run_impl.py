from pathlib import Path
import os
from os.path import abspath
import shutil
import re
import subprocess
import hashlib
from lxml import etree
from peimp import append_import

PATCH_NAME = 'escargot-msn'
PATCH_VERSION = 1

PATCH_DLL = 'escargot.dll'
PATCH_DLL_FUNC = 'ImportMe'

#ROOT = Path('d:/data/msn-patcher')
ROOT = Path('c:/home/escargot/msn-patcher')
DIR_INPUT = ROOT / 'input'
DIR_VERSIONS = ROOT / 'versions'
DIR_INSTALLER = ROOT / 'installer'
DIR_FINAL = ROOT / 'final'

def main():
	mkdirp(DIR_INPUT)
	mkdirp(DIR_VERSIONS)
	mkdirp(DIR_FINAL)
	
	for p in DIR_INPUT.iterdir():
		if not p.is_dir(): continue
		program_name = p.name
		for v in p.iterdir():
			if v.is_dir(): continue
			version_name = v.stem
			print(version_name)
			mkdirp(DIR_VERSIONS / program_name / version_name)
			try:
				extract_installer(version_name, program_name)
			except:
				continue
			v, _, _ = parse_name(version_name)
			if program_name == 'msn':
				if v[0] < 5:
					# Figure it out later
					pass
				elif v[0] < 15:
					extract_msi(version_name)
					product_code_tpl = patch_extracted_msi(version_name)
					pack_patched_msi(version_name, product_code_tpl)
				else:
					# Doesn't work yet
					pass
			elif program_name == 'yahoo':
				if v[0] == 5:
					if v[1] < 6:
						patch_yahoo_files(version_name)
						pack_patched_yahoo(version_name)
				else:
					pass
			else:
				# Undetermined/unsupported program, ignore
				pass

def mkdirp(p):
	p.mkdir(parents = True, exist_ok = True)

# General functions

def extract_installer(version_name, program_name):
	v, _, vs = parse_name(version_name)
	
	outdir = DIR_VERSIONS / program_name / version_name / 'extracted'
	if outdir.exists(): return
	outdir.mkdir(parents = True)
	
	here = abspath('.')
	
	try:
		if program_name == 'msn':
			outdir_msgr = outdir / 'messenger'
			outdir_msgr.mkdir(parents = True)
			
			exefile = DIR_INPUT / 'msn/{}.exe'.format(version_name)
			msifile = DIR_INPUT / 'msn/{}.msi'.format(version_name)
			
			if exefile.exists():
				subprocess.run([str(exefile), '/T:{}'.format(abspath(str(outdir_msgr))), '/C', '/Q'], check = True, stdout = subprocess.PIPE)
			elif msifile.exists():
				shutil.copy(str(msifile), str(outdir_msgr / 'MsnMsgs.msi'))
				if v[0] >= 14:
					outdir_contacts = outdir / 'contacts'
					outdir_contacts.mkdir(parents = True)
					
					contactsfile = DIR_INPUT / 'msn/contacts/contacts-{}.msi'.format(vs)
					if not contactsfile.exists(): assert False
					shutil.copy(str(contactsfile), str(outdir_contacts / 'Contacts.msi'))
			else:
				assert False
		elif program_name == 'yahoo':
			try:
				exefile = DIR_INPUT / 'yahoo/{}.exe'.format(version_name)
				e_wise = abspath('e_wise/E_WISE_W.EXE')
				subprocess.run([e_wise, abspath(str(exefile)), abspath(str(outdir))], check = True, stdout = subprocess.PIPE)
				
				batfile = outdir / '00000000.BAT'
				os.chdir(outdir)
				subprocess.run(['cmd.exe', '/C', abspath(str(batfile))], check = True, stdout = subprocess.PIPE)
				os.remove(batfile)
				os.chdir(here)
			except KeyboardInterrupt:
				pass
			except:
				print('Could not be extracted - program might have to be manually patched')
				raise
		else:
			assert False
	except:
		shutil.rmtree(str(outdir))
		raise

# MSN

def extract_msi(name):
	outdir = DIR_VERSIONS / 'msn' / name / 'msi'
	if outdir.exists(): return
	outdir.mkdir(parents = True)
	
	here = abspath('.')
	
	try:
		msi2xml = abspath('msi2xml/msi2xml.exe')
		msi = DIR_VERSIONS / 'msn' / name / 'extracted/messenger/MsnMsgs.msi'
		if not msi.exists():
			# Some MSN installers store the MSI as `Messenger.msi`
			msi = DIR_VERSIONS / 'msn' / name / 'extracted/messenger/Messenger.msi'
		msi = str(msi)
		
		outdir_msgr = outdir / 'messenger'
		outdir_msgr.mkdir(parents = True)
		os.chdir(str(outdir_msgr))
		subprocess.check_call([
			msi2xml, '-q', '-b', 'streams', '-c', 'files',
			'-o', 'MsnMsgs.xml', msi
		])
		
		v, _, _ = parse_name(name)
		
		if v[0] >= 14:
			contacts = str(DIR_VERSIONS / 'msn' / name / 'extracted/contacts/Contacts.msi')
			
			outdir_contacts = outdir / 'contacts'
			outdir_contacts.mkdir(parents = True)
			os.chdir(str(outdir_contacts))
			subprocess.check_call([
				msi2xml, '-q', '-b', 'streams', '-c', 'files',
				'-o', 'Contacts.xml', contacts
			])
	except:
		shutil.rmtree(str(outdir))
		raise
	finally:
		os.chdir(here)

def patch_extracted_msi(name):
	msi_product_code = None
	contacts_product_code = None
	
	outdir = DIR_VERSIONS / 'msn' / name / 'msi-patched'
	if outdir.exists():
		return
	shutil.copytree(str(DIR_VERSIONS / 'msn' / name / 'msi'), str(outdir))
	
	try:
		msnmsgr_name = None
		msnmsgr_dir = None
		msnmsgr_filename = None
		
		contacts_name = None
		
		msi_xml = outdir / 'messenger/MsnMsgs.xml'
		msi_xml_root = etree.parse(str(msi_xml))
		
		# Get product code first
		msi_product_code = get_msi_product_code_from_xml(msi_xml_root)
		assert msi_product_code is not None
		
		msnmsgr_elm = msi_xml_root.find('/table[@name="Component"]')
		assert msnmsgr_elm is not None
		msnmsgr_rows = msnmsgr_elm.findall('row')
		assert msnmsgr_rows is not None
		
		for msnmsgr_row in msnmsgr_rows:
			msnmsgr_component_id = msnmsgr_row[0].text
			assert msnmsgr_component_id is not None
			if msnmsgr_component_id.startswith('MsgrCoreExeComponent'):
				msnmsgr_name = msnmsgr_row[5].text
				msnmsgr_dir = msnmsgr_row[2].text
				break
		assert msnmsgr_name is not None and msnmsgr_dir is not None
		
		file_elm = msi_xml_root.find('/table[@name="File"]')
		assert file_elm is not None
		file_rows = file_elm.findall('row')
		assert file_rows is not None
		
		for file_row in file_rows:
			file_name = file_row[0].text
			if file_name == msnmsgr_name:
				msnmsgr_row = file_row
				msnmsgr_filename = get_full_filename_msi_xml(file_row[2].text)
				break
		assert msnmsgr_filename is not None
		
		msi_files = outdir / 'messenger/files'
		
		v, _, _ = parse_name(name)
		msn = msi_files / msnmsgr_name
		assert msn.exists()
		
		with msn.open('rb') as fh:
			msn_content = fh.read()
		msn_content = append_import(msn_content, PATCH_DLL.encode('utf-8'), PATCH_DLL_FUNC.encode('utf-8'))
		
		with msn.open('wb') as fh:
			fh.write(msn_content)
		
		msnmsgr_row[0].set('md5', hashlib.md5(msn_content).hexdigest().lower())
		msnmsgr_row[3].text = str(len(msn_content))
		
		if v[0] >= 5:
			add_switcher_to_msi_files_xml(msi_xml_root, msi_files, msnmsgr_filename, 'MsgrFeat', msnmsgr_dir)
			with msi_xml.open('wb') as fh:
				fh.write(etree.tostring(msi_xml_root))
		
		if v[0] >= 14:
			contacts_xml = outdir / 'contacts/Contacts.xml'
			contacts_xml_root = etree.parse(str(contacts_xml))
			
			contacts_product_code = get_msi_product_code_from_xml(contacts_xml_root)
			assert contacts_product_code is not None
			
			contacts_elm = contacts_xml_root.find('/table[@name="Component"]')
			assert contacts_elm is not None
			contacts_rows = contacts_elm.findall('row')
			assert contacts_rows is not None
			
			for contacts_row in contacts_rows:
				wlcomm_component_id = contacts_row[0].text
				if wlcomm_component_id == 'WLComm':
					wlcomm_name = contacts_row[5].text
					break
			assert wlcomm_name is not None
			
			contacts_file_elm = contacts_xml_root.find('/table[@name="File"]')
			assert contacts_file_elm is not None
			contacts_file_rows = contacts_file_elm.findall('row')
			assert contacts_file_rows is not None
			
			for contacts_file_row in contacts_file_rows:
				contacts_file_name = contacts_file_row[0].text
				if contacts_file_name == wlcomm_name:
					wlcomm_row = contacts_file_row
					wlcomm_filename = get_full_filename_msi_xml(wlcomm_row[2].text)
					break
			assert wlcomm_filename is not None
			
			contacts_files = outdir / 'contacts/files'
			
			wlcomm = contacts_files / wlcomm_name
			assert wlcomm.exists()
			
			with wlcomm.open('rb') as fh:
				wlcomm_content = fh.read()
			wlcomm_content = append_import(wlcomm_content, PATCH_DLL.encode('utf-8'), PATCH_DLL_FUNC.encode('utf-8'))
			
			with wlcomm.open('wb') as fh:
				fh.write(wlcomm_content)
			
			wlcomm_row[0].set('md5', hashlib.md5(wlcomm_content).hexdigest().lower())
			wlcomm_row[3].text = str(len(wlcomm_content))
			
			add_switcher_to_msi_files_xml(contacts_xml_root, contacts_files, wlcomm_filename, 'ContactEngine', 'ContactDir')
			with contacts_xml.open('wb') as fh:
				fh.write(etree.tostring(contacts_xml_root))
	except:
		shutil.rmtree(str(outdir))
		raise
	finally:
		return msi_product_code, contacts_product_code

def pack_patched_msi(name, product_code_tpl):
	v, _, vs = parse_name(name)
	if product_code_tpl is None: return
	
	if v[0] >= 14:
		outdir = DIR_VERSIONS / 'msn' / name / 'msi-packed'
		if outdir.exists():
			return
	else:
		outdir = DIR_FINAL / 'msn'
	
	patched_name = 'escargot-{}'.format(name)
	outfile = outdir / '{}.msi'.format('Messenger' if v[0] >= 14 else patched_name)
	if outfile.exists():
		return
	
	if v[0] >= 14:
		# Copy other components to build folder for WLM 14+ first due to copytree limitations (returns error if target folder already exists)
		shutil.copytree(str(DIR_INPUT / 'msn/misc' / str(v[0])), str(outdir))
	
	xml2msi = abspath('msi2xml/xml2msi.exe')
	xml = str(DIR_VERSIONS / 'msn/{}/msi-patched/messenger/MsnMsgs.xml'.format(name))
	
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
	
	if v[0] < 14:
		return
	
	outfile_contacts = outdir / 'Contacts.msi'
	if outfile_contacts.exists():
		return
	
	contacts_xml = str(DIR_VERSIONS / 'msn/{}/msi-patched/contacts/Contacts.xml'.format(name))
	
	subprocess.call([
		xml2msi, '-q', '-m',
		#'-d', product_version_guid, # --product-code
		#'-g', product_guid, # --upgrade-code
		'-o', str(outfile_contacts),
		contacts_xml
	])
	
	msi_product_code, contacts_product_code = product_code_tpl
	with open(DIR_INSTALLER / 'msn/script/wlm14-installer.nsi', 'r') as fh:
		nsi_content = fh.read()
	
	nsi_content = nsi_content.format(
		outfile = str(outdir / '{}.exe'.format(patched_name)), base_name = name[:name.rfind('-')],
		welcomefinish_bitmap = str(DIR_INSTALLER / 'msn/assets/banner.bmp'),
		msi_product_code = msi_product_code, wlcomm_product_code = contacts_product_code,
		version_string = vs,
	)
	
	installer_script = outdir / 'installer.nsi'
	with open(installer_script, 'w') as fh:
		fh.write(nsi_content)
	
	subprocess.check_call([
		'makensis.exe', str(installer_script)
	])

# Yahoo! Messenger

def patch_yahoo_files(name):
	outdir = DIR_VERSIONS / 'yahoo' / name / 'patched'
	if outdir.exists():
		return
	shutil.copytree(str(DIR_VERSIONS / 'yahoo' / name / 'extracted'), str(outdir))
	
	maindir = outdir / 'MAINDIR'
	if not maindir.exists(): return
	
	shutil.copyfile(PATCH_DLL, str(maindir / 'escargot.dll'))
	
	with open('escargot.ini', 'r') as fh:
		ini_content = fh.read()
	ini_content = ini_content.format(type = 'yahoo')
	
	with open(maindir / 'YPager.exe-escargot.ini', 'w') as fh:
		fh.write(ini_content)
	
	ypager = maindir / 'YPager.exe'
	assert ypager.exists()
	
	with ypager.open('rb') as fh:
		ypager_content = fh.read()
	ypager_content = append_import(ypager_content, PATCH_DLL.encode('utf-8'), PATCH_DLL_FUNC.encode('utf-8'))
	
	with ypager.open('wb') as fh:
		fh.write(ypager_content)

def pack_patched_yahoo(name):
	v, _, _ = parse_name(name)
	
	patched = DIR_VERSIONS / 'yahoo' / name / 'patched'
	if not patched.exists(): return
	outdir = DIR_FINAL / 'yahoo'
	if not outdir.exists():
		outdir.mkdir()
	
	version = '.'.join(map(str, v[:2]))
	
	patched_exe = outdir / '{}.exe'.format('escargot-{}'.format(name))
	if patched_exe.exists():
		return
	
	with open(DIR_INSTALLER / 'yahoo/script/installer-{}.nsi'.format(version), 'r') as fh:
		nsi_content = fh.read()
	
	nsi_content = nsi_content.format(
		outfile = str(patched_exe),
	)
	
	installer_script = patched / 'installer.nsi'
	with open(installer_script, 'w') as fh:
		fh.write(nsi_content)
	
	subprocess.check_call([
		'makensis.exe', str(installer_script)
	])

# msi2xml XML helper functions

def get_msi_product_code_from_xml(xml_root):
	property_elm = xml_root.find('/table[@name="Property"]')
	if property_elm is None: return None
	property_rows = property_elm.findall('row')
	if property_rows is None: return None
	
	for property_row in property_rows:
		property_name = property_row[0].text
		if property_name == 'ProductCode':
			return property_row[1].text

def add_switcher_to_msi_files_xml(xml_root, msi_files, ini_filename, feature_type, msi_directory):
	switcher_dll = msi_files / 'escargotdll'
	switcher_ini_configured = msi_files / 'escargotini'
	
	shutil.copyfile(PATCH_DLL, str(switcher_dll))
	
	with open('escargot.ini', 'r') as fh:
		ini_content = fh.read()
	
	ini_content = ini_content.format(type = 'msn')
	
	with open(switcher_ini_configured, 'w') as fh:
		fh.write(ini_content)
	
	# TODO: Change GUIDs and possibly component names when possible - these two are just for testing
	add_file_to_msi_xml(xml_root, 'EscargotSwitcherComponentMain', feature_type, msi_directory, '{B06C425B-066E-4C57-9EB9-6FA297FD7CE0}', switcher_dll, PATCH_DLL)
	add_file_to_msi_xml(xml_root, 'EscargotSwitcherComponentConfig', feature_type, msi_directory, '{46A8EA19-AE19-42DD-B78F-9FEB1B76807A}', switcher_ini_configured, 'escargot.ini|{}-escargot.ini'.format(ini_filename))
	
	msifilehash = find_msifilehash_table(xml_root)
	assert msifilehash is not None
	# We don't need to worry about generating our own MSI hash for the INI, just supplies `0`s
	msifilehash.append(create_generic_msi_xml_row('escargotini', '0', '0', '0', '0', '0'))

def find_msifilehash_table(xml_root):
	msifilehash = xml_root.find('/table[@name="MsiFileHash"]')
	if msifilehash is None:
		# Create new `MSIFileHash` table and store it in root of XML
		msifilehash = etree.fromstring(MSIFILEHASH_TABLE_XML)
		
		xml_root.getroot().append(msifilehash)
	return msifilehash

def add_file_to_msi_xml(root, component_name, feature_type, msi_directory, guid, component_path, filename):
	media_elm = root.find('/table[@name="Media"]/row')
	assert media_elm is not None
	sequence_new = str(int(media_elm[1].text) + 1)
	
	component_elm = root.find('/table[@name="Component"]')
	assert component_elm is not None
	component_elm.append(create_generic_msi_xml_row(component_name, guid, msi_directory, '0', None, component_path.name))
	featurecomponents_elm = root.find('/table[@name="FeatureComponents"]')
	assert featurecomponents_elm is not None
	featurecomponents_elm.append(create_generic_msi_xml_row(feature_type, component_name))
	
	file_elm = root.find('/table[@name="File"]')
	assert file_elm is not None
	file_elm.append(create_file_msi_xml_row(component_path, component_name, filename, sequence_new))
	
	media_elm[1].text = sequence_new

def create_generic_msi_xml_row(*args):
	root = etree.Element('row')
	for arg in args:
		root.append(create_basic_xml_element('td', arg))
	return root

def create_file_msi_xml_row(file_path, component_name, filename, sequence):
	root = etree.Element('row')
	file_arg = etree.Element('td')
	file_arg.set('href', 'files/{}'.format(file_path.name))
	
	with file_path.open('rb') as fh:
		file_content = fh.read()
	file_arg.set('md5', hashlib.md5(file_content).hexdigest().lower())
	file_arg.text = file_path.name
	root.append(file_arg)
	
	root.append(create_basic_xml_element('td', component_name))
	root.append(create_basic_xml_element('td', filename))
	root.append(create_basic_xml_element('td', str(len(file_content))))
	root.append(create_basic_xml_element('td', None))
	root.append(create_basic_xml_element('td', None))
	root.append(create_basic_xml_element('td', '0'))
	root.append(create_basic_xml_element('td', sequence))
	return root

# General XML helper functions

def create_basic_xml_element(name, text):
	tmp = etree.Element(name)
	tmp.text = text
	
	return tmp

def get_full_filename_msi_xml(filename):
	if '|' in filename:
		# Filename defines both short-hand and long file names. Get long file name only
		return filename.split('|', 1)[1]
	return filename

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

# Helper functions

def parse_name(name):
	m = re.search(r'-(\d+(?:\.\d+)*)-(.+)$', name)
	if not m:
		raise Exception("can't parse name `{}`".format(name))
	vs = m.group(1)
	v = tuple(map(int, vs.split('.')))
	l = m.group(2)
	return v, l, vs

MSIFILEHASH_TABLE_XML = '''<table name="MsiFileHash">
	<col key="yes" def="s72">File_</col>
	<col def="i2">Options</col>
	<col def="i4">HashPart1</col>
	<col def="i4">HashPart2</col>
	<col def="i4">HashPart3</col>
	<col def="i4">HashPart4</col>
</table>'''

if __name__ == '__main__':
	main()
