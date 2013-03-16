import sys
import json
import urllib2
import urllib
import re
import math
import collections
from datetime import datetime
from datetime import timedelta

## all the messages per block
blocks = {}

## method for pringint one message in chat
def _print( msg ):
  id = msg['id'];

  t = datetime.strptime( msg['time'] , '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta( hours = 2 ) ## for Finland
  time_unix = t.strftime("%s")
  time_human = t.strftime('%H:%M')

  text = msg['message'].encode('utf-8').strip()
  author = msg['from'].encode('utf-8').strip()

  ## print data
  d = [ time_unix, time_human, text, author, id ]
  d = map( lambda x : str( x ) , d )
  print '|'.join( d )

## detect al blocks
def _block( line ):
   global blocks
   if not 'key' in line:
       return
   if line['key'].startswith( 'msgs:' ):
       blocks[ line['key'] ] = line['val']

def _per_block():
  global blocks
  for block in blocks:
    print block
    map( _print , blocks[block] )
    print '--'


def analyze_chat( f ):
  f = open( f, 'r')
  for line in f:
    _block( json.loads( line ) )
  _per_block();

if __name__ == '__main__':
  analyze_chat( sys.argv[1] )