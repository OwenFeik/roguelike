#TODO: refactor bonus calculations to iterate

from equipslots import EquipSlots

class Equipment:
    def __init__(self,main_hand=None,off_hand=None):
        self.main_hand=main_hand
        self.off_hand=off_hand


    @property
    def health_bonus(self):
        bonus=0
        if self.main_hand and self.main_hand.equip:
            bonus+=self.main_hand.equip.health_bonus
        if self.off_hand and self.off_hand.equip:
            bonus+=self.off_hand.equip.health_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus=0
        if self.main_hand and self.main_hand.equip:
            bonus+=self.main_hand.equip.power_bonus
        if self.off_hand and self.off_hand.equip:
            bonus+=self.off_hand.equip.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus=0
        if self.main_hand and self.main_hand.equip:
            bonus+=self.main_hand.equip.defense_bonus
        if self.off_hand and self.off_hand.equip:
            bonus+=self.off_hand.equip.defense_bonus

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

    
