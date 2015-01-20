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
        self.id = msg['id']

        self.time = None ## TODO: fixme

        self.text = None
        if isinstance( msg['text'], str) or isinstance( msg['text'], unicode):
            self.text = msg['text'].encode('utf-8').strip()
        self.author = msg['meta']['userId']

    def __str__(self):
        return self.time + ' + ' +self.text

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

        messages = sorted( messages , key= lambda msg: msg.time )

        return messages

## all the messages per block
__MESSAGE_CLASS = Message

if __name__ == '__main__':

    msgs = Message.load( sys.argv[1] )

    print 'Total number of messages', len( msgs.values() )

    for m in msgs.values():
        print m.text
