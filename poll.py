import sys
import json
import urllib2
import urllib
import re
import math
import collections

from datetime import datetime
from datetime import timedelta

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

        self.time = None ## msg['tc']

        self.text = info['frontends']['heading']

        self.participants = info['participantCount']

    def __str__(self):
        return self.id + ',' + self.participants

    def __hash__( self ):
        return hash( self.id )

    @staticmethod
    def load( file_name ):
        messages = {}

        for line in open( file_name ):
            if re.search( Message.HEADER, line):
                m = Message( line )
                if m.id:
                    messages[ m.id ] = m

        return messages

    @staticmethod
    def load_per_block( file_name, ids):

        messages = []

        for line in open( file_name ):
            if re.search( Poll.HEADER, line):
                m = Poll( line )
                if m.id in ids:
                    messages.append( m )

        messages = list( set( messages ) )
        messages = sorted( messages , key= lambda msg: msg.time )

        return messages

## all the messages per block
__CLASS = Poll
