from session import *
from chat import *
from poll import *
import sys

session = Presemo( sys.argv[1] + '/objects.dirty' )

for block in session.blocks:

    for content in block.content():

        print block.type, block.id, content.time, content.id
