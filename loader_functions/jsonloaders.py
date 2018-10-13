import json
import libtcodpy as lc

from entity import Entity
from gamemessages import MessageLog
from gamestates import GameStates
from map_objects.gamemap import GameMap

def json_save_game(player,entities,game_map,message_log,game_state):
    data={
        'player_index':entities.index(player),
        'entities':[entity.to_json() for entity in entities],
        'game_map':game_map.to_json(),
        'message_log':message_log.to_json(),
        'game_state':game_state.value
    }
    with open('savegames/save_game.json','w') as save_file:
        json.dump(data,save_file,indent=4)

def json_load_game():
    with open('savegames/save_game.json','r') as save_file:
        data=json.load(save_file)

    player_index=data['player_index']
    entities_json=data['entities']
    game_map_json=data['game_map']
    message_log_json=data['message_log']
    game_state_json=data['game_state']

    entities=[Entity.from_json(entity_json) for entity_json in entities_json]
    player=entities[player_index]
    game_map=GameMap.from_json(game_map_json)
    message_log=MessageLog.from_json(message_log_json)
    game_state=GameStates(game_state_json)

    return player,entities,game_map,message_log,game_state

def json_get_constants():
    with open('resources/constants.json','r') as constants_file:
        constants=json.load(constants_file)
    with open('resources/colours.json','r') as colours_file:
        colours_json=json.load(colours_file)
    
    colours={}
    for colour in colours_json:
        colours[colour]=lc.Color(colours_json[colour][0],colours_json[colour][1],colours_json[colour][2])
    constants['colours']=colours
    
    return constants