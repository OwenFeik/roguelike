import loader_functions.jsonloaders

class Tile:
    def __init__(self,blocked,terrain,block_sight=None,texture=0):
        self.blocked=blocked
        if block_sight is None:
            block_sight=blocked
        self.block_sight=block_sight
        self.explored=False
        self.terrain=terrain
        if texture:
            self.texture=texture  
        else: 
            self.texture=loader_functions.jsonloaders.json_get_texture(self.terrain)
    
    def reload_texture(self,texture=-1):
        if texture>=0:
            self.texture=texture
        else:
            self.texture=loader_functions.jsonloaders.json_get_texture(self.terrain)
            
    def to_json(self):
        json_data={
            'blocked':self.blocked,
            'terrain':self.terrain,
            'block_sight':self.block_sight,
            'explored':self.explored,
            'texture':self.texture
        }
        return json_data
    
    @staticmethod
    def from_json(json_data):
        blocked=json_data.get('blocked')
        terrain=json_data.get('terrain')
        block_sight=json_data.get('block_sight')
        explored=json_data.get('explored')
        texture=json_data.get('texture')

        if texture:
            tile=Tile(blocked,terrain,block_sight,texture)
        else:
            tile=Tile(blocked,terrain,block_sight)

        if tile.explored:
            tile.explored=explored

        return tile