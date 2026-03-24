class Skill:
    def __init__(self, name, description, effect, is_acquired, quantity=0, attribute="none", prereqs=None):
        self.name = name
        self.description = description
        self.effect = effect
        self.quantity = quantity
        self.attribute = attribute
        self.prerequisites = prereqs if prereqs else []
        self.acquired = is_acquired

class SkillTree:
    def __init__(self, name, total_number, abilities_list: list[Skill], is_exhausted = False):
        self.name = name
        self.total_number = total_number
        self.abilities_list = abilities_list
        self.is_exhausted = is_exhausted


def apply_ability(skill, receiver):
    if skill.effect == "addition":
        if skill.attribute == "BULLET_SIZE":
            receiver.bullet_size_doubled_activated = True
        elif skill.attribute == "max_hp":
            old_val = getattr(receiver, skill.attribute)
            
            setattr(receiver, skill.attribute, old_val+skill.quantity)

            # Current hp gets addition if max_hp is increased
            receiver.current_hp = min(receiver.max_hp, receiver.current_hp+1)
        elif skill.attribute == "max_shield":
            old_val = getattr(receiver, skill.attribute)
            
            setattr(receiver, skill.attribute, old_val+skill.quantity)
            
            # Current shield gets addition if max_shield is increased
            receiver.current_shield = min(receiver.max_shield, receiver.current_shield+1)
        else:    
            old_val = getattr(receiver, skill.attribute)
            
            setattr(receiver, skill.attribute, old_val+skill.quantity)
    elif skill.effect == "percentage":
        if skill.attribute == "fire_rate":
            old_val = getattr(receiver, skill.attribute)
            
            setattr(receiver, skill.attribute, old_val-(old_val*skill.quantity))
        else:
            old_val = getattr(receiver, skill.attribute)
            
            setattr(receiver, skill.attribute, old_val+(old_val*skill.quantity))
    elif skill.effect == "state":
        setattr(receiver, skill.attribute, True)

############################
# Count: 5
############################
sw1 = Skill("Swift fire I", "Fire rate +25%", "percentage", False, quantity=.25, attribute="fire_rate")
sw2 = Skill("Swift fire II", "Fire rate +10%", "percentage", False, quantity=.10, prereqs=[sw1], attribute="fire_rate")
sw3 = Skill("Swift fire III", "Fire rate +10%", "percentage", False, quantity=.10, prereqs=[sw1, sw2], attribute="fire_rate")
sw4 = Skill("Swift fire IV", "Fire rate +10%", "percentage", False, quantity=.10, prereqs=[sw1, sw2, sw3], attribute="fire_rate")
sw5 = Skill("Swift fire V", "Fire rate +30% (maxed out)", "percentage", False, quantity=.30, prereqs=[sw1, sw2, sw3, sw4], attribute="fire_rate")

# Swift fire skill tree
swift_fire_skill_tree = SkillTree("Swift fire tree", 5, [sw1,sw2,sw3,sw4,sw5])

fb1 = Skill("Fast Bullet I", "Bullet speed +20%", "percentage", False, quantity=.20, attribute="bullet_speed")
fb2 = Skill("Fast Bullet II", "Bullet speed +10%", "percentage", False, quantity=.10, prereqs=[fb1], attribute="bullet_speed")
fb3 = Skill("Fast Bullet III", "Bullet speed +10%", "percentage", False, quantity=.10, prereqs=[fb1, fb2], attribute="bullet_speed")
fb4 = Skill("Fast Bullet IV", "Bullet speed +10%", "percentage", False, quantity=.10, prereqs=[fb1, fb2, fb3], attribute="bullet_speed")
fb5 = Skill("Fast Bullet V", "Bullet speed +10% (maxed out)", "percentage", False, quantity=.10, prereqs=[fb1, fb2, fb3, fb4], attribute="bullet_speed")

# Fast bullet skill tree
fast_bullet_skill_tree = SkillTree("Fast bullet tree", 5, [fb1,fb2,fb3,fb4,fb5])

hp1 = Skill("Increase max hp I", "Max hp +1", "addition", False, quantity=1, attribute="max_hp")
hp2 = Skill("Increase max hp II", "Max hp +1", "addition", False, quantity=1, prereqs=[hp1], attribute="max_hp")
hp3 = Skill("Increase max hp III", "Max hp +1", "addition", False, quantity=1, prereqs=[hp1, hp2], attribute="max_hp")
hp4 = Skill("Increase max hp IV", "Max hp +1", "addition", False, quantity=1, prereqs=[hp1, hp2, hp3], attribute="max_hp")
hp5 = Skill("Increase max hp V", "Max hp +1", "addition", False, quantity=1, prereqs=[hp1, hp2, hp3, hp4], attribute="max_hp")

# HP skill tree
hp_skill_tree = SkillTree("Max hp tree", 5, [hp1,hp2,hp3,hp4,hp5])


############################
# Count: 4
############################
ms1 = Skill("Movement speed I", "Movement speed +10%", "percentage", False, quantity=.10, attribute="movement_speed")
ms2 = Skill("Movement speed II", "Movement speed +10%", "percentage", False, quantity=.10, prereqs=[ms1], attribute="movement_speed")
ms3 = Skill("Movement speed III", "Movement speed +10%", "percentage", False, quantity=.10, prereqs=[ms1, ms2], attribute="movement_speed")
ms4 = Skill("Movement speed IV", "Movement speed +10% (maxed out)", "percentage", False, quantity=.10, prereqs=[ms1, ms2, ms3], attribute="movement_speed")

# Movement speed skill tree
movement_speed_skill_tree = SkillTree("Movement speed tree", 4, [ms1,ms2,ms3,ms4])


############################
# Count: 3
############################
bd1 = Skill("Bullet damage I", "Bullet damage +5", "addition", False, quantity=5, attribute="damage")
bd2 = Skill("Bullet damage II", "Bullet damage +5", "addition", False, quantity=5, prereqs=[bd1], attribute="damage")
bd3 = Skill("Bullet damage III", "Bullet damage +10 (maxed out)", "addition", False, quantity=10, prereqs=[bd1, bd2], attribute="damage")

# Bullet damage skill tree
bullet_damage_skill_tree = SkillTree("Bullet damage tree", 3, [bd1, bd2, bd3])

pb1 = Skill("Piercing bullet I", "Bullet pierce +1", "addition", False, quantity=1, attribute="bullet_pierce_number")
pb2 = Skill("Piercing bullet II", "Bullet pierce +1", "addition", False, quantity=1, prereqs=[pb1], attribute="bullet_pierce_number")
pb3 = Skill("Piercing bullet III", "Bullet pierce +1", "addition", False, quantity=1, prereqs=[pb1, pb2], attribute="bullet_pierce_number")

# Bullet pierce skill tree
bullet_pierce_skill_tree = SkillTree("Bullet pierce tree", 3, [pb1, pb2, pb3])

bb1 = Skill("Bullet bounce I", "Bullet bounce +1", "addition", False, quantity=1, attribute="bullet_bounce_number")
bb2 = Skill("Bullet bounce II", "Bullet bounce +1", "addition", False, quantity=1, prereqs=[bb1], attribute="bullet_bounce_number")
bb3 = Skill("Bullet bounce III", "Bullet bounce +1", "addition", False, quantity=1, prereqs=[bb1, bb2], attribute="bullet_bounce_number")

# Bullet bounce skill tree
bullet_bounce_skill_tree = SkillTree("Bullet bounce tree", 3, [bb1, bb2, bb3])

s1 = Skill("Shield I", "Max shield +1 (Shield regenerates every 2 minutes)", "addition", False, quantity=1, attribute="max_shield")
s2 = Skill("Shield II", "Max shield +1 (Shield regenerates every 2 minutes)", "addition", False, quantity=1, prereqs=[s1], attribute="max_shield")
s3 = Skill("Shield III", "Max shield +1 (Shield regenerates every 2 minutes)", "addition", False, quantity=1, prereqs=[s1, s2], attribute="max_shield")

# Shield skill tree
shield_skill_tree = SkillTree("Shield tree", 3, [s1, s2, s3])

############################
# Count: 2
############################
proj1 = Skill("Projectile increase I", "Projectile +1", "addition", False, quantity=1, attribute="bullet_number")
proj2 = Skill("Projectile increase II", "Projectile +1", "addition", False, quantity=1, prereqs=[proj1], attribute="bullet_number")

# Projectile skill tree
projectile_skill_tree = SkillTree("Projectile tree", 2, [proj1, proj2])

############################
# Count: 1
############################
sdtime = Skill("Slow down time I", "Slow down time when enemies' projectiles are near player", "state", False, attribute="slow_time_active")

# Slow down skill tree
slow_down_skill_tree = SkillTree("Slow down tree", 1, [sdtime])

negate = Skill("Projectile negation I", "Spawn object that orbits around player that negates enemies' projectiles", "state", False, attribute="negator_active")

# Projectile negation skill tree
projectile_negation_skill_tree = SkillTree("Projectile negation tree", 1, [negate])

bsize = Skill("Bullet size increase I", "Increase bullet size 2x", "addition", False, attribute="BULLET_SIZE")

# Bullet size increase skill tree
bullet_size_skill_tree = SkillTree("Bullet size tree", 1, [bsize])

bexp = Skill("Bullet explosion I", "Player's bullets explodes when enemies are hit", "state", False, attribute="bullets_explode_state")

# Bullet explosion skill tree
bullet_explosion_skill_tree = SkillTree("Bullet explosion tree", 1, [bexp])