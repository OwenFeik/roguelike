import libtcodpy as lc
from random import randint
from map_objects.tile import Tile
from map_objects.room import Room
from entity import Entity
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from equipslots import EquipSlots
from components.equip import Equip
from itemfunctions import heal,cast_lightning,cast_fireball,cast_confuse
from renderfunctions import RenderOrder
from gamemessages import Message
from randomutils import random_choice_from_dict,from_dungeon_floor
import loader_functions.jsonloaders

class GameMap:
    def __init__(self,width,height,floor=0):
        self.width=width
        self.height=height
        self.tiles=self.initialise_tiles()
        self.floor=floor

    def to_json(self):
        json_data={
            'width':self.width,
            'height':self.height,
            'tiles':[[tile.to_json() for tile in tile_row] for tile_row in self.tiles],
            'floor':self.floor
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        width=json_data.get('width')
        height=json_data.get('height')
        tiles_json=json_data.get('tiles')
        floor=json_data.get('floor')

        game_map=GameMap(width,height,floor)
        game_map.tiles=[[Tile.from_json(tile_json) for tile_json in tile_row_json] for tile_row_json in tiles_json]

        return game_map
    
    def initialise_tiles(self):
        tiles=[[Tile(True,'wall') for y in range(self.height)]for x in range(self.width)]
        return tiles

    def refresh_tiles(self):
        for tile in self.tiles:
            tile.reload_texture()

    def make_map(self,max_rooms,room_min_size,room_max_size,map_width,map_height,player,entities):
        rooms=[]
        num_rooms=0

        center_of_last_room_x=None
        center_of_last_room_y=None

        for r in range(max_rooms):
            w=randint(room_min_size,room_max_size)
            h=randint(room_min_size,room_max_size)

            x=randint(0,map_width-w-1)
            y=randint(0,map_height-h-1)

            new_room=Room(x,y,w,h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.place_room(new_room)
                (new_x,new_y)=new_room.center()

                center_of_last_room_x=new_x
                center_of_last_room_y=new_y

                if num_rooms==0:
                    player.x=new_x
                    player.y=new_y
                else:
                    (prev_x,prev_y)=rooms[num_rooms-1].center()
                    if randint(0,1)==1:
                        self.create_h_tunnel(prev_x,new_x,prev_y)
                        self.create_v_tunnel(prev_y,new_y,new_x)
                    else:
                        self.create_v_tunnel(prev_y,new_y,prev_x)
                        self.create_h_tunnel(prev_x,new_x,new_y)
                
                self.place_entities(new_room,entities)

                rooms.append(new_room)
                num_rooms+=1
        stairs_component=Stairs(self.floor+1)
        down_stairs=Entity(center_of_last_room_x,center_of_last_room_y,'>',lc.white,'Stairs',render_order=RenderOrder.STAIRS,stairs=stairs_component)
        entities.append(down_stairs)

        #Check to make sure a path exists from the player to the down stairs
        fov_map=lc.map_new(self.width,self.height)
        for y in range(0,self.height):
            for x in range(0,self.width):
                lc.map_set_properties(fov_map,x,y,True,not self.tiles[x][y].blocked)
        lc.map_compute_fov(fov_map,0,0,100,True,0)
        path=lc.path_new_using_map(fov_map,1)
        lc.path_compute(path,player.x,player.y,down_stairs.x,down_stairs.y)

        if lc.path_is_empty(path): #If no path exists, make a tunnel to the down stairs
            if randint(0,1)==1:
                self.create_h_tunnel(down_stairs.x,player.x,down_stairs.y)
                self.create_v_tunnel(down_stairs.y,player.y,player.x)
            else:
                self.create_v_tunnel(down_stairs.y,player.y,down_stairs.x)
                self.create_h_tunnel(down_stairs.x,player.x,player.y)

    def place_room(self,room): #Place a room object on the map
        for x in range(0,room.width-1):
            for y in range(0,room.height-1):
                self.tiles[x+room.x+1][y+room.y+1].blocked=room.grid[y][x]
                self.tiles[x+room.x+1][y+room.y+1].block_sight=room.grid[y][x]
                if room.grid[y][x]: #If the room object has a true at the location, it means an obstruction exists
                    self.tiles[x+room.x+1][y+room.y+1].terrain='rubble'
                else: #Otherwise, the tile is open ground
                    self.tiles[x+room.x+1][y+room.y+1].terrain='ground'
                    self.tiles[x+room.x+1][y+room.y+1].texture=randint(21,23)

    def create_h_tunnel(self,x1,x2,y):
        for x in range(min(x1,x2),max(x1,x2)+1):
            self.tiles[x][y].blocked=False
            self.tiles[x][y].block_sight=False
            self.tiles[x][y].terrain='ground'
            self.tiles[x][y].reload_texture()
    
    def create_v_tunnel(self,y1,y2,x):
        for y in range(min(y1,y2),max(y1,y2)+1):
            self.tiles[x][y].blocked=False
            self.tiles[x][y].block_sight=False
            self.tiles[x][y].terrain='ground'
            self.tiles[x][y].reload_texture()

    def place_entities(self,room,entities):
        max_enemies_per_room=from_dungeon_floor([[2,1],[3,4],[5,6]],self.floor)
        max_items_per_room=from_dungeon_floor([[1,1],[2,4]],self.floor)
        
        number_of_enemies=randint(0,max_enemies_per_room)
        number_of_items=randint(0,max_items_per_room)

        monster_chances={'orc':80,'troll':from_dungeon_floor([[15,3],[30,5],[60,7]],self.floor)}
        item_chances={
        'healing_potion':35,
        'sword':from_dungeon_floor([[5,4]],self.floor),
        'shield':from_dungeon_floor([[15,8]],self.floor),
        'lightning_scroll':from_dungeon_floor([[25,4]],self.floor),
        'fireball_scroll':from_dungeon_floor([[25,6]],self.floor),
        'confusion_scroll':from_dungeon_floor([[10,2]],self.floor)
        }

        for i in range(number_of_enemies):
            x=randint(room.x+1,room.x+room.width-1)
            y=randint(room.y+1,room.y+room.height-1)
            if not any([entity for entity in entities if entity.x==x and entity.y==y]) and not self.is_blocked(x,y):
                monster_choice=random_choice_from_dict(monster_chances)
                if monster_choice=='orc':
                    enemy=loader_functions.jsonloaders.json_get_enemy('orc')
                    enemy.x=x
                    enemy.y=y
                else:
                    enemy=loader_functions.jsonloaders.json_get_enemy('troll')
                    enemy.x=x
                    enemy.y=y
                
                entities.append(enemy)

        for i in range(number_of_items):
            x=randint(room.x+1,room.x+room.width-1)
            y=randint(room.y+1,room.y+room.height-1)

            if not any([entity for entity in entities if entity.x==x and entity.y==y]) and not self.is_blocked(x,y):
                item_choice=random_choice_from_dict(item_chances)
                item=loader_functions.jsonloaders.json_get_item(item_choice)
                item.x=x
                item.y=y
                entities.append(item)

    def is_blocked(self,x,y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def next_floor(self,player,message_log,constants):
        self.floor+=1
        entities=[player]

        self.tiles=self.initialise_tiles()
        self.make_map(constants['max_rooms'],constants['room_min_size'],
            constants['room_max_size'],constants['map_width'],constants['map_height'],
            player,entities)

        player.fighter.heal(player.fighter.max_health // 2)

        message_log.add_message(Message('You take a moment to rest and recover your strength.',lc.light_violet))

        return entities