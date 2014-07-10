#!/bin/python
#
# Copyright (C) 2012 Gedare Bloom
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# $Id: fetch-flagged-email.py 2 2012-04-19 00:40:58Z gedarebloom@gmail.com $
#

from datetime import date, timedelta
import email
import getopt
import getpass
import os
import re
import sys

## get imapclient at http://imapclient.freshfoo.com/
from imapclient import IMAPClient 

def usage():
  print "\
fetch-flagged-email.py retrieves email that has been \\\\Flagged (gmail starred).\n\
Specify a folder (gmail label) and it will retrieve all flagged emails\n\
in that folder using imap and your account/password. The imap support\n\
relies on a non-standard python library imapclient which is available at\n\
http://imapclient.freshfoo.com/. By default fetched emails remain flagged\n\
on the server, but passing the -r flag unflags (unstars) them.\n\
Emails are saved in text files based on email sequence numbers.\n\
\n\
You can customize the default arguments in fetch-flagged-email.py:main().\n\
Your email account and password can be entered interactively in addition to\n\
passed on the command line or hard-coded as default arguments.\n\
\n\
Usage: fetch-flagged-email.py -[hi:f:u:p:d:o:r]\n\
  -h --help           print this help\n\
  -i --imap           imap server                           [imap.gmail.com]\n\
  -f --folder         folder to use                         [INBOX]\n\
  -u --username       email account                         []\n\
  -p --password       account password                      []\n\
  -d --days           days back to look (0 for all)         [0]\n\
  -o --output         output directory for messages         [.]\n\
  -r --resetflag      reset \\\\Flagged (starred) attribute   [False]\n"

def connect(server_address):
  return IMAPClient(server_address, use_uid=True, ssl=True)

def searchmail(imap_server, search, output, resetflag):
  messages = imap_server.search(search)
  messages_contents = imap_server.fetch(messages, ['RFC822'])
  for message_id, data in messages_contents.iteritems():
    message_string = data['RFC822']
    message = email.message_from_string(message_string)
    filename =  "{0:04}.mail".format(data['SEQ'])
    outfile = os.path.join(output,filename)
    f = open(outfile, 'w')
    f.write(message_string)
    f.close()
    print "{0} -> {1}\n".format(message['subject'], outfile)

  if resetflag:
    imap_server.remove_flags(messages, '\\Flagged')

def main():
  ## Customize these default args and stop using any command line arguments.

  # imap server
  imap = 'imap.gmail.com'
  
  # restrict searching to a folder (label) name you use
  folder = 'INBOX'
  
  # username and password can be entered on command line, interactively,
  # or hard-coded here. username is of the form user@domain.com
  username = ''
  password = ''

  # For search keywords see http://tools.ietf.org/html/rfc3501#section-6.4.4
  ## To get flagged (starred) email that has PATCH in the subject line
  ## and is not a reply:
  ##   search = ['FLAGGED', 'SUBJECT \"PATCH\"', 'NOT SUBJECT \"Re\"']
  ## Default behavior: get flagged email
  search = ['FLAGGED']

  # set to '0' to get all
  days = '0'

  # where search result emails get written
  output = "."

  # Set to True to reset the Flagged flag (starred) automatically
  resetflag = False

  # Process args
  try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:f:u:p:d:o:r",
        ["help", "imap=", "folder", "username=", "password=",
          "days=", "output=", "resetflag="])
  except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit()
    elif opt in ("-i", "--imap"):
      imap = True
    elif opt in ("-f", "--folder"):
      folder = arg
    elif opt in ("-u", "--username"):
      username = arg
    elif opt in ("-p", "--password"):
      password = arg
    elif opt in ("-d", "--days"):
      days = arg
    elif opt in ("-o", "--output"):
      output = arg
    elif opt in ("-r", "--resetflag"):
      resetflag = True
    else:
      assert False, "unhandled option"
   
  if not os.path.exists(output):
    print("Invalid output directory: " + output)
    sys.exit(1)

  if not username:
    username = raw_input("Enter email account: ")

  if not password:
    password = getpass.getpass("Enter email account password: ")

  if not days == "0":
    cutoff = date.today() - timedelta(int(days))
    search.append("SINCE {0}".format(cutoff.strftime('%d-%b-%Y')))

  imap_server = connect(imap)
  imap_server.login(username, password)
  imap_server.select_folder(folder)
  searchmail(imap_server, search, output, resetflag)
  
if __name__ == "__main__":
  main()

