import libtcodpy as lc

from loader_functions.jsonloaders import json_get_constants
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
    return json_get_constants()

def get_game_variables(constants):
    fighter_component=Fighter(health=100,defense=1,power=2)
    inventory_component=Inventory(26)
    level_component=Level()
    equipment_component=Equipment()
    player=Entity(0,0,chr(1),lc.white,'Player',blocks=True,render_order=RenderOrder.ACTOR,fighter=fighter_component,inventory=inventory_component,level=level_component,equipment=equipment_component)

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