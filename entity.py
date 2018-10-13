import math
import libtcodpy as lc
from renderfunctions import RenderOrder
from components.ai import ai_from_json
from components.equip import Equip
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.item import Item
from components.level import Level
from components.stairs import Stairs



#TODO: refactor initialisation to allow passing of a *args of components
#TODO: 1 line if statements in JSON functions

class Entity:
    def __init__(self,x,y,char,colour,name,blocks=False,render_order=RenderOrder.CORPSE,fighter=None,ai=None,item=None,inventory=None,stairs=None,level=None,equipment=None,equip=None):
        self.x=x
        self.y=y
        self.char=char
        self.colour=colour
        self.name=name
        self.blocks=blocks
        self.render_order=render_order
        self.fighter=fighter
        self.ai=ai
        self.item=item
        self.inventory=inventory
        self.stairs=stairs
        self.level=level
        self.equipment=equipment
        self.equip=equip

        if self.fighter:
            self.fighter.owner=self
        if self.ai:
            self.ai.owner=self
        if self.item:
            self.item.owner=self
        if self.inventory:
            self.inventory.owner=self
        if self.level:
            self.level.owner=self
        if self.equipment:
            self.equipment.owner=self
        if self.equip:
            self.equip.owner=self

            if not self.item:
                item=Item()
                self.item=item
                self.item.owner=self 

    def to_json(self):
        if self.fighter:
            fighter=self.fighter.to_json()
        else:
            fighter=None
        
        if self.ai:
            ai=self.ai.to_json()
        else:
            ai=None

        if self.item:
            item=self.item.to_json()
        else:
            item=None

        if self.inventory:
            inventory=self.inventory.to_json()
        else:
            inventory=None
        
        if self.stairs:
            stairs=self.stairs.to_json()
        else:
            stairs=None

        if self.equipment:
            equipment=self.equipment.to_json()
        else:
            equipment=None

        if self.level:
            level=self.level.to_json()
        else:
            level=None

        if self.equip:
            equip=self.equip.to_json()
        else:
            equip=None
        
        json_data={
            'x':self.x,
            'y':self.y,
            'char':self.char,
            'colour':[self.colour.r,self.colour.g,self.colour.b],
            'name':self.name,
            'blocks':self.blocks,
            'render_order':self.render_order.value,
            'fighter':fighter,
            'ai':ai,
            'item':item,
            'inventory':inventory,
            'stairs':stairs,
            'equipment':equipment,
            'level':level,
            'equip':equip
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        x=json_data.get('x')
        y=json_data.get('y')
        char=json_data.get('char')
        colour=lc.Color(json_data.get('colour')[0],json_data.get('colour')[1],json_data.get('colour')[2])
        name=json_data.get('name')
        blocks=json_data.get('blocks')
        render_order=RenderOrder(json_data.get('render_order'))

        if json_data.get('fighter'):
            fighter=Fighter.from_json(json_data.get('fighter'))
        else:
            fighter=None
            
        if json_data.get('ai'):
            ai=ai_from_json(json_data.get('ai'))
        else:
            ai=None

        if json_data.get('item'):
            item=Item.from_json(json_data.get('item'))
        else:
            item=None
        
        if json_data.get('inventory'):
            inventory=Inventory.from_json(json_data.get('inventory'))
        else:
            inventory=None

        if json_data.get('stairs'):
            stairs=Stairs.from_json(json_data.get('stairs'))
        else:
            stairs=None
        
        if json_data.get('equipment'):
            equipment=Equipment.from_json(json_data.get('equipment'))
        else:
            equipment=None

        if json_data.get('level'):
            level=Level.from_json(json_data.get('level'))
        else:
            level=None

        if json_data.get('equip'):
            equip=Equip.from_json(json_data.get('equip'))
        else:
            equip=None

        return Entity(x,y,char,colour,name,blocks,render_order,fighter,ai,item,inventory,stairs,level,equipment,equip)

    def move(self,dx,dy):
        self.x+=dx
        self.y+=dy
    
    def move_towards(self,target_x,target_y,game_map,entities):
        dx=target_x-self.x
        dy=target_y-self.y
        distance=math.sqrt(dx**2+dy**2)

        dx=int(round(dx/distance))
        dy=int(round(dy/distance))

        if not (game_map.is_blocked(self.x+dx,self.y+dy)or get_blocking_entities_at_location(entities,self.x+dx,self.y+dy)):
            self.move(dx,dy)

    def move_astar(self,target,entities,game_map):
        fov_map=lc.map_new(game_map.width,game_map.height)

        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                lc.map_set_properties(fov_map,x1,y1,not game_map.tiles[x1][y1].block_sight,not game_map.tiles[x1][y1].blocked)
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                lc.map_set_properties(fov_map,entity.x,entity.y,True,False)

        path=lc.path_new_using_map(fov_map,1.41)
        lc.path_compute(path,self.x,self.y,target.x,target.y)

        if not lc.path_is_empty(path) and lc.path_size(path)<25:
            x,y=lc.path_walk(path,True)
            if x or y:
                self.x=x
                self.y=y
        else:
            self.move_towards(target.x,target.y,game_map,entities)

        lc.path_delete(path)
    
    def distance(self,x,y):
        return math.sqrt((x-self.x)**2+(y-self.y)**2)

    def distance_to(self,other):
        dx=other.x-self.x
        dy=other.y-self.y
        return math.sqrt(dx**2+dy**2)

def get_blocking_entities_at_location(entities,destination_x,destination_y):
    for entity in entities:
        if entity.blocks and entity.x==destination_x and entity.y==destination_y:
            return entity
    return None