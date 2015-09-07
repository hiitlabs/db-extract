## from files, print descriptives of uses

import sys
from session import *

def descriptives( file_name ):

    session = Presemo( file_name )

    print "Number of blocks", len( session.blocks )

    messages = 0
    votes = 0

    for block in session.blocks:

        activity = block.activity()

        messages += activity[1]
        votes += activity[2]

    print "Total number of messages", messages
    print "Total number of votes", votes


if __name__ == '__main__':
    for f in sys.argv[1:]:
        print f
        descriptives( f )
