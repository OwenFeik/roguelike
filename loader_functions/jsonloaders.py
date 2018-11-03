import json
import libtcodpy as lc

from entity import Entity #Load in entities from savegame and initialise enemies and items
from gamemessages import MessageLog #Load messagelog from savegame
from gamestates import GameStates #Load gamestate from savegame
from map_objects.gamemap import GameMap #Load gamemap from savegame
from map_objects.tile import Tile #Initialise tiles from json
from menus import loading_bar #Show save progress

def json_save_game(player,entities,game_map,message_log,game_state,con,screen_width,screen_height):
    loading_bar(con,'Saving entities...',.1,screen_width,screen_height) #Show loading bar
    lc.console_flush()
    
    player_index=entities.index(player) #Get player index
    entities_json=[entity.to_json() for entity in entities] #JSON-ise all entities 
    
    loading_bar(con,'Saving map...',.3,screen_width,screen_height) #Update loading bar
    lc.console_flush()
    
    game_map_json=game_map.to_json() #JSON-ise map
    
    loading_bar(con,'Saving messages...',.6,screen_width,screen_height) #Update loading bar
    lc.console_flush()
    
    message_log_json=message_log.to_json() #JSON-ise messages

    #Organise data to write
    data={
        'player_index':player_index,
        'entities':entities_json,
        'game_map':game_map_json,
        'message_log':message_log_json,
        'game_state':game_state.value
    }


    loading_bar(con,'Saving file...',.7,screen_width,screen_height) #Final loading bar update
    lc.console_flush()
    
    with open('savegames/save_game.json','w') as save_file: #Write JSON data to file
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

def json_get_enemy(enemy):
    with open('resources/enemies.json','r') as f:
        enemies=json.load(f)
        found_enemy=enemies[enemy]
        #Need these to initialise entity from JSON
        found_enemy['x']=0
        found_enemy['y']=0
        return Entity.from_json(found_enemy)

def json_get_item(item):
    with open('resources/items.json','r') as f:
        items=json.load(f)
        found_item=items[item]
        #Need these to initialise entity from JSON
        found_item['x']=0
        found_item['y']=0
        return Entity.from_json(found_item)

# def json_get_tile(preset):
#     with open('resources/tiles.json','r') as f:
#         tiles=json.load(f)
#         return Tile.from_json(tiles[preset])