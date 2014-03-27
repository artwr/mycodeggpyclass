#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# This code was modified by Arthur Wiedmer. The original code is available 
# from the Google's Python Class website listed above.

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def get_special_paths(dir): 
  """ returns a list of the absolute paths 
  of the special files in the given directory """
  filenames = os.listdir(dir)
  specialfiles = []
  for filename in filenames:
    match =re.search(r".*__\w+__.*", filename)
    if match:
      specialfiles.append(os.path.abspath(os.path.join(dir, filename)))
      # print os.path.abspath(os.path.join(dir, filename))
  return specialfiles

def check_duplicates(pathlist):
  filenames = [os.path.basename(x) for x in pathlist]
  return len(filenames) != len(set(filenames))
  
    
def copy_to(paths, dir):
  """ given a list of paths, copies those files into the given directory """
  if not os.path.exists(dir):
    os.makedirs(dir)
  for path in paths:
    shutil.copy(path, dir)
  return
    
def zip_to(paths, zippath):
  """ given a list of paths, zip those files up into the given zipfile """
  cmd = 'zip -j ' + zippath + ' ' + ' '.join(paths)
  print "Command to run:", cmd
  # if not os.path.exists(os.path.dirname(zippath)):
  #   sys.stderr.write("Error. Path to zip file: \n" + os.path.dirname(zippath) + "\n does not exists")
  (status, output) = commands.getstatusoutput(cmd)
  if status:    ## Error case, print the command's output to stderr and exit
    sys.stderr.write(output)
    sys.stderr.write('\n')
    sys.exit(1)    
  return

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  specialpaths = []
  for filename in args:
    specialpaths.extend(get_special_paths(filename))
  if check_duplicates(specialpaths):
    sys.stderr.write("Error. There are duplicate file names across directories.")
    sys.exit(1)
  if todir =='' and tozip == '':
    for path in specialpaths:
      print path
    sys.exit(0)
  elif todir !='':
    copy_to(specialpaths, todir)
    sys.exit(0)
  elif tozip !='':

    zip_to(specialpaths, tozip)
    sys.exit(0)
  else:
    sys.stderr.write("Error. Cannot set --todir and --tozip flags at the same time.")
    sys.exit(1)

  # os.path.basename(path)
  
if __name__ == "__main__":
  main()
