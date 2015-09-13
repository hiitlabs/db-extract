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



def out( type, block, content):

    t = '?????'
    if id in types:

        t = types[ id ]

    print type , ',', t ,',' , block['id'] , ',' , content.time, content.id, content.text, block['title'].encode('utf8')

session = Presemo( sys.argv[1] + '/objects.dirty' )

for block in session.blocks:

    for content in block.content():

        print block.type, block.id, content.time, content.id
