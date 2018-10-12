import libtcodpy as lc
from entity import Entity
from renderfunctions import RenderOrder
from map_objects.gamemap import GameMap
from gamemessages import MessageLog
from gamestates import GameStates
from equipslots import EquipSlots

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.equip import Equip

def get_constants():
    window_title='roguelike'

    screen_width=80
    screen_height=50

    bar_width=20
    panel_height=7
    panel_y=screen_height-panel_height

    message_x=bar_width+2
    message_width=screen_width-bar_width-2
    message_height=panel_height-1

    map_width=80
    map_height=43

    room_max_size=8
    room_min_size=3
    max_rooms=30
    max_enemies_per_room=3
    max_items_per_room=2

    fov_algorithm=0
    fov_light_walls=True
    fov_radius=5

    colours={
        'dark-wall':lc.Color(50,35,0),
        'dark-ground':lc.Color(20,0,0),
        'light-wall':lc.Color(100,75,0),
        'light-ground':lc.Color(50,0,0)
    }

    constants={
        'window_title':window_title,
        'screen_width':screen_width,
        'screen_height':screen_height,
        'bar_width':bar_width,
        'panel_height':panel_height,
        'panel_y':panel_y,
        'message_x':message_x,
        'message_width':message_width,
        'message_height':message_height,
        'map_width':map_width,
        'map_height':map_height,
        'room_max_size':room_max_size,
        'room_min_size':room_min_size,
        'max_rooms':max_rooms,
        'fov_algorithm':fov_algorithm,
        'fov_light_walls':fov_light_walls,
        'fov_radius':fov_radius,
        'max_enemies_per_room':max_enemies_per_room,
        'max_items_per_room':max_items_per_room,
        'colours':colours
    }

    return constants

def get_game_variables(constants):
    fighter_component=Fighter(health=100,defense=1,power=2)
    inventory_component=Inventory(26)
    level_component=Level()
    equipment_component=Equipment()
    player=Entity(0,0,'@',lc.white,'Player',blocks=True,render_order=RenderOrder.ACTOR,fighter=fighter_component,inventory=inventory_component,level=level_component,equipment=equipment_component)

    entities=[player]

    equip_component=Equip(EquipSlots.MAIN_HAND,power_bonus=2)
    dagger=Entity(0,0,'i',lc.sky,'Dagger',equip=equip_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    game_map=GameMap(constants['map_width'],constants['map_height'])
    game_map.make_map(constants['max_rooms'],constants['room_min_size'],constants['room_max_size'],constants['map_width'],
                    constants['map_height'],player,entities)

    message_log=MessageLog(constants['message_x'],constants['message_width'],constants['message_height'])

    game_state=GameStates.PLAYER_TURN

    return player,entities,game_map,message_log,game_state