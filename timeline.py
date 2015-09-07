from session import *
from chat import *
from poll import *
import sys

## initialize content types

types = {}

#f = open('/Users/mnelimar/Desktop/blocks_function.txt')

#for l in f:
#    l = l.split('|')

#    types[ l[0] ] = l[1]

b = Block( sys.argv[1] + '/objects.dirty' )

def out( type, block, content):

    t = '?????'
    if id in types:

        t = types[ id ]

    print type , ',', t ,',' , block['id'] , ',' , content.time, content.id, content.text, block['title'].encode('utf8')

## legacy for May 2014 stuff
# Message.HEADER = 'chat-message:(.*)'

for block in b.get_blocks( 'chat' , Message ):

    for content in block['content']:

        out( 'chat', block , content )


Message.HEADER = 'thread-message:(.*)'

for block in b.get_blocks( 'thread' , Message ):

    for content in block['content']:

        out( 'chat', block , content )

## todo: this should be done with extensions, not hack

Message.HEADER = 'rating:(.*)'

## TODO: fixme
shown_ids = []

for block in b.get_blocks( 'rating' , Message ):

    for content in block['content']:

        if content.id not in shown_ids: ## todo: fixme

            out( 'vote', block , content )

            shown_ids.append( content.id )

##for block in b.get_blocks( 'poll' , Poll ):

#    for content in block['content']:

#        out( 'poll', block['id'], content )
