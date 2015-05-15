from session import *
from chat import *
import sys


b = Block( sys.argv[1] )

for block in b.get_blocks( 'chat' , Message ):

    for content in block['content']:

        print block['id'] , ',', content.time
