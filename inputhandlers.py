import libtcodpy as lc
from gamestates import GameStates

def handle_keys(key,game_state):
    if game_state==GameStates.PLAYER_TURN:
        return handle_player_turn_keys(key)
    elif game_state==GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state==GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY,GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    elif game_state==GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state==GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    return {}


def handle_mouse(mouse):
    (x,y)=(mouse.cx,mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click':(x,y)}
    elif mouse.rbutton_pressed:
        return {'right_click':(x,y)}
    return {}

def handle_targeting_keys(key):
    if key.vk==lc.KEY_ESCAPE:
        return {'exit':True}
    return {}

def handle_player_turn_keys(key):
    key_char=chr(key.c)

    if key.vk==lc.KEY_UP or key_char=='w':
        return {'move':(0,-1)}
    elif key.vk==lc.KEY_DOWN or key_char=='s':
        return {'move':(0,1)}
    elif key.vk==lc.KEY_LEFT or key_char=='a':
        return {'move':(-1,0)}
    elif key.vk==lc.KEY_RIGHT or key_char=='d':
        return {'move':(1,0)}
    elif key_char=='q':
        return {'move':(-1,-1)}
    elif key_char=='e':
        return {'move':(1,-1)}
    elif key_char=='z':
        return {'move':(-1,1)}
    elif key_char=='c':
        return {'move':(1,1)}
    elif key_char=='v':
        return {'wait':True}

    if key_char=='g':
        return {'pickup':True}
    elif key_char=='i':
        return {'show_inventory':True}
    elif key_char=='f':
        return {'drop_inventory':True}
    elif key_char=='r':
        return {'show_char_screen':True}
    elif key.vk==lc.KEY_ENTER:
        return {'take_stairs':True}

    if key.vk==lc.KEY_ENTER and key.lalt:
        return {'fullscreen':True}

    if key.vk==lc.KEY_ESCAPE:
        return {'exit':True}

    return {}

def handle_player_dead_keys(key):
    key_char=chr(key.c)

    if key_char=='i':
        return {'show_inventory':True}

    if key.vk==lc.KEY_ENTER and key.lalt:
        return {'fullscreen':True}
    elif key.vk==lc.KEY_ESCAPE:
        return {'exit':True}
    
    return {}

def handle_inventory_keys(key):
    index=key.c-ord('a')

    if index>=0:
        return {'inventory_index':index}

    if key.vk==lc.KEY_ENTER and key.lalt:
        return {'fullscreen':True}
    elif key.vk==lc.KEY_ESCAPE:
        return {'exit':True}

    return {}

def handle_main_menu(key):
    key_char=chr(key.c)

    if key_char=='a':
        return {'new_game':True}
    elif key_char=='b':
        return {'load_game':True}
    elif key_char=='c' or key.vk==lc.KEY_ESCAPE:
        return {'exit':True}

    return {}

def handle_level_up_menu(key):
    if key:
        key_char=chr(key.c)

        if key_char=='a':
            return {'level_up':'hp'}
        elif key_char=='b':
            return {'level_up':'pow'}
        elif key_char=='c':
            return {'level_up':'def'}
    return {}

def handle_character_screen(key):
    if key.vk==lc.KEY_ESCAPE:
        return {'exit':True}
    return {}