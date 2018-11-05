import libtcodpy as lc
from enum import Enum,auto
from gamestates import GameStates
from menus import inventory_menu,level_up_menu,character_screen,loading_bar
from random import randint

class RenderOrder(Enum):
    STAIRS=auto()
    CORPSE=auto()
    ITEM=auto()
    ACTOR=auto()

def get_names_under_mouse(mouse,entities,fov_map):
    (x,y)=(mouse.cx,mouse.cy)

    names=[entity.name for entity in entities
    if entity.x==x and entity.y==y and lc.map_is_in_fov(fov_map,entity.x,entity.y)]

    names=', '.join(names)
    return names.capitalize()


def render_bar(panel,x,y,total_width,name,value,maximum,bar_colour,back_colour):
    bar_width=int(float(value)/maximum*total_width)

    lc.console_set_default_background(panel,back_colour)
    lc.console_rect(panel,x,y,total_width,1,False,lc.BKGND_SCREEN)

    lc.console_set_default_background(panel,bar_colour)
    if bar_width>0:
        lc.console_rect(panel,x,y,bar_width,1,False,lc.BKGND_SCREEN)
    
    lc.console_set_default_foreground(panel,lc.white)
    lc.console_print_ex(panel,int(x+total_width/2),y,lc.BKGND_NONE,lc.CENTER,'{0}: {1}/{2}'.format(name,value,maximum))

def render_all(con,panel,game_map,entities,player,fov_map,fov_recompute,message_log,screen_width,screen_height,bar_width,panel_height,panel_y,mouse,tile_data,game_state):
    
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible=lc.map_is_in_fov(fov_map,x,y)
                wall=game_map.tiles[x][y].block_sight

                if visible:
                    lc.console_set_char_background(con,x,y,tile_data.get(game_map.tiles[x][y].terrain)['light'],lc.BKGND_SET)
                    lc.console_set_char_foreground(con,x,y,tile_data.get(game_map.tiles[x][y].terrain)['dark'])
                    lc.console_set_char(con,x,y,chr(game_map.tiles[x][y].texture))
                    game_map.tiles[x][y].explored=True
                elif game_map.tiles[x][y].explored:
                    lc.console_set_char_background(con,x,y,tile_data.get(game_map.tiles[x][y].terrain)['dark'],lc.BKGND_SET)
                    lc.console_set_char_foreground(con,x,y,lc.black)

    entities_in_render_order=sorted(entities,key=lambda x:x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con,entity,fov_map,game_map)
    
    lc.console_blit(con,0,0,screen_width,screen_height,0,0,0)

    lc.console_set_default_background(panel,lc.black)
    lc.console_clear(panel)

    y=1
    for message in message_log.messages:
        lc.console_set_default_foreground(panel,message.colour)
        lc.console_print_ex(panel,message_log.x,y,lc.BKGND_NONE,lc.LEFT,message.text)
        y+=1
        
    render_bar(panel,1,1,bar_width,'HP',player.fighter.health,player.fighter.max_health,lc.red,lc.darker_red)
    lc.console_print_ex(panel,1,3,lc.BKGND_NONE,lc.LEFT,'Dungeon Level: {0}'.format(game_map.floor))

    lc.console_set_default_background(panel,lc.light_gray)
    lc.console_print_ex(panel,1,0,lc.BKGND_NONE,lc.LEFT,get_names_under_mouse(mouse,entities,fov_map))

    lc.console_blit(panel,0,0,screen_width,panel_height,0,0,panel_y)

    if game_state in (GameStates.SHOW_INVENTORY,GameStates.DROP_INVENTORY):
        if game_state==GameStates.SHOW_INVENTORY:
            inventory_title='Press the key next to an item to use it or Esc to cancel.\n'
        else:
            inventory_title='Press the key next to an item to drop it or Esc to cancel. \n'
            
        inventory_menu(con,inventory_title,player,50,screen_width,screen_height)
    elif game_state==GameStates.LEVEL_UP:
        level_up_menu(con,'Level up! Choose a stat to raise:',player,40,screen_width,screen_height)
    elif game_state==GameStates.CHARACTER_SCREEN:
        character_screen(player,30,10,screen_width,screen_height)

def clear_all(con,entities):
    for entity in entities:
        clear_entity(con,entity)

def draw_entity(con,entity,fov_map,game_map):
    if lc.map_is_in_fov(fov_map,entity.x,entity.y):
        lc.console_set_default_foreground(con,entity.colour)
        lc.console_put_char(con,entity.x,entity.y,entity.char,lc.BKGND_NONE)
    elif entity.stairs and game_map.tiles[entity.x][entity.y].explored:
        dim_colour=lc.Color(entity.colour.r//2,entity.colour.g//2,entity.colour.b//2)
        lc.console_set_default_foreground(con,dim_colour)
        lc.console_put_char(con,entity.x,entity.y,entity.char,lc.BKGND_NONE)

def clear_entity(con,entity):
    lc.console_put_char(con,entity.x,entity.y,' ',lc.BKGND_NONE)