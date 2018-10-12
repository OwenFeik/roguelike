from equipslots import EquipSlots

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
        if self.head and self.head.equip:
            bonus+=self.head.equip.health_bonus
        if self.neck and self.neck.equip:
            bonus+=self.neck.equip.health_bonus        
        if self.chest and self.chest.equip:
            bonus+=self.chest.equip.health_bonus
        if self.hands and self.hands.equip:
            bonus+=self.hands.equip.health_bonus
        if self.ring and self.ring.equip:
            bonus+=self.ring.equip.health_bonus        
        if self.main_hand and self.main_hand.equip:
            bonus+=self.main_hand.equip.health_bonus
        if self.off_hand and self.off_hand.equip:
            bonus+=self.off_hand.equip.health_bonus
        if self.legs and self.legs.equip:
            bonus+=self.legs.equip.health_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus=0
        if self.head and self.head.equip:
            bonus+=self.head.equip.power_bonus
        if self.neck and self.neck.equip:
            bonus+=self.neck.equip.power_bonus        
        if self.chest and self.chest.equip:
            bonus+=self.chest.equip.power_bonus
        if self.hands and self.hands.equip:
            bonus+=self.hands.equip.power_bonus
        if self.ring and self.ring.equip:
            bonus+=self.ring.equip.power_bonus        
        if self.main_hand and self.main_hand.equip:
            bonus+=self.main_hand.equip.power_bonus
        if self.off_hand and self.off_hand.equip:
            bonus+=self.off_hand.equip.power_bonus
        if self.legs and self.legs.equip:
            bonus+=self.legs.equip.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus=0
        if self.head and self.head.equip:
            bonus+=self.head.equip.defense_bonus
        if self.neck and self.neck.equip:
            bonus+=self.neck.equip.defense_bonus        
        if self.chest and self.chest.equip:
            bonus+=self.chest.equip.defense_bonus
        if self.hands and self.hands.equip:
            bonus+=self.hands.equip.defense_bonus
        if self.ring and self.ring.equip:
            bonus+=self.ring.equip.defense_bonus        
        if self.main_hand and self.main_hand.equip:
            bonus+=self.main_hand.equip.defense_bonus
        if self.off_hand and self.off_hand.equip:
            bonus+=self.off_hand.equip.defense_bonus
        if self.legs and self.legs.equip:
            bonus+=self.legs.equip.defense_bonus

        return bonus
        

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

    
