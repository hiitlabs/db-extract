import sys
import json

from chat import Message

class _Block:

    def __init__( self, _id, _type, parent ):
        self.type = _type
        self.id = _id
        self.title = 'missing'

        self.data = None

        ## collect extra data
        dbkey = self.type + ':' + self.id

        if self.type == 'chat' or self.type == 'rating':
            dbkey += 'frontends'

        if len( parent.__search_key( dbkey ) ) > 0:

            self.data = parent.__search_key( dbkey )[-1]

            if 'heading' in self.data:
                self.title = self.data['heading'].encode('utf-8')

            if 'frontends' in self.data:
                self.title = self.data['frontends']['heading'].encode('utf-8')

            print self.id  , ',' ,  self.type ,  ','  , self.title



class Block:

    def __search_key( self, key ):

        ret = []

        for line in open( self.f ):
            line = json.loads( line )

            if line['key'] == key:
                ret.append( line['val'] )

        return ret


    STORE = "BlockStore:refs"

    def __init__(self, file_name ):

        self.f = file_name

        blocks = self.__search_key( self.STORE )

        ## manually make sure that we have only one of each
        self.blocks = {}

        for b in blocks[-1]:
            if b['id'] not in self.blocks:
                self.blocks[ b['id'] ] = b
                print b['type']
                print _Block( b['id'], b['type'], self )

        self.blocks = self.blocks.values()

        self.content = {}


        ## check hot to make this smarter
        for block in self.blocks:

            if block['type'] == 'chat':
                key = 'chat:' + block['id'] + 'msgIds'
                self.content[ block['id'] ] = set( self.__search_key( key )[-1] )

    def get_blocks( self, type_name, class_name ):

        for block in self.blocks:
            if block['type'] == type_name:

                print '\n\n\n'


                b = _Block( block['id'], block['type'], self )

                ## all content of this block
                print '\n'.join( map( lambda x: ' - ' + str(x), class_name.load_per_block( self.f, self.content[ block['id'] ] ) ) )


if __name__ == '__main__':
    b = Block( sys.argv[1] )
    ## b.get_blocks( 'chat' , Message )
    ## b.get_blocks( 'scatter', Message )
