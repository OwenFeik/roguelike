import libtcodpy as lc
from gamestates import GameStates
from renderfunctions import RenderOrder
from gamemessages import Message

def kill_player(player):
    player.char='%'
    player.colour=lc.dark_red
    player.name='player\'s corpse'

    return Message('You died!',lc.red), GameStates.PLAYER_DEAD

def kill_enemy(enemy):
    death_message=Message('{0} dies!'.format(enemy.name.capitalize()),lc.orange)

    enemy.char='%'
    enemy.colour=lc.dark_red
    enemy.blocks=False
    enemy.fighter=None
    enemy.ai=None
    enemy.name='remains of '+enemy.name
    enemy.render_order=RenderOrder.CORPSE

    return death_message