from struct import unpack, pack

def append_import(data: bytes, new_dll_name: bytes, import_func: bytes) -> bytes:
	data_raw = data
	
	assert data[:2] == b'\x4d\x5a'
	h_dos = data[:64]
	ptr_pe = unpack('<I', h_dos[-4:])[0]
	
	h_pe = data[ptr_pe:ptr_pe+0x78]
	sec_align = unpack('<I', h_pe[0x38:0x38+4])[0]
	fil_align = unpack('<I', h_pe[0x38+4:0x38+8])[0]
	#print("Align:", sec_align, fil_align)
	size_init_data = unpack('<I', h_pe[0x20:0x24])[0]
	size_img = unpack('<I', h_pe[0x50:0x54])[0]
	data = data[ptr_pe+0x78:]
	assert h_pe[:4] == b'\x50\x45\x00\x00'
	machine = h_pe[4:6]
	num_sec = unpack('<H', h_pe[6:8])[0]
	#print("Machine/Sections/Checksum:", machine, num_sec, unpack('<I', h_pe[0x58:0x58+4])[0])
	assert h_pe[0x4C:0x50] == b'\0' * 4
	assert h_pe[0x70:0x74] == b'\0' * 4
	n_rva = unpack('<I', h_pe[0x74:0x78])[0]
	
	data_dirs = data[:8*16]
	data = data[8*16:]
	assert data_dirs[4*17:4*17+4] == b'\0' * 4
	assert data_dirs[-8:] == b'\0' * 8
	
	rva_impt = unpack('<I', data_dirs[8:12])[0]
	siz_imp = unpack('<I', data_dirs[12:16])[0]
	#print("Import RVA/Size:", rva_impt, siz_imp)
	
	sections = data[:40*num_sec]
	
	first_sec_data_offset = None
	max_virtual = 0
	base_import = None
	for s in split_by_length(sections, 40):
		name, vsize, vaddr, rsize, raddr, p2r, p2l, nr, nl, chars = unpack('<8sIIIIIIHHI', s)
		max_virtual = max(vsize + vaddr, max_virtual)
		if first_sec_data_offset is None or raddr < first_sec_data_offset:
			first_sec_data_offset = raddr
		if vaddr <= rva_impt < vaddr + rsize:
			base_import = raddr + (rva_impt - vaddr)
	
	import_data = data_raw[base_import:base_import+siz_imp]
	
	free_offset = ptr_pe + len(h_pe + data_dirs + sections)
	assert first_sec_data_offset - free_offset >= 100
	assert set(data_raw[free_offset:first_sec_data_offset]) == { 0 }
	
	# Pad to align
	max_virtual += ((sec_align - (max_virtual % sec_align)) % sec_align)
	pad_len = ((sec_align - (len(data_raw) % sec_align)) % sec_align)
	new_section_raw_offset = len(data_raw) + pad_len
	
	new_section = pack('<8sIIIIIIHHI',
		b'.scrgt\0\0', 0x1000, max_virtual, 0x1000, new_section_raw_offset, 0, 0, 0, 0, 0xC0000040
	)
	
	new_imp_desc_rva_base = max_virtual + len(import_data) + 20
	new_import_desc = pack('<IIIII',
		new_imp_desc_rva_base + len(new_dll_name) + 1,
		0, 0, new_imp_desc_rva_base,
		new_imp_desc_rva_base + len(new_dll_name) + 1 + 8,
	)
	new_import_data = import_data[:-20] + new_import_desc + (b'\0'*20)
	extra = new_dll_name + b'\0' + (
		pack('<II', new_imp_desc_rva_base + len(new_dll_name) + 1 + 16, 0)
		+ pack('<II', new_imp_desc_rva_base + len(new_dll_name) + 1 + 16, 0)
		+ b'\0\0' + import_func + b'\0'
	)
	
	# Increment num_sec by 1
	data_raw = replace(data_raw, ptr_pe+6, pack('<H', num_sec + 1))
	# Patch new import table RVA
	data_raw = replace(data_raw, ptr_pe+0x78+8, pack('<I', max_virtual))
	# Patch new import table size
	data_raw = replace(data_raw, ptr_pe+0x78+12, pack('<I', siz_imp+20))
	# Patch size_init_data/size_img
	# This doesn't seem to be necessary
	#data_raw = replace(data_raw, ptr_pe+0x20, pack('<I', size_init_data+3*4096))
	data_raw = replace(data_raw, ptr_pe+0x50, pack('<I', size_img+4096))
	# New section header
	data_raw = replace(data_raw, free_offset, new_section)
	# New section data
	data_raw += b'\0'*pad_len
	data_raw += new_import_data + extra + b'\0' * (0x1000 - len(new_import_data) - len(extra))
	
	return data_raw

def split_by_length(data, n):
	assert len(data) % n == 0
	for i in range(len(data) // n):
		yield data[i*n:(i+1)*n]

def replace(data, offset, newdata):
	return data[:offset] + newdata + data[offset+len(newdata):]
