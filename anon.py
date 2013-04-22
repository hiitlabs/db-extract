import sys

# sys.path.append('./db-extract')

import chat

class Message( chat.Message ):
	
  def fill(self, msg ):
  	chat.Message.fill( self, msg )
  	self.kissa = 'kissa1'

  def __str__(self):
  	return self.kissa

chat.__MESSAGE_CLASS = Message
chat.analyze_chat('../dev1.db')
print chat.all_print()