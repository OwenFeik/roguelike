import libtcodpy as lc
import entity
from gamemessages import Message


class Inventory:
    def __init__(self,capacity):
        self.capacity=capacity
        self.items=[]

    def to_json(self):
        json_data={
            'capacity':self.capacity,
            'items':[item.to_json() for item in self.items]
        }
        return json_data

    @staticmethod
    def from_json(json_data):
        capacity=json_data.get('capacity')
        items=[entity.Entity.from_json(item) for item in json_data.get('items')]
        inventory=Inventory(capacity)
        inventory.items=items
        return inventory

    def add_item(self,item):
        results=[]

        if len(self.items)>=self.capacity:
            results.append({
                'item_added':None,
                'message':Message('You cannot carry any more, your inventory is full.',lc.yellow)
            })
        else:
            results.append({
                'item_added':item,
                'message':Message('You pick up the {0}!'.format(item.name),lc.blue)
            })
            self.items.append(item)
        
        return results

    def remove_item(self,item):
        self.items.remove(item)

    def drop_item(self,item):
        results=[]
        
        if self.owner.equipment.main_hand==item or self.owner.equipment.off_hand==item:
            self.owner.equipment.toggle_equip(item)

        item.x=self.owner.x
        item.y=self.owner.y

        self.remove_item(item)
        results.append({'item_dropped':item,'message':Message('You dropped the {0}'.format(item.name),lc.yellow)})

        return results

    def use(self,item_entity,**kwargs):
        results=[]

        item_component=item_entity.item

        if item_component.use_function is None:
            equip_component=item_entity.equip

            if equip_component:
                results.append({'equip':item_entity})
            else:
                results.append({'message':Message('The {0} cannot be used!'.format(item_entity.name),lc.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting':item_entity})
            else:
                kwargs={**item_component.function_kwargs,**kwargs}
                item_use_results=item_component.use_function(self.owner,**kwargs)

                for result in item_use_results:
                    if result.get('consumed'):
                        self.remove_item(item_entity)
                results.extend(item_use_results)

        return results