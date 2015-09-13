import sys
import json

from chat import Message
from poll import Poll

class Block:

    def __init__( self, _id, _type, file ):
        self.type = _type
        self.id = _id

        self.file = file

        self.title = 'missing'

        self.data = None
        self._content = None

        ## collect descriptive data

        ## block name
        dbkey = self.type + ':' + self.id

        if self.type == 'chat' or self.type == 'rating' or self.type == 'thread':
            dbkey += 'frontends'

        if len( Presemo.search_key( self.file , dbkey ) ) > 0:

            self.data = Presemo.search_key( self.file , dbkey )[-1]

            if 'heading' in self.data:
                self.title = unicode( self.data['heading'] )

            elif 'frontends' in self.data:
                self.title = unicode( self.data['frontends']['heading'] )

        ## block raw content
        if self.type == 'chat':
            key = 'chat:' + self.id + 'msgIds'
            self._content = set( Presemo.search_key( self.file , key )[-1] )

        if self.type == 'thread':
            key = 'thread:' + self.id + 'msgIds'
            self._content = set( Presemo.search_key( self.file , key )[-1] )

        if self.type == 'rating':
            key = 'rating:' + self.id + 'msgIds'
            self._content = set( Presemo.search_key( self.file , key )[-1] )

        if self.type == 'poll':
            key = 'poll:' + self.id
            self._content = Presemo.search_key( self.file , key )


    def __str__( self ):
        return self.id  + '|' +  self.type +  '|'  + unicode( self.title ).encode('ascii', 'ignore') + '|' + '|'.join( map( str , self.activity() ) )

    def activity(self):

        messages = 0
        votes = 0
        participants = -1

        dbkey = self.type + ':' + self.id

        if Presemo.search_key( self.file , dbkey + 'participantCount' ):

            participants = max( Presemo.search_key( self.file , dbkey + 'participantCount' ) )

        if self.type == 'chat' or self.type == 'rating' or self.type == 'thread':

            messages = len( self._content )

        if self.type == 'rating':

            temp = Presemo.search_key( self.file , dbkey + 'results' )[-1]

            if temp:
                votes = sum( map( lambda x: x['points'] , temp ) )

        if self.type == 'poll':

            votes = Presemo.search_key( self.file, dbkey  )[-1]
            votes = len( votes['participants'] )

        return participants, messages, votes


    def content( self ):

        ## real content loading

        if self.type == 'chat':
            ## Message.HEADER = 'chat-message:(.*)'
            HEADER = 'chat:(.*)meta'
            msg = Message.load_per_block( self.file , self._content  )
            return msg

        if self.type == 'rating':
            Message.HEADER = 'rating:(.*)'
            msg = Message.load_per_block( self.file , self._content  )
            return msg

        if self.type == 'poll':
            polls = Poll.load_per_block( self.file , [ self.id ] )
            return polls

        print self.type
        return []


class Presemo:

    @staticmethod
    def search_key( file, key ):

        ret = []

        for line in open( file ):
            line = json.loads( line )

            if line['key'] == key:
                ret.append( line['val'] )

        return ret

    STORE = "BlockStore:refs"

    def __init__(self, file_name ):

        self.file = file_name

        blocks = Presemo.search_key( self.file, self.STORE )

        ## check which term to use for blockstore
        if len( blocks ) == 0:
            self.STORE = "blocks:refs"
            blocks = Presemo.search_key( self.file, self.STORE )

        ## manually make sure that we have only one of each
        self.raw_blocks = {}
        self.blocks = {}

        for b in blocks[-1]:
            if b['id'] not in self.blocks:
                self.raw_blocks[ b['id'] ] = b
                self.blocks[ b['id'] ] = Block( b['id'], b['type'], self.file )

        self.blocks = self.blocks.values()


if __name__ == '__main__':
    b = Presemo( sys.argv[1] )

    for block in b.blocks:

        print block.title.encode('utf8')
