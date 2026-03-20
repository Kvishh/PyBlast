class Skill:
    def __init__(self, name, description, effect, is_acquired, category="none", prereqs=None):
        self.name = name
        self.description = description
        self.effect = effect
        self.category = category
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
        if skill.category == "BULLET_SIZE":
            receiver.bullet_size_doubled_activated = True
    elif skill.effect == "percentage":
        pass
    elif skill.effect == "state":
        pass

############################
# Count: 5
############################
sw1 = Skill("Swift fire 1", "Fire rate +25%", "percentage", False, category="shooting_cd")
sw2 = Skill("Swift fire 2", "Fire rate +10%", "percentage", False, prereqs=[sw1], category="shooting_cd")
sw3 = Skill("Swift fire 3", "Fire rate +10%", "percentage", False, prereqs=[sw1, sw2], category="shooting_cd")
sw4 = Skill("Swift fire 4", "Fire rate +10%", "percentage", False, prereqs=[sw1, sw2, sw3], category="shooting_cd")
sw5 = Skill("Swift fire 5", "Fire rate +30% (maxed out)", "percentage", False, prereqs=[sw1, sw2, sw3, sw4], category="shooting_cd")

# Swift fire skill tree
swift_fire_skill_tree = SkillTree("Swift fire tree", 5, [sw1,sw2,sw3,sw4,sw5])

fb1 = Skill("Fast Bullet 1", "Bullet speed +20%", "percentage", False, category="bullet_speed")
fb2 = Skill("Fast Bullet 2", "Bullet speed +10%", "percentage", False, prereqs=[fb1], category="bullet_speed")
fb3 = Skill("Fast Bullet 3", "Bullet speed +10%", "percentage", False, prereqs=[fb1, fb2], category="bullet_speed")
fb4 = Skill("Fast Bullet 4", "Bullet speed +10%", "percentage", False, prereqs=[fb1, fb2, fb3], category="bullet_speed")
fb5 = Skill("Fast Bullet 5", "Bullet speed +10% (maxed out)", "percentage", False, prereqs=[fb1, fb2, fb3, fb4], category="bullet_speed")

# Fast bullet skill tree
fast_bullet_skill_tree = SkillTree("Fast bullet tree", 5, [fb1,fb2,fb3,fb4,fb5])

hp1 = Skill("Max hp 1", "Max hp +1", "addition", False, category="max_hp")
hp2 = Skill("Max hp 1", "Max hp +1", "addition", False, prereqs=[hp1], category="max_hp")
hp3 = Skill("Max hp 1", "Max hp +1", "addition", False, prereqs=[hp1, hp2], category="max_hp")
hp4 = Skill("Max hp 1", "Max hp +1", "addition", False, prereqs=[hp1, hp2, hp3], category="max_hp")
hp5 = Skill("Max hp 1", "Max hp +1", "addition", False, prereqs=[hp1, hp2, hp3, hp4], category="max_hp")

# HP skill tree
hp_skill_tree = SkillTree("Max hp tree", 5, [hp1,hp2,hp3,hp4,hp5])


############################
# Count: 4
############################
ms1 = Skill("Movement speed 1", "Movement speed +10%", "percentage", False, category="movement_speed")
ms2 = Skill("Movement speed 2", "Movement speed +10%", "percentage", False, prereqs=[ms1], category="movement_speed")
ms3 = Skill("Movement speed 3", "Movement speed +10%", "percentage", False, prereqs=[ms1, ms2], category="movement_speed")
ms4 = Skill("Movement speed 4", "Movement speed +10% (maxed out)", "percentage", False, prereqs=[ms1, ms2, ms3], category="movement_speed")

# Movement speed skill tree
movement_speed_skill_tree = SkillTree("Movement speed tree", 4, [ms1,ms2,ms3,ms4])


############################
# Count: 3
############################
bd1 = Skill("Bullet damage 1", "Bullet damage +5", "addition", False, category="damage")
bd2 = Skill("Bullet damage 2", "Bullet damage +5", "addition", False, prereqs=[bd1], category="damage")
bd3 = Skill("Bullet damage 3", "Bullet damage +10 (maxed out)", "addition", False, prereqs=[bd1, bd2], category="damage")

# Bullet damage skill tree
bullet_damage_skill_tree = SkillTree("Bullet damage tree", 3, [bd1, bd2, bd3])

pb1 = Skill("Piercing bullet 1", "Bullet pierce +1", "addition", False, category="bullet_pierce_number")
pb2 = Skill("Piercing bullet 2", "Bullet pierce +1", "addition", False, prereqs=[pb1], category="bullet_pierce_number")
pb3 = Skill("Piercing bullet 3", "Bullet pierce +1", "addition", False, prereqs=[pb1, pb2], category="bullet_pierce_number")

# Bullet pierce skill tree
bullet_pierce_skill_tree = SkillTree("Bullet pierce tree", 3, [pb1, pb2, pb3])

s1 = Skill("Shield 1", "Shield +1", "addition", False, category="shield")
s2 = Skill("Shield 2", "Shield +1", "addition", False, prereqs=[s1], category="shield")
s3 = Skill("Shield 3", "Shield +1", "addition", False, prereqs=[s1, s2], category="shield")

# Shield skill tree
shield_skill_tree = SkillTree("Shield tree", 3, [s1, s2, s3])


############################
# Count: 2
############################
bb1 = Skill("Bullet bounce 1", "Bullet bounce +1", "addition", False, category="bullet_bounce_number")
bb2 = Skill("Bullet bounce 2", "Bullet bounce +1", "addition", False, prereqs=[bb1], category="bullet_bounce_number")

# Bullet bounce skill tree
bullet_bounce_skill_tree = SkillTree("Bullet bounce tree", 2, [bb1, bb2])

proj1 = Skill("Projectile increase 1", "Projectile +1", "addition", False, category="bullet_number")
proj2 = Skill("Projectile increase 2", "Projectile +1", "addition", False, prereqs=[proj1], category="bullet_number")

# Projectile skill tree
projectile_skill_tree = SkillTree("Projectile tree", 2, [proj1, proj2])

############################
# Count: 1
############################
sdtime = Skill("Slow down 1", "Slow down time when projectiles near player", "state", False)

# Slow down skill tree
slow_down_skill_tree = SkillTree("Slow down tree", 1, [sdtime])

negate = Skill("Projectile negation 1", "Spinning object around player that negates projectiles", "state", False)

# Projectile negation skill tree
projectile_negation_skill_tree = SkillTree("Projectile negation tree", 1, [negate])

bsize = Skill("Bullet size increase 1", "Increase bullet size", "addition", False, category="BULLET_SIZE")

# Bullet size increase skill tree
bullet_size_skill_tree = SkillTree("Bullet size tree", 1, [bsize])