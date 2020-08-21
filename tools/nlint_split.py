
import os
import sys
import re
import shutil

# input order handle
din = sys.argv
if len(din) != 3:
	raise ValueError("Error:wrong input parameter,should be `python3 split_nlint.py <log path> <rtl root>`")

# check log path
log_path = din[1]
if not os.path.exists(log_path):
	raise ValueError("Error:log %s not exists" % log_path)
rtl_root = din[2]
if not os.path.exists(rtl_root):
	raise ValueError("Error:rtl %s not exists" % rtl_root)

# prepare output dir
log_root = os.path.split(log_path)[0]
dout_root = os.path.join(log_root,"nlint_analysis")
if os.path.exists(dout_root):
	# os.removedirs(dout_root)
	shutil.rmtree(dout_root)
os.mkdir(dout_root)

# read log
with open(log_path,'r') as f:
	data = [[i.strip() for i in x.split(":")] for x in f.readlines() if ":" in x]
# print(data[:-5])

# handle
result = {}
for i in data:
	fname,etype,esource = i[0],i[1],":".join(i[2:])
	file_name = os.path.splitext(os.path.split(fname)[1])[0]
	line = fname.split("(")[1].replace(")","")
	error_type = etype.split(" ")[0].strip()
	esource = "%s:%s" % (line,esource)
	# print(file_name,error_type,error_source)
	# break
	if result.get(file_name) is None:
		result[file_name] = {error_type:[esource]}
	elif result[file_name].get(error_type) is None:
		result[file_name][error_type] = [esource]
	else:
		result[file_name][error_type].append(esource)

# save and back
for name in result.keys():
	
	file_root = os.path.join(dout_root,name)
	rtl_path = os.path.join(rtl_root,"%s.v" % name)
	rtl_tmp = {}

	os.mkdir(file_root)
	for etype in result[name].keys():
		type_root = os.path.join(file_root,"%s.log" % etype)
		with open(type_root,'w') as f:
			f.write("\n".join(result[name][etype]))
		print("Info:write %s of file %s finish" % (etype,name))
		for im in result[name][etype]:
			im_line,im_info = im.split(":",1)
			if rtl_tmp.get(im_line) is not None:
				rtl_tmp[im_line][0] = 1
			else:
				rtl_tmp[im_line] = [0,im_info]

	with open(rtl_path,'r') as f:
		rtl_content = f.read().split("\n")
	for i in range(len(rtl_content)):
		rtl_content[i] = re.sub(r"//nLint.*$",'',rtl_content[i])

	for rtl_line in rtl_tmp.keys():
		if rtl_tmp[rtl_line][0] == 1:
			im = "//nLint (More than 1) %s" % rtl_tmp[rtl_line][1]
		else:
			im = "//nLint %s" % rtl_tmp[rtl_line][1]
		rtl_content[int(rtl_line) - 1] += im
	with open(rtl_path,'w') as f:
	# with open(os.path.join(file_root,"%s.v" % name),'w') as f:
		f.write("\n".join(rtl_content))
	print("Info:Back to %s finish" % name)
		# pass
	# print(name)
	# pass
# print(result)