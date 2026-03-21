import random
from configs import *
import abilities


list_of_skill_trees = [abilities.swift_fire_skill_tree,
                       abilities.fast_bullet_skill_tree,
                       abilities.hp_skill_tree,
                       abilities.movement_speed_skill_tree,
                       abilities.bullet_damage_skill_tree,
                       abilities.bullet_pierce_skill_tree,
                       abilities.shield_skill_tree,
                       abilities.bullet_bounce_skill_tree,
                       abilities.projectile_skill_tree,
                       abilities.slow_down_skill_tree,
                       abilities.projectile_negation_skill_tree,
                       abilities.bullet_size_skill_tree,
                       abilities.bullet_explosion_skill_tree]

choices = []

def roll():
    skill_trees_choices = set([])
    skills_choices = []

    while True:
        # Break loop if the skill tree choices length is past 3, three
        # choices are only needed
        if len(skill_trees_choices) >= 3:
            break

        chosen_tree = random.choice(list_of_skill_trees)
        if chosen_tree not in skill_trees_choices and not chosen_tree.is_exhausted:
            skill_trees_choices.add(chosen_tree)

    # Iteration of the skill tree's abilities_list
    for skill_tree in skill_trees_choices:
        for i in range(skill_tree.total_number):

            # Check if the skill object is already acquired if it is
            # not, then add it to list where player will be choosing
            if not skill_tree.abilities_list[i].acquired:
                skills_choices.append(skill_tree.abilities_list[i])
                break
    
    print(*(s.name for s in skills_choices))
    num_choice = int(input("pick a number: "))-1
    skills_choices[num_choice].acquired = True

    # Checking if the skill_tree is exhausted, meaning every skill in
    # that tree is acquired, by iterating every skill in its abilities_list
    for skill_tree in skill_trees_choices:
        if all(skill.acquired for skill in skill_tree.abilities_list):
            skill_tree.is_exhausted = True

    return skills_choices[num_choice]