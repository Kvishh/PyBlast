class Skill:
    def __init__(self, name, description, is_acquired, prereqs=None):
        self.name = name
        self.description = description
        self.prerequisites = prereqs if prereqs else []
        self.acquired = is_acquired

class SkillTree:
    def __init__(self, name, total_number, abilities_list: list[Skill], is_exhausted = False):
        self.name = name
        self.total_number = total_number
        self.abilities_list = abilities_list
        self.is_exhausted = is_exhausted

############################
# Count: 5
############################
sw1 = Skill("Swift fire 1", "Fire rate +25%", False)
sw2 = Skill("Swift fire 2", "Fire rate +10%", False, [sw1])
sw3 = Skill("Swift fire 3", "Fire rate +10%", False, [sw1, sw2])
sw4 = Skill("Swift fire 4", "Fire rate +10%", False, [sw1, sw2, sw3])
sw5 = Skill("Swift fire 5", "Fire rate +30% (maxed out)", False, [sw1, sw2, sw3, sw4])

# Swift fire skill tree
swift_fire_skill_tree = SkillTree("Swift fire tree", 5, [sw1,sw2,sw3,sw4,sw5])

fb1 = Skill("Fast Bullet 1", "Bullet speed +20%", False)
fb2 = Skill("Fast Bullet 2", "Bullet speed +10%", False, [fb1])
fb3 = Skill("Fast Bullet 3", "Bullet speed +10%", False, [fb1, fb2])
fb4 = Skill("Fast Bullet 4", "Bullet speed +10%", False, [fb1, fb2, fb3])
fb5 = Skill("Fast Bullet 5", "Bullet speed +10% (maxed out)", False, [fb1, fb2, fb3, fb4])

# Fast bullet skill tree
fast_bullet_skill_tree = SkillTree("Fast bullet tree", 5, [fb1,fb2,fb3,fb4,fb5])

hp1 = Skill("Max hp 1", "Max hp +1", False)
hp2 = Skill("Max hp 1", "Max hp +1", False, [hp1])
hp3 = Skill("Max hp 1", "Max hp +1", False, [hp1, hp2])
hp4 = Skill("Max hp 1", "Max hp +1", False, [hp1, hp2, hp3])
hp5 = Skill("Max hp 1", "Max hp +1", False, [hp1, hp2, hp3, hp4])

# HP skill tree
hp_skill_tree = SkillTree("Max hp tree", 5, [hp1,hp2,hp3,hp4,hp5])


############################
# Count: 4
############################
ms1 = Skill("Movement speed 1", "Movement speed +10%", False)
ms2 = Skill("Movement speed 2", "Movement speed +10%", False, [ms1])
ms3 = Skill("Movement speed 3", "Movement speed +10%", False, [ms1, ms2])
ms4 = Skill("Movement speed 4", "Movement speed +10% (maxed out)", False, [ms1, ms2, ms3])

# Movement speed skill tree
movement_speed_skill_tree = SkillTree("Movement speed tree", 4, [ms1,ms2,ms3,ms4])


############################
# Count: 3
############################
bd1 = Skill("Bullet damage 1", "Bullet damage +5", False)
bd2 = Skill("Bullet damage 2", "Bullet damage +5", False, [bd1])
bd3 = Skill("Bullet damage 3", "Bullet damage +10 (maxed out)", False, [bd1, bd2])

# Bullet damage skill tree
bullet_damage_skill_tree = SkillTree("Bullet damage tree", 3, [bd1, bd2, bd3])

pb1 = Skill("Piercing bullet 1", "Bullet pierce +1", False)
pb2 = Skill("Piercing bullet 2", "Bullet pierce +1", False, [pb1])
pb3 = Skill("Piercing bullet 3", "Bullet pierce +1", False, [pb1, pb2])

# Bullet pierce skill tree
bullet_pierce_skill_tree = SkillTree("Bullet pierce tree", 3, [pb1, pb2, pb3])

s1 = Skill("Shield 1", "Shield +1", False)
s2 = Skill("Shield 2", "Shield +1", False, [s1])
s3 = Skill("Shield 3", "Shield +1", False, [s1, s2])

# Shield skill tree
shield_skill_tree = SkillTree("Shield tree", 3, [s1, s2, s3])


############################
# Count: 2
############################
bb1 = Skill("Bullet bounce 1", "Bullet bounce +1", False)
bb2 = Skill("Bullet bounce 2", "Bullet bounce +1", False, [bb1])

# Bullet bounce skill tree
bullet_bounce_skill_tree = SkillTree("Bullet bounce tree", 2, [bb1, bb2])

proj1 = Skill("Projectile increase 1", "Projectile +1", False)
proj2 = Skill("Projectile increase 2", "Projectile +1", False, [proj1])

# Projectile skill tree
projectile_skill_tree = SkillTree("Projectile tree", 2, [proj1, proj2])

############################
# Count: 1
############################
sdtime = Skill("Slow down 1", "Slow down time when projectiles near player", False)

# Slow down skill tree
slow_down_skill_tree = SkillTree("Slow down tree", 1, [sdtime])

negate = Skill("Projectile negation 1", "Spinning object around player that negates projectiles", False)

# Projectile negation skill tree
projectile_negation_skill_tree = SkillTree("Projectile negation tree", 1, [negate])

bsize = Skill("Bullet size increase 1", "Increase bullet size", False)

# Bullet size increase skill tree
bullet_size_skill_tree = SkillTree("Bullet size tree", 1, [bsize])