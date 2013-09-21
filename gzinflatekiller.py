#!/bin/env python
#:############################################
#:	GZINFLATEKILLER
#:	by Les Cordell
#:	
#:	Hunt through files containing a base64
#:	GZInflate Command
#:
#:	Written on 07/08/2013
#:	last modified @ 07/08/2013
#:############################################
import sys, os, re

#: Extensions constant, these are the files that our program will check
EXTS = ['php']
#: Our Patterns constant contains all of our regular expressions that we want to check against and skip
PATTERNS = [re.compile("<\?php eval\(gzinflate\(base64_decode\(\'.*\'\)\)\);\?>"), re.compile('^\r\n')]


def gzInflateKill():
	"""
	#: The main function that is run, it checks through the argv arguements first,
	#: it requires a directory enclosed in quotes.
	"""
	dirname = False

	#: Check provided directory name
	if (len(sys.argv) < 2):
		print "You must provide a directory name enclosed in quotes to run this script.\n"
		quit()
	elif (len(sys.argv) > 2):
		print "Too many arguements provided, you must provide a directory for this script to run"
		quit()
	elif (len(sys.argv) == 2):
		#: Store the directory name
		dirname = sys.argv[1]
	else:
		#: If there is an error return false
		print "There was an error running this script, please check that you have specified a directory enclosed in quotes."
		quit()

	#: Open the directory
	parseDir(dirname)
	quit()


def parseDir(dirname):
	"""
	#: This is our directory parser, here we parse through every directory until we hit the last
	#: feeding the files off to the cleanFile function
	"""
	if os.path.exists(dirname):
		#: If our directory exists then we'll open it and return some files
		#: Walk through the directory
		for root, dirs, files in os.walk(dirname):
			if files: #: If we get any files
				for file in files: #: For each file in the list
					if file.split('.')[-1] in EXTS: #: Get the extension
						thisFile = os.path.join(root, file)
						if os.path.isfile(thisFile):
							print "cleaning: " + thisFile
							cleanFile(thisFile)

			if dirs: #: If we get any directories
				for dir in dirs: #: For each directory in the list
						parseDir(dir);	#: Recursively run the function
		

def cleanFile(filename):
	"""
	#: Here we will strip the injection from the php file
	"""
	newFile = []
	#: First open the file for reading and get our new file
	with open(filename, 'r') as aFile:
		for line in aFile.readlines():
			#: For each line check if it matches the injection or the new line
			if patternMatch(line):
				pass
			else: 			   #: Append line to new file if no match
				newFile.append(line)
			aFile.close()	   #: close the file
	
	#: Now we open the file for reading
	if newFile:
		newFile = ''.join(newFile) # : join our new file
		with open(filename, 'w+b') as aFile:
			aFile.write(newFile)
			aFile.close()

def patternMatch(line):
	"""
	#: We pass lines into this function, check them against our PATTERNS constant
	#: if we match any of them, we return a true, otherwise we return false
	"""
	for pattern in PATTERNS:
		if pattern.match(line):
			return True

	return False

# BEGIN #
if __name__ == '__main__':
	gzInflateKill();
