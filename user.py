import sys
import json
import re

class User:

    HEADER = 'UserConstructor:(.*)personas'

    def __init__(self, line = None, json = None):
        if line:
            self.parse( line )
        if json:
            self.fill( json )

    def parse( self, line):
        self.fill( json.loads( line ) )

    def fill(self, user ):
        self._json = user

        user = user['val']

        self.id = None
        if 'web' in user:
            self.id = user['web']['id']

        self.name = user['username'].encode('utf8')

    @staticmethod
    def load( file_name ):
        users = {}

        for line in open( file_name ):
            if re.search( User.HEADER, line):
                u = User( line )
                if u.id:
                    users[ u.id ] = u

        return users


if __name__ == '__main__':

    users = User.load( sys.argv[1] )

    print 'Total number of users', len( users.values() )

    for u in users.values():
        if u.name != '':
            print u.name
