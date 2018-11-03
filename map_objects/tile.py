class Tile:
    def __init__(self,blocked,terrain,block_sight=None):
        self.blocked=blocked
        if block_sight is None:
            block_sight=blocked
        self.block_sight=block_sight
        self.explored=False
        self.terrain=terrain
    
    def to_json(self):
        json_data={
            'blocked':self.blocked,
            'terrain':self.terrain,
            'block_sight':self.block_sight,
            'explored':self.explored
        }
        return json_data
    
    @staticmethod
    def from_json(json_data):
        blocked=json_data.get('blocked')
        terrain=json_data.get('terrain')
        block_sight=json_data.get('block_sight')
        explored=json_data.get('explored')

        tile=Tile(blocked,terrain,block_sight)
        if tile.explored:
            tile.explored=explored

        return tile