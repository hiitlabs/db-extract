# -- coding: utf-8 --

import sys
import json
import urllib2
import urllib
import re
import math
import collections
from datetime import datetime
from datetime import timedelta

class Block():

  def __init__(self, json = None):
    if json:
      self.fill( json )

  def parse( self, line):
    self.fill( json.loads( line ) )

  def fill( self, json ):
    self.id = json['id']
    self.name = json['label']

  def __str__(self):
    return self.name

__blocks = {}

def _print( block ):
  print str( block )

def _block( line ):
   global __blocks
   if not 'key' in line:
       return
   if line['key'].startswith( 'blocks:' ):
       __blocks[ line['key'] ] = line['val']

def all_print():
  global __blocks
  for block in __blocks:
    map( _print , __blocks[ block ] )

def all():
  return map( lambda x : Block(x),  __blocks.values() )

def get( id ):
  if id in __blocks:
    return Block( __blocks[ id ] )
  return None

def analyze( f ):
  f = open( f, 'r')
  for line in f:
    _block( json.loads( line ) )

if __name__ == '__main__':
  analyze( sys.argv[1] )
  all_print()