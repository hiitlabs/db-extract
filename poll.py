import sys
import json
import urllib2
import urllib
import re
import math
import collections

from datetime import datetime
from datetime import timedelta
## poll blocks don't have a tc, thus a hack

xxx_log = None
xxx_session = None
import sys

def xxx_init_time_estimate( file_name ):

    global xxx_log
    global xxx_session

    xxx_log = open( file_name ).readlines()

    def debug( x ):
        try:
            return json.loads( x )
        except ValueError:
            return None

    xxx_log = map( debug, xxx_log )

    xxx_session = open( sys.argv[1] + '/sessions.dirty' )
    xxx_session = map( debug , xxx_session )

    xxx_session = filter( lambda x: x != None, xxx_session )

    temp = xxx_session

    xxx_session = {}

    for t in temp:

        if 'val' in t and 'userId' in t['val']:
            if t['val']['userId'] not in xxx_session:
                xxx_session[ t['val']['userId'] ] = t

def xxx_estimate_time( poll ):

    global xxx_log
    global xxx_sessio

    current = xxx_log.index( poll._json )

    back_closest_with_tc = 0
    future_closest_with_tc = len( xxx_log )

    ## go back
    for i in range( current, 0, -1 ):

        if 'UserConstructor' in xxx_log[i]['key']:

            back_closest_with_tc = i
            break

    ## go future
    for i in range( current, len( xxx_log ) ):

            if 'UserConstructor' in xxx_log[i]['key']:

                future_closest_with_tc = i
                break

    closest_with_tc = back_closest_with_tc
    if abs( back_closest_with_tc - current ) > abs( future_closest_with_tc ):
        closest_with_tc = future_closest_with_tc


    key = xxx_log[i]['key'][16:]

    if key in xxx_session:
        date = xxx_session[ key ]['val']['cookie']['expires']
        delta = xxx_session[ key ]['val']['cookie']['originalMaxAge']
                                        ## 2015-04-28T11:09:43.277Z
        date = datetime.strptime( date , '%Y-%m-%dT%H:%M:%S.%fZ')
        date -= timedelta( milliseconds = delta )

        date = date - datetime.utcfromtimestamp(0)

        return '%i' %  ( date.total_seconds() * 1000 )

    return None

class Poll:

    HEADER = 'poll:(.*)' ## not super, but good enought?

    def __init__(self, line = None, json = None):
        if line:
            self.parse( line )
        if json:
            self.fill( json )

    def parse( self, line):
        self.fill( json.loads( line ) )

    def fill(self, info ):
        self._json = info

        info = info['val']

        ## dummy control for mistakes in rating system code
        if not isinstance( info , dict ):
            self.id = None
            return

        if not 'id' in info:
            self.id = None
            return

        self.id = info['id']

        self.time = xxx_estimate_time( self ) ## None ## msg['tc']

        if 'heading' in info:
            self.text = info['heading']
        else:
            self.text = info['frontends']['heading']

        self.participants = info['participantCount']

    def __str__(self):
        return self.id + ',' + self.participants

    def __hash__( self ):
        return hash( self.id )



    @staticmethod
    def load( file_name ):

        xxx_init_time_estimate( file_name )

        messages = {}

        for line in open( file_name ):
            if re.search( Message.HEADER, line):
                m = Message( line )
                if m.id:
                    messages[ m.id ] = m

        return messages

    @staticmethod
    def load_per_block( file_name, ids):

        xxx_init_time_estimate( file_name )

        messages = []

        for line in open( file_name ):
            if re.search( Poll.HEADER, line):
                m = Poll( line )
                if m.id in ids:
                    messages.append( m )

        messages = list( set( messages ) )
        messages = filter( lambda x: x.time != None, messages )

        messages = sorted( messages , key= lambda msg: msg.time )

        return messages

## all the messages per block
__CLASS = Poll
