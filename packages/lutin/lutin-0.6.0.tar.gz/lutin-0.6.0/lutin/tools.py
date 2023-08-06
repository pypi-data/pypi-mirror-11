#!/usr/bin/python
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

import os
import shutil
import errno
import fnmatch
# Local import
from . import debug
from . import depend
import multiprocess

"""
	
"""
def get_run_folder():
	return os.getcwd()

"""
	
"""
def get_current_path(file):
	return os.path.dirname(os.path.realpath(file))

def create_directory_of_file(file):
	folder = os.path.dirname(file)
	try:
		os.stat(folder)
	except:
		os.makedirs(folder)

def get_list_sub_folder(path):
	# TODO : os.listdir(path)
	for dirname, dirnames, filenames in os.walk(path):
		return dirnames
	return []

def remove_folder_and_sub_folder(path):
	if os.path.isdir(path):
		debug.verbose("remove folder : '" + path + "'")
		shutil.rmtree(path)

def remove_file(path):
	if os.path.isfile(path):
		os.remove(path)

def file_size(path):
	if not os.path.isfile(path):
		return 0
	statinfo = os.stat(path)
	return statinfo.st_size

def file_read_data(path, binary=False):
	if not os.path.isfile(path):
		return ""
	if binary == True:
		file = open(path, "rb")
	else:
		file = open(path, "r")
	data_file = file.read()
	file.close()
	return data_file

def file_write_data(path, data):
	file = open(path, "w")
	file.write(data)
	file.close()

def list_to_str(list):
	if type(list) == type(str()):
		return list + " "
	else:
		result = ""
		# mulyiple imput in the list ...
		for elem in list:
			result += list_to_str(elem)
		return result

def add_prefix(prefix,list):
	if type(list) == type(None):
		return ""
	if type(list) == type(str()):
		return prefix+list
	else:
		if len(list)==0:
			return ''
		else:
			result=[]
			for elem in list:
				result.append(prefix+elem)
			return result

def copy_file(src, dst, cmd_file=None, force=False):
	if os.path.exists(src) == False:
		debug.error("Request a copy a file that does not existed : '" + src + "'")
	cmd_line = "copy \"" + src + "\" \"" + dst + "\""
	if     force == False \
	   and depend.need_re_build(dst, src, file_cmd=cmd_file , cmdLine=cmd_line) == False:
		return
	debug.print_element("copy file", src, "==>", dst)
	create_directory_of_file(dst)
	shutil.copyfile(src, dst)
	multiprocess.store_command(cmd_line, cmd_file)


def copy_anything(src, dst):
	tmpPath = os.path.dirname(os.path.realpath(src))
	tmpRule = os.path.basename(src)
	for root, dirnames, filenames in os.walk(tmpPath):
		debug.verbose(" root='" + str(root) + "' dir='" + str(dirnames) + "' filenames=" + str(filenames))
		tmpList = filenames
		if len(tmpRule)>0:
			tmpList = fnmatch.filter(filenames, tmpRule)
		# Import the module :
		for cycleFile in tmpList:
			#for cycleFile in filenames:
			debug.verbose("Might copy : '" + tmpPath+cycleFile + "' ==> '" + dst + "'")
			copy_file(tmpPath+"/"+cycleFile, dst+"/"+cycleFile)


def copy_anything_target(target, src, dst):
	tmpPath = os.path.dirname(os.path.realpath(src))
	tmpRule = os.path.basename(src)
	for root, dirnames, filenames in os.walk(tmpPath):
		debug.verbose(" root='" + str(root) + "' dir='" + str(dirnames) + "' filenames=" + str(filenames))
		tmpList = filenames
		if len(tmpRule)>0:
			tmpList = fnmatch.filter(filenames, tmpRule)
		# Import the module :
		for cycleFile in tmpList:
			#for cycleFile in filenames:
			newDst = dst
			if len(newDst) != 0 and newDst[-1] != "/":
				newDst += "/"
			if root[len(src)-1:] != "":
				newDst += root[len(src)-1:]
				if len(newDst) != 0 and newDst[-1] != "/":
					newDst += "/"
			debug.verbose("Might copy : '" + root+"/"+cycleFile + "' ==> '" + newDst+cycleFile + "'" )
			target.add_file_staging(root+"/"+cycleFile, newDst+cycleFile)


def filter_extention(list_files, extentions, invert=False):
	out = []
	for file in list_files:
		in_list = False
		for ext in extentions:
			if file[-len(ext):] == ext:
				in_list = True
		if     in_list == True \
		   and invert == False:
			out.append(file)
		elif     in_list == False \
		     and invert == True:
			out.append(file)
	return out


def move_if_needed(src, dst):
	if not os.path.isfile(src):
		debug.error("request move if needed, but file does not exist: '" + str(src) + "' to '" + str(dst) + "'")
		return
	src_data = file_read_data(src)
	if os.path.isfile(dst):
		# file exist ==> must check ...
		dst_data = file_read_data(dst)
		if src_data == dst_data:
			# nothing to do ...
			return
	file_write_data(dst, src_data)
	remove_file(src)



