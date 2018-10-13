import itemfunctions
from gamemessages import Message

class Item:
    def __init__(self,use_function=None,targeting=False,targeting_message=None,**kwargs):
        self.use_function=use_function
        self.targeting=targeting
        self.targeting_message=targeting_message
        self.function_kwargs=kwargs

    def to_json(self):
        if self.use_function:
            use_function=self.use_function.__name__
        else:
            use_function=None

        if self.targeting_message:
            targeting_message=self.targeting_message.to_json()
        else:
            targeting_message=None

        json_data={
            'use_function':use_function,
            'targeting':self.targeting,
            'targeting_message':targeting_message,
            'function_kwargs':self.function_kwargs
        }
        return json_data
    
    @staticmethod
    def from_json(json_data):
        if json_data.get('use_function'):
            use_function=getattr(itemfunctions,json_data.get('use_function'))
        else:
            use_function=None
        targeting=json_data.get('targeting')
        if json_data.get('targeting_message'):
            targeting_message=Message.from_json(json_data.get('targeting_message'))
        else:
            targeting_message=None
        function_kwargs=json_data.get('function_kwargs')

        return Item(use_function,targeting,targeting_message,**function_kwargs)