import sys
import json
import urllib2
import urllib
import re
import math
import collections
from datetime import datetime
from datetime import timedelta

CVS_SEPARATOR = '|'

class Message:

  def __init__(self, json = None):
    if json:
      self.fill( json )

  def parse( self, line):
    self.fill( json.loads( line ) )

  def fill(self, msg ):
    self.id = msg['id']
    self.time = datetime.strptime( msg['time'] , '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta( hours = 2 ) ## for Finland
    self.text = msg['text'].encode('utf-8').strip()
    self.author = msg['from'].encode('utf-8').strip()

  def __str__(self):
    time_unix = self.time.strftime("%s")
    time_human = self.time.strftime('%H:%M')
    l = [ time_unix, time_human, self.text, self.author, self.id ]
    l = map( lambda x : str( x ) , l )
    return CVS_SEPARATOR.join( l )

## all the messages per block
__blocks = {}

## method for pringint one message in chat
def _print( msg ):
  msg = Message( msg )
  print str(msg)

## detect al blocks
def _block( line ):
   global __blocks
   if not 'key' in line:
       return
   if line['key'].startswith( 'msgs:' ):
       __blocks[ line['key'] ] = line['val']

def print():
  global __blocks
  for block in __blocks:
    print block
    map( _print , __blocks[block] )
    print '--'


def analyze_chat( f ):
  f = open( f, 'r')
  for line in f:
    _block( json.loads( line ) )
  print();

if __name__ == '__main__':
  analyze_chat( sys.argv[1] )