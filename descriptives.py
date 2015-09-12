## from files, print descriptives of uses

import sys
from session import *

import chat
import datetime

import collections

def descriptives( file_name ):

    session = Presemo( file_name )

    print "Number of blocks", len( session.blocks )

    print "Block types", collections.Counter( map( lambda x: x.type , session.blocks ) )

    messages = collections.defaultdict( int )
    votes = collections.defaultdict( int )

    for block in session.blocks:

        activity = block.activity()

        messages[ block.type ] += activity[1]
        votes[ block.type ] += activity[2]

    print "Total number of messages", messages
    print "Total number of votes", votes

    ## check days from content that has time code

    chat.Message.HEADER = 'thread-message:(.*)' ## fixme
    messages = chat.Message.load( file_name )

    messages = map( lambda x: x.time, messages.values() )
    messages = map( lambda x: datetime.datetime.fromtimestamp( x / 1000 ) , messages )

    dates = map( lambda x: x.date() , messages )
    dates = set( dates )
    print "Data collected for", len( dates ), "days"


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print f
        descriptives( f )
