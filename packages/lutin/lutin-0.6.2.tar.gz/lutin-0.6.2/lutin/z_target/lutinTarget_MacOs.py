#!/usr/bin/python
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license APACHE v2.0 (see license file)
##

from lutin import debug
from lutin import target
from lutin import tools
from lutin import host
from lutin import multiprocess
import os
import stat
import shutil

class Target(target.Target):
	def __init__(self, config):
		#processor type selection (auto/arm/ppc/x86)
		if config["arch"] == "auto":
			config["arch"] = "x86"
		#bus size selection (auto/32/64)
		if config["bus-size"] == "auto":
			config["bus-size"] = str(host.BUS_SIZE)
		# http://biolpc22.york.ac.uk/pub/linux-mac-cross/
		# http://devs.openttd.org/~truebrain/compile-farm/apple-darwin9.txt
		target.Target.__init__(self, "MacOs", config, "")
		
		self.folder_bin="/MacOS"
		self.folder_lib="/lib"
		self.folder_data="/Resources"
		self.folder_doc="/doc"
		
		self.suffix_lib_static='.a'
		self.suffix_lib_dynamic='.dylib'
		self.suffix_binary=''
		self.suffix_package=''
		
		self.global_flags_cc.append("-D__STDCPP_LLVM__")
		
	
	def get_staging_folder(self, binaryName):
		return tools.get_run_folder() + self.folder_out + self.folder_staging + "/" + binaryName + ".app/Contents/"
	
	def get_staging_folder_data(self, binaryName):
		return self.get_staging_folder(binaryName) + self.folder_data + "/"
	
	def make_package(self, pkgName, pkgProperties, basePkgPath):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Generate package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		
		if    "ICON" in pkgProperties.keys() \
		   and pkgProperties["ICON"] != "":
			tools.copy_file(pkgProperties["ICON"], self.get_staging_folder_data(pkgName) + "/icon.icns", force=True)
		
		# http://www.sandroid.org/imcross/#Deployment
		infoFile=self.get_staging_folder(pkgName) + "/Info.plist"
		# Create the info file
		tmpFile = open(infoFile, 'w')
		tmpFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
		tmpFile.write("<!DOCTYPE plist PUBLIC \"-//Apple Computer//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n")
		tmpFile.write("<plist version=\"1.0\">\n")
		tmpFile.write("    <dict>\n")
		tmpFile.write("        <key>CFBundleExecutableFile</key>\n")
		tmpFile.write("        <string>"+pkgName+"</string>\n")
		tmpFile.write("        <key>CFBundleName</key>\n")
		tmpFile.write("        <string>"+pkgName+"</string>\n")
		tmpFile.write("        <key>CFBundleIdentifier</key>\n")
		tmpFile.write("        <string>" + pkgProperties["COMPAGNY_TYPE"] + "." + pkgProperties["COMPAGNY_NAME2"] + "." + pkgName + "</string>\n")
		tmpFile.write("        <key>CFBundleSignature</key>\n")
		tmpFile.write("        <string>????</string>\n")
		tmpFile.write("        <key>CFBundleIconFile</key>\n")
		tmpFile.write("        <string>icon.icns</string>\n")
		tmpFile.write("    </dict>\n")
		tmpFile.write("</plist>\n")
		tmpFile.write("\n\n")
		tmpFile.flush()
		tmpFile.close()
		infoFile=self.get_staging_folder(pkgName) + "/PkgInfo"
		# Create the info file
		tmpFile = open(infoFile, 'w')
		tmpFile.write("APPL????")
		tmpFile.flush()
		tmpFile.close()
		
		# Create a simple interface to localy install the aplication for the shell (a shell command line interface)
		shell_file_name=self.get_staging_folder(pkgName) + "/shell/" + pkgName
		# Create the info file
		tools.create_directory_of_file(shell_file_name)
		tmpFile = open(shell_file_name, 'w')
		tmpFile.write("#!/bin/bash\n")
		tmpFile.write("# Simply open the real application in the correct way (a link does not work ...)\n")
		tmpFile.write("/Applications/" + pkgName + ".app/Contents/MacOS/" + pkgName + " $*\n")
		#tmpFile.write("open -n /Applications/edn.app --args -AppCommandLineArg $*\n")
		tmpFile.flush()
		tmpFile.close()
		
		
		# Must create the disk image of the application 
		debug.info("Generate disk image for '" + pkgName + "'")
		output_file_name = self.get_final_folder() + "/" + pkgName + ".dmg"
		cmd = "hdiutil create -volname "
		cmd += pkgName + " -srcfolder "
		cmd += tools.get_run_folder() + self.folder_out + self.folder_staging + "/" + pkgName + ".app"
		cmd += " -ov -format UDZO "
		cmd += output_file_name
		tools.create_directory_of_file(output_file_name)
		multiprocess.run_command_direct(cmd)
		debug.info("disk image: " + output_file_name)
		
		debug.info("You can have an shell interface by executing : ")
		debug.info("    sudo cp " + shell_file_name + " /usr/local/bin")
	
	def install_package(self, pkgName):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Install package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		debug.info("copy " + tools.get_run_folder() + self.folder_out + self.folder_staging + "/" + pkgName + ".app in /Applications/")
		if os.path.exists("/Applications/" + pkgName + ".app") == True:
			shutil.rmtree("/Applications/" + pkgName + ".app")
		# copy the application in the basic application folder : /Applications/xxx.app
		shutil.copytree(tools.get_run_folder() + self.folder_out + self.folder_staging + "/" + pkgName + ".app", "/Applications/" + pkgName + ".app")
	
	def un_install_package(self, pkgName):
		debug.debug("------------------------------------------------------------------------")
		debug.info("Un-Install package '" + pkgName + "'")
		debug.debug("------------------------------------------------------------------------")
		debug.info("remove OLD application /Applications/" + pkgName + ".app")
		# Remove the application in the basic application folder : /Applications/xxx.app
		if os.path.exists("/Applications/" + pkgName + ".app") == True:
			shutil.rmtree("/Applications/" + pkgName + ".app")




