import libtcodpy as lc
import textwrap

class Message:
    def __init__(self,text,colour=lc.white):
        self.text=text
        self.colour=colour

    def to_json(self):
        json_data={
            'text':self.text,
            'colour':self.colour
        }
        return json_data
    
    @staticmethod
    def from_json(json_data):
        text=json_data.get('text')
        colour=json_data.get('colour')

        if colour:
            message=Message(text,colour)
        else:
            message=Message(text)
        
        return message

class MessageLog:
    def __init__(self,x,width,height):
        self.messages=[]
        self.x=x
        self.width=width
        self.height=height
        
    def to_json(self):
       json_data={
           'x':self.x,
           'width':self.width,
           'height':self.height,
           'messages':[message.to_json() for message in self.messages]
       }
       return json_data
    
    @staticmethod
    def from_json(json_data):
       x=json_data.get('x')
       width=json_data.get('width')
       height=json_data.get('height')
       messages_json=json_data.get('messages')
        
       message_log=MessageLog(x,width,height)

       for message_json in messages_json:
           message_log.add_message(Message.from_json(message_json))

       return message_log

    def add_message(self, message):
        new_msg_lines=textwrap.wrap(message.text,self.width)

        for line in new_msg_lines:
            if len(self.messages)==self.height:
                del self.messages[0]
            self.messages.append(Message(line,message.colour))