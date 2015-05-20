from session import *
from chat import *
from poll import *
import sys

b = Block( sys.argv[1] + '/objects.dirty' )

def out( type, id, content):
    print type , ',' , id , ',' , content.time


for block in b.get_blocks( 'chat' , Message ):

    for content in block['content']:

        out( 'chat', block['id'] , content )

## todo: this should be done with extensions, not hack

Message.HEADER = 'rating:(.*)'

## TODO: fixme
shown_ids = []

for block in b.get_blocks( 'rating' , Message ):

    for content in block['content']:

        if content.id not in shown_ids: ## todo: fixme

            out( 'vote', block['id'] , content )

            shown_ids.append( content.id )

for block in b.get_blocks( 'poll' , Poll ):

    for content in block['content']:

        out( 'poll', block['id'], content )
