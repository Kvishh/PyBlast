import pygame
import random
import abilities
from configs import *
from abilities import apply_ability

pygame.init()

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

class RollSystem:
    choices = []

    level_up_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
    level_up_overlay.fill((0,0,0, 192))

    rect_containers = [pygame.Rect(((DISPLAY_WIDTH//2)-(600//2)),(150*i)-50,600,110) for i in range(1, 4)]

    header_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 64)
    skill_name_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 42)
    skill_desc_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 22)

    rect_containers_max_ypos_dict = {i: [rect, rect.y] for i, rect in enumerate(rect_containers, start=1)}
    # The key is the index and the values are rect and original rect y

    skill_trees_choices = set([])
    skills_choices = []

    stop = False

def render_outlined(text: str, text_color: pygame.typing.ColorLike, outline_color: pygame.typing.ColorLike, outline_width: int, font) -> pygame.Surface:
        old_outline = font.outline
        if old_outline != 0:
            font.outline = 0
        base_text_surf = font.render(text, False, text_color)
        font.outline = outline_width
        outlined_text_surf = font.render(text, True, outline_color)

        outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
        font.outline = old_outline
        return outlined_text_surf

def roll(events, level_up_state, player):
    # This is to ensure that skills choices and skill trees choices roll only once
    if not RollSystem.skills_choices and not RollSystem.skill_trees_choices:
        RollSystem.stop = False

        while True:
            # Break loop if the skill tree choices length is past 3, three
            # choices are only needed
            if len(RollSystem.skill_trees_choices) >= 3:
                break
            
            # Pick random skill tree and if it has not been added to the set
            # of skill trees that will be given to the player and if every skill
            # in that tree has not been obtained by the player, then add that to
            # the top 3 skill trees
            chosen_tree = random.choice(list_of_skill_trees)
            if chosen_tree not in RollSystem.skill_trees_choices and not chosen_tree.is_exhausted:
                RollSystem.skill_trees_choices.add(chosen_tree)

        # Iteration of every skill tree's abilities_list
        for skill_tree in RollSystem.skill_trees_choices:
            for i in range(skill_tree.total_number):

                # Check if the skill object is already acquired if it is
                # not, then add it to list of skills where player will be
                # choosing
                if not skill_tree.abilities_list[i].acquired:
                    RollSystem.skills_choices.append(skill_tree.abilities_list[i])
                    break
    
    show_choices(RollSystem.skills_choices, events, level_up_state, player)

def show_choices(skills_choices, events, level_up_state, player):
    # Checks if RollSystem.choices is empty, if it is empty then fill it in
    # with skill name and description (not actual object)
    if not RollSystem.choices:
        for skill in skills_choices: RollSystem.choices.append((skill.name, skill.description))

    # Dark overlay
    display.blit(RollSystem.level_up_overlay, (0,0))

    mx, my = (pygame.mouse.get_pos()[0] * DISPLAY_WIDTH / WINDOW_WIDTH), (pygame.mouse.get_pos()[1] * DISPLAY_HEIGHT / WINDOW_HEIGHT)
    for i, val in enumerate(RollSystem.rect_containers, start=1):

        # if cursor is hovering over the rect containers, change color and moves upward a bit
        if val.collidepoint(mx, my):
            rect_bg_color = (63, 85, 117)
            val.y = max(RollSystem.rect_containers_max_ypos_dict[i][1]-10, val.y - 3)
        else:
            val.y = min(RollSystem.rect_containers_max_ypos_dict[i][1], val.y + 3)
            rect_bg_color = (23, 30, 41)

        # Drawing of the box or rect container and their border
        pygame.draw.rect(display, (rect_bg_color), (val.x, val.y, val.w, val.h), border_radius=8)
        pygame.draw.rect(display, (3, 71, 55), (val.x, val.y, val.w, val.h), 3, border_radius=8)

        # Creation of texts' surfaces
        skill_name_text = render_outlined(RollSystem.choices[i-1][0], (255,255,255), (0,0,0), 2, RollSystem.skill_name_font)
        skill_desc_text = render_outlined(RollSystem.choices[i-1][1], (255,255,255), (0,0,0), 2, RollSystem.skill_desc_font)
        header_text = render_outlined("Choose an Upgrade", (17, 255, 00), (0,0,0), 2, RollSystem.header_font)
        
        # Blitting of texts 
        display.blit(skill_name_text, (val.x+10, val.y+15))
        display.blit(skill_desc_text, (val.x+10, val.y+55))
        display.blit(header_text, ((DISPLAY_WIDTH//2)-(header_text.get_rect().w//2), 20))

        for evt in events:
            if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
                if val.collidepoint(mx, my):
                    skill = skills_choices[i-1]
                    skill.acquired = True

                    # This is to make the rect rows stop looping when player has chosen 
                    # an upgrade
                    RollSystem.stop = True

                    # Checking if the skill_tree is exhausted, meaning every skill in
                    # that tree is acquired, by iterating every skill in its abilities_list
                    for skill_tree in RollSystem.skill_trees_choices:
                        if all(skill.acquired for skill in skill_tree.abilities_list):
                            skill_tree.is_exhausted = True
                    
                    # Reset
                    RollSystem.skills_choices.clear()
                    RollSystem.skill_trees_choices.clear()
                    RollSystem.choices.clear()

                    # Applying the ability
                    apply_ability(skill, player)

        if RollSystem.stop:
            # Continue game loop
            level_up_state[0] = False
            break