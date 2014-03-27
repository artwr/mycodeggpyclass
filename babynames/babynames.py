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

"""Baby Names exercise

Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 -Extract the year and print it
 -Extract the names and rank numbers and just print them
 -Get the names data into a dict and print it
 -Build the [year, 'name rank', ... ] list and print it
 -Fix main() to use the extract_names list
"""

def extract_names(filename):
  """
  Given a file name for baby.html, returns a list starting with the year string
  followed by the name-rank strings in alphabetical order.
  ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
  """
  # Create list
  nameranklist = []
  with open(filename, 'rU') as inputfile:
    text = inputfile.read()
    matchyear = re.search(r"Popularity\sin\s(\d+)", text)
    if matchyear:
      year = matchyear.group(1)
    nameranklist.append(year)
    nametuples = re.findall(r'<td>(\d+)</td><td>([a-zA-Z\-]+)</td><td>([a-zA-Z\-]+)</td>', text)
    if nametuples is None:
      sys.stderr.write('Could not find name-rank list in html file\n')
      sys.exit(1)
  # Create dictionary to store name rank pairs. 
  namerankdict = {}
  for tuple1 in nametuples:
    (rank, nameb, nameg) = tuple1
    if nameb not in namerankdict or namerankdict[nameb] > rank:
      namerankdict[nameb] = rank
    if nameg not in namerankdict or namerankdict[nameg] > rank:
      namerankdict[nameg] = rank
  for key in sorted(namerankdict.keys()):
    nameranklist.append(key + " " + namerankdict[key])
  return nameranklist


def main():
  # This command-line parsing code is provided.
  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  # Notice the summary flag and remove it from args if it is present.
  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  # +++your code here+++
  # For each filename, get the names, then either print the text output
  # or write it to a summary file
  for filename in args:
    nrlist = extract_names(filename)
    text = '\n'.join(nrlist) + '\n'
    if summary:
      with open(filename+".summary", 'w') as ofile:
        ofile.write(text)
      ofile.close()
    else:
      print text

if __name__ == '__main__':
  main()
