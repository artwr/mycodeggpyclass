#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# This code was modified by Arthur Wiedmer. The original code is available 
# from the Google's Python Class website listed above.

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
# LAB(begin solution)
def url_sort_key(url):
  """Used to order the urls in increasing order by 2nd word if present."""
  match = re.search(r'-(\w+)-(\w+)\.jpg', url)
  if match:
    return match.group(2)
  else:
    return url
# LAB(end solution)

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  hostname = filename.split("_")[1]
  protocol = "http://"
  with open(filename,'rU') as logfile:
    text = logfile.read()
  logfile.close()
  relpathlist = re.findall(r"GET (\S*puzzle\S*) HTTP", text)
  if len(relpathlist) == 0:
    sys.stderr.write("No urls found\n")
    sys.exit(1)
  relpathlist = list(set(relpathlist))
  relpathlist = sorted(relpathlist, key = url_sort_key)
  urllist = [protocol + hostname + u for u in relpathlist]
  return urllist
  
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
  print "Retrieving..."
  imglist = []
  for index, url in enumerate(img_urls):
    filename = "img" + str(index).zfill(3) + ".jpg"
    imglist.append(filename)
    try:
      urllib.urlretrieve(url, dest_dir + "/" +filename)
    except IOError:
      print 'problem reading url:', url
  
  # Create list of images
  # filelist = os.listdir(dest_dir)
  # imgfilelist = []
  # for file1 in filelist:
  #   if re.search(r".*jpg",file1):
  #     imgfilelist.append(file1)
  
  #Start creating index.html
  htmlfilename = dest_dir + "/index.html"
  with open(htmlfilename,'w') as htmlfile:
    htmlfile.write("""<verbatim>
    <html>
    <body>
    """)
    imgtags = "<img src=" + "><img src=".join(imglist) + ">"
    htmlfile.write(imgtags)
    htmlfile.write("""
    </body>
    </html>
    """)
  htmlfile.close()
  


# Start of main()
def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
