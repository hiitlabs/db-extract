import sys
import json
import urllib2
import urllib
import re
import math
import collections

from datetime import datetime
from datetime import timedelta

class Message:

    HEADER = 'chat:(.*)meta' ## not super, but good enought?

    def __init__(self, line = None, json = None):
        if line:
            self.parse( line )
        if json:
            self.fill( json )

    def parse( self, line):
        self.fill( json.loads( line ) )

    def fill(self, msg ):
        self._json = msg

        msg = msg['val']

        ## dummy control for mistakes in rating system code
        if not isinstance( msg , dict ):
            self.id = None
            return

        if not 'id' in msg:
            self.id = None
            return

        self.id = msg['id']

        self.time = msg['tc']

        self.text = None
        if isinstance( msg['text'], str) or isinstance( msg['text'], unicode):
            self.text = msg['text'].encode('utf-8').strip()

        if 'userId' in  msg['meta']:
            self.author = msg['meta']['userId']

    def __str__(self):
        return self.text + ' (' + self.author + ',' + str( self.time ) + ')'

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
            if re.search( Message.HEADER, line):
                m = Message( line )
                if m.id in ids:
                    messages.append( m )

        messages = list( set( messages ) )
        messages = sorted( messages , key= lambda msg: msg.time )

        return messages

## all the messages per block
__MESSAGE_CLASS = Message

if __name__ == '__main__':

    msgs = Message.load( sys.argv[1] )

    print 'Total number of messages', len( msgs.values() )

    for m in msgs.values():
        print m.time,",",m.author,",",m.text
