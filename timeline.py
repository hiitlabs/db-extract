from session import *
from chat import *
from poll import *
import sys


b = Block( sys.argv[1] )


for block in b.get_blocks( 'chat' , Message ):

    for content in block['content']:

        print 'chat', block['id'] , ',', content.time

## todo: this should be done with extensions, not hack

Message.HEADER = 'rating:(.*)'

## TODO: fixme
shown_ids = []

for block in b.get_blocks( 'rating' , Message ):

    for content in block['content']:

        if content.id not in shown_ids: ## todo: fixme

            print 'vote', block['id'] , ',', content.time , ',' , content.id

            shown_ids.append( content.id )

for block in b.get_blocks( 'poll' , Poll ):

    for content in block['content']:

        print 'poll', block['id'],  ',', content.time
