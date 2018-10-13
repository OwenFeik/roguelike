class Stairs:
    def __init__(self,floor):
        self.floor=floor

    def to_json(self):
        return {'floor':self.floor}
    
    @staticmethod
    def from_json(json_data):
        return Stairs(json_data.get('floor'))