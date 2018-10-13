from equipslots import EquipSlots
from components.equip import Equip

class Equipment:
    def __init__(self,head=None,neck=None,chest=None,hands=None,ring=None,main_hand=None,off_hand=None,legs=None,feet=None):
        self.head=head
        self.neck=neck
        self.chest=chest
        self.hands=hands
        self.ring=ring
        self.main_hand=main_hand
        self.off_hand=off_hand
        self.legs=legs
        self.feet=feet

    @property
    def health_bonus(self):
        bonus=0
        if self.head:
            bonus+=self.head.health_bonus
        if self.neck:
            bonus+=self.neck.health_bonus        
        if self.chest:
            bonus+=self.chest.health_bonus
        if self.hands:
            bonus+=self.hands.health_bonus
        if self.ring:
            bonus+=self.ring.health_bonus        
        if self.main_hand:
            bonus+=self.main_hand.health_bonus
        if self.off_hand:
            bonus+=self.off_hand.health_bonus
        if self.legs:
            bonus+=self.legs.health_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus=0
        if self.head:
            bonus+=self.head.power_bonus
        if self.neck:
            bonus+=self.neck.power_bonus        
        if self.chest:
            bonus+=self.chest.power_bonus
        if self.hands:
            bonus+=self.hands.power_bonus
        if self.ring:
            bonus+=self.ring.power_bonus        
        if self.main_hand:
            bonus+=self.main_hand.power_bonus
        if self.off_hand:
            bonus+=self.off_hand.power_bonus
        if self.legs:
            bonus+=self.legs.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus=0
        if self.head:
            bonus+=self.head.defense_bonus
        if self.neck:
            bonus+=self.neck.defense_bonus        
        if self.chest:
            bonus+=self.chest.defense_bonus
        if self.hands:
            bonus+=self.hands.defense_bonus
        if self.ring:
            bonus+=self.ring.defense_bonus        
        if self.main_hand:
            bonus+=self.main_hand.defense_bonus
        if self.off_hand:
            bonus+=self.off_hand.defense_bonus
        if self.legs:
            bonus+=self.legs.defense_bonus

        return bonus
        
    def to_json(self):

        json_data={}
        if self.head:
            json_data['head']=self.head.to_json()
        if self.neck:
            json_data['neck']=self.neck.to_json()
        if self.chest:
            json_data['chest']=self.chest.to_json()
        if self.hands:
            json_data['hands']=self.hands.to_json()
        if self.ring:
            json_data['ring']=self.ring.to_json()
        if self.main_hand:
            json_data['main_hand']=self.main_hand.to_json()
        if self.off_hand:
            json_data['off_hand']=self.off_hand.to_json()
        if self.legs:
            json_data['legs']=self.legs.to_json()
        
        return json_data


    @staticmethod
    def from_json(json_data):
        head_json=json_data.get('head')
        neck_json=json_data.get('neck')
        chest_json=json_data.get('chest')
        hands_json=json_data.get('hands')
        ring_json=json_data.get('ring')
        main_hand_json=json_data.get('main_hand')
        off_hand_json=json_data.get('off_hand')
        legs_json=json_data.get('legs')

        equipment=Equipment()
        if head_json:
            equipment.head=Equip.from_json(head_json)
        if neck_json:
            equipment.neck=Equip.from_json(neck_json)
        if chest_json:
            equipment.chest=Equip.from_json(chest_json)
        if hands_json:
            equipment.hands=Equip.from_json(hands_json)
        if ring_json:
            equipment.ring=Equip.from_json(ring_json)
        if main_hand_json:
            equipment.main_hand=Equip.from_json(main_hand_json)
        if off_hand_json:
            equipment.off_hand=Equip.from_json(off_hand_json)
        if legs_json:
            equipment.legs=Equip.from_json(legs_json)
        return equipment



    def toggle_equip(self,equip_entity):
        results=[]
        
        slot=equip_entity.equip.slot

        if slot==EquipSlots.MAIN_HAND:
            if self.main_hand==equip_entity:
                self.main_hand=None
                results.append({'dequipped':equip_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped':self.main_hand})

                self.main_hand=equip_entity
                results.append({'equipped':equip_entity})
        elif slot==EquipSlots.OFF_HAND:
            if self.off_hand==equip_entity:
                self.off_hand=None
                results.append({'dequipped':equip_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped':self.off_hand})

                    self.main_hand=equip_entity
                    results.append({'equipped':equip_entity})

        return results

    
