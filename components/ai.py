import libtcodpy as lc
from random import randint
from gamemessages import Message

class BasicMonster:
    def take_turn(self,target,fov_map,game_map,entities):
        results=[]
        
        enemy=self.owner
        if lc.map_is_in_fov(fov_map,enemy.x,enemy.y):
            if enemy.distance_to(target)>=2:
                enemy.move_astar(target,entities,game_map)
            elif target.fighter.health>0:
                attack_results=enemy.fighter.attack(target)
                results.extend(attack_results)
        
        return results

class ConfusedMonster:
    def __init__(self,previous_ai,number_of_turns):
        self.previous_ai=previous_ai
        self.number_of_turns=number_of_turns
    
    def take_turn(self,target,fov_map,game_map,entities):
        results=[]

        if self.number_of_turns>0:
            random_x=self.owner.x+randint(0,2)-1
            random_y=self.owner.y+randint(0,2)-1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x,random_y,game_map,entities)
            
            self.number_of_turns-=1
        else:
            self.owner.ai=self.previous_ai
            results.append({'message':Message('The {0} is no longer confused!'.format(self.owner.name),lc.red)})

        return results