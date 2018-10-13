from equipslots import EquipSlots

class Equip:
    def __init__(self,slot,power_bonus=0,defense_bonus=0,health_bonus=0):
        self.slot=slot
        self.power_bonus=power_bonus
        self.defense_bonus=defense_bonus
        self.health_bonus=health_bonus

    def to_json(self):
        json_data={
            'slot':self.slot.value,
            'power_bonus':self.power_bonus,
            'defense_bonus':self.defense_bonus,
            'health_bonus':self.health_bonus
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        slot=EquipSlots(json_data.get('slot'))
        power_bonus=json_data.get('power_bonus')
        defense_bonus=json_data.get('defense_bonus')
        health_bonus=json_data.get('health_bonus')

        return Equip(slot,power_bonus,defense_bonus,health_bonus)