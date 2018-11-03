import libtcodpy as lc

def menu(con,header,options,width,screen_width,screen_height):
    if len(options)>26: 
        raise ValueError('Maximum of 26 options in menu')
    
    header_height=lc.console_get_height_rect(con,0,0,width,screen_height,header)
    height=len(options)+header_height

    window=lc.console_new(width,height)

    lc.console_set_default_foreground(window,lc.white)
    lc.console_print_rect_ex(window,0,0,width,height,lc.BKGND_NONE,lc.LEFT,header)

    y=header_height
    letter_index=ord('a')
    for option_text in options:
        text='('+chr(letter_index)+')'+option_text
        lc.console_print_ex(window,0,y,lc.BKGND_NONE,lc.LEFT,text)
        y+=1
        letter_index+=1

    x=int(screen_width/2 - width/2)
    y=int(screen_height/2 - height/2)
    
    lc.console_blit(window,0,0,width,height,0,x,y,1.0,0.7)

def inventory_menu(con,header,player,inventory_width,screen_width,screen_height):
    if len(player.inventory.items)==0:
        options=['Inventory is empty.']
    else:
        options=[]

        for item in player.inventory.items:
            if player.equipment.main_hand==item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand==item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)
    menu(con,header,options,inventory_width,screen_width,screen_height)

def main_menu(con,background_image,screen_width,screen_height):
    lc.image_blit_2x(background_image,0,0,0)

    lc.console_set_default_foreground(0,lc.yellow)
    lc.console_print_ex(0,int(screen_width/2),int(screen_height/2)-4,lc.BKGND_NONE,lc.CENTER,'roguelike')
    lc.console_print_ex(0,int(screen_width/2)+7,int(screen_height/2)-1,lc.BKGND_NONE,lc.CENTER,'by owen')

    menu(con,'',['New game','Continue','Quit'],24,screen_width,screen_height)

def level_up_menu(con,header,player,menu_width,screen_width,screen_height):
    options=['Constitution (+20 hp, from {0})'.format(player.fighter.max_health),
            'Strength (+1 attack, from {0})'.format(player.fighter.power),
            'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con,header,options,menu_width,screen_width,screen_height)

def message_box(con,header,width,screen_width,screen_height):
    menu(con,header,[],width,screen_width,screen_height)

def character_screen(player,character_screen_width,character_screen_height,screen_width,screen_height):
    window=lc.console_new(character_screen_width,character_screen_height)

    lc.console_set_default_foreground(window,lc.white)

    lc.console_print_rect_ex(window,0,1,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Character Information')

    lc.console_print_rect_ex(window,0,2,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Level: {0}'.format(player.level.current_level))
    lc.console_print_rect_ex(window,0,3,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Experience: {0}'.format(player.level.current_xp))
    lc.console_print_rect_ex(window,0,4,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Experince to next: {0}'.format(player.level.experience_to_next_level))
    lc.console_print_rect_ex(window,0,6,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Maximum health: {0}'.format(player.fighter.max_health))
    lc.console_print_rect_ex(window,0,7,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Power: {0}'.format(player.fighter.power))
    lc.console_print_rect_ex(window,0,8,character_screen_width,character_screen_height,lc.BKGND_NONE,lc.LEFT,'Defense: {0}'.format(player.fighter.defense))

    x=screen_width//2-character_screen_width//2
    y=screen_height//2-character_screen_height//2

    lc.console_blit(window,0,0,character_screen_width,character_screen_height,0,x,y,1.0,0.7)

def loading_bar(con,header,progress,screen_width,screen_height):
    x=screen_width//4 #Starts a quarter of the way across the screen
    y=screen_height//4 #Quarter of the way down the screen
    width=screen_width//2 #Half the width of the screen
    height=4

    window=lc.console_new(width,4) # Create loading bar window
    lc.console_set_default_foreground(window,lc.white)
    lc.console_print_rect_ex(window,0,1,screen_width//2,4,lc.BKGND_NONE,lc.LEFT,header)

    for pos in range(0,int(width*progress)): # Set achieved progress to white
        lc.console_set_char_background(window,pos,2,lc.white)
    for pos in range(int(width*progress),width): # Set remaining space to grey
        lc.console_set_char_background(window,pos,2,lc.light_grey)

    lc.console_blit(window,0,0,width,height,0,x,y,1.0,1.0) #Blit changes