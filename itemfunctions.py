import libtcodpy as lc
from gamemessages import Message
from components.ai import ConfusedMonster

def heal(*args,**kwargs):
    entity=args[0]
    amount=kwargs.get('amount')

    results=[]

    if entity.fighter.health==entity.fighter.max_health:
        results.append({'consumed':False,'message':Message('You are already at full health.',lc.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed':True,'message':Message('Your wounds start to feel better!',lc.green)})
    
    return results

def cast_lightning(*args,**kwargs):
    caster=args[0]
    entities=kwargs.get('entities')
    fov_map=kwargs.get('fov_map')
    damage=kwargs.get('damage')
    maximum_range=kwargs.get('maximum_range')

    results=[]

    target=None
    closest_distance=maximum_range+1

    for entity in entities:
        if entity.fighter and entity != caster and lc.map_is_in_fov(fov_map,entity.x,entity.y):
            distance=caster.distance_to(entity)

            if distance<closest_distance:
                target=entity
                closest_distance=distance

    if target:
        results.append({'consumed':True,'target':target,'message':Message('A lightning bolt strikes {0} for {1} damage.'.format(target.name,damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed':False,'target':None,'message':Message('No enemy is close enough to strike.',lc.red)})
    
    return results

def cast_fireball(*args,**kwargs):
    entities=kwargs.get('entities')
    fov_map=kwargs.get('fov_map')
    damage=kwargs.get('damage')
    radius=kwargs.get('radius')
    target_x=kwargs.get('target_x')
    target_y=kwargs.get('target_y')

    results=[]

    if not lc.map_is_in_fov(fov_map,target_x,target_y):
        results.append({'consumed':False,'message':Message('You cannot target a tile you can\'t see.',lc.yellow)})
        return results
    results.append({'consumed':True,'message':Message('The fireball explodes, burning everything within {0} tiles!'.format(radius),lc.orange)})

    for entity in entities:
        if entity.distance(target_x,target_y)<=radius and entity.fighter:
            results.append({'message':Message('{0} is burned for {1} damage.'.format(entity.name,damage),lc.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse(*args,**kwargs):
    entities=kwargs.get('entities')
    fov_map=kwargs.get('fov_map')
    target_x=kwargs.get('target_x')
    target_y=kwargs.get('target_y')

    results=[]

    if not lc.map_is_in_fov(fov_map,target_x,target_y):
        results.append({'consumed':False,'message':Message('You cannot target you cannot see.',lc.yellow)})
        return results
    
    for entity in entities:
        if entity.x==target_x and entity.y==target_y and entity.ai:
            confused_ai=ConfusedMonster(entity.ai,10)
            confused_ai.owner=entity
            entity.ai=confused_ai

            results.append({'consumed':True,'message':Message('The eyes of the {0} look vacant as he begins to stumble around.'.format(entity.name),lc.green)})

            break
    else:
        results.append({'consumed':False,'message':Message('There is no targetable enemy at the location.',lc.yellow)})
    
    return results