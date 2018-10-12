import libtcodpy as lc
from gamemessages import Message

class Fighter:
    def __init__(self,health,defense,power,xp=0):
        self.base_max_health=health
        self.health=health
        self.base_defense=defense
        self.base_power=power
        self.xp=xp

    @property
    def max_health(self):
        if self.owner and self.owner.equipment:
            bonus=self.owner.equipment.health_bonus
        else:
            bonus=0
        
        return self.base_max_health+bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus=self.owner.equipment.power_bonus
        else:
            bonus=0
        
        return self.base_power+bonus
    
    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus=self.owner.equipment.defense_bonus
        else:
            bonus=0
        
        return self.base_defense+bonus

    def to_json(self):
        json_data={
            'base_max_health':self.base_max_health,
            'health':self.health,
            'base_defense':self.base_defense,
            'base_power':self.base_power,
            'xp':self.xp
        }

    @staticmethod
    def from_json(json_data):
        base_max_health=json_data.get('base_max_health')
        health=json_data.get('health')
        base_defense=json_data.get('base_defense')
        base_power=json_data.get('base_power')
        xp=json_data.get('xp')
        
        fighter_component=Fighter(base_max_health,base_defense,base_power,xp)
        fighter_component.health=health
        
        return fighter_component

    def take_damage(self,amount):
        results=[]

        self.health-=amount

        if self.health <= 0:
            results.append({'dead':self.owner,'xp':self.xp})

        return results

    def heal(self,amount):
        self.health+=amount
        
        if self.health>=self.max_health:
            self.health=self.max_health

    def attack(self,target):
        results=[]

        damage=self.power-target.fighter.defense

        if damage>0:
            results.append({'message':Message("{0} attacks {1} for {2} points of damage.".format(self.owner.name.capitalize(),target.name,str(damage)),
            lc.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message':Message("{0} attacks {1} but does no damage.".format(self.owner.name.capitalize(),target.name),lc.white)})

        return results
        
