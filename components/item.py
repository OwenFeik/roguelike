import itemfunctions

class Item:
    def __init__(self,use_function=None,targeting=False,targeting_message=None,**kwargs):
        self.use_function=use_function
        self.targeting=targeting
        self.targeting_message=targeting_message
        self.function_kwargs=kwargs

    def to_json(self):
        json_data={
            'use_function':self.use_function.__name__,
            'targeting':self.targeting,
            'targeting_message':self.targeting_message,
            'function_kwargs':self.function_kwargs
        }
        return json_data
    
    @staticmethod
    def from_json(json_data):
        use_function=getattr(itemfunctions,json_data.get('use_function'))
        targeting=json_data.get('targeting')
        targeting_message=json_data.get('targeting_message')
        function_kwargs=json_data.get('function_kwargs')

        return Item(use_function,targeting,targeting_message,function_kwargs)