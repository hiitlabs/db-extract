import sys

# sys.path.append('./db-extract')

import chat

class Message( chat.Message ):
	
  def fill(self, msg ):
  	chat.Message.fill( self, msg )
  	self.experiment = msg['_experiment']

  def __str__(self):
  	s = chat.Message.__str__( self )
  	return s + self.CVS_SEPARATOR +  str(self.experiment)

chat.__MESSAGE_CLASS = Message
chat.analyze_chat('../dev1.db')
print chat.all_print()