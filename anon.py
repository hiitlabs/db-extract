import sys

# sys.path.append('./db-extract')

import chat

class Message( chat.Message ):
	
  def fill(self, msg ):
  	chat.Message.fill( self, msg )
  	self.experiment = msg['_experiment']
  	self.author_id = msg['from_id']

  def __str__(self):
  	s = chat.Message.__str__( self )
  	experiment = '1' if self.experiment else '0'
  	return experiment + self.CVS_SEPARATOR + self.author_id

chat.__MESSAGE_CLASS = Message
_authors = {}

def analyze( db ):
	global _authors

	chat.analyze_chat( db )

	for m in chat.get_messages():
		u = ( db, m.author_id , m.experiment )
		if u not in _authors:
			_authors[ u ] = 0
		_authors[ u ] += 1

analyze('../dev1.db')
analyze('../dev2.db')