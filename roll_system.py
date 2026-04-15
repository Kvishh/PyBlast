import pygame
import random
import abilities
from configs import *
from abilities import apply_ability
from font_system import FontSystem as fs
from sound_system import SFX

class RollSystem:
    list_of_skill_trees = [abilities.swift_fire_skill_tree,
                       abilities.fast_bullet_skill_tree,
                       abilities.hp_skill_tree,
                       abilities.movement_speed_skill_tree,
                       abilities.bullet_damage_skill_tree,
                       abilities.bullet_pierce_skill_tree,
                       abilities.shield_skill_tree,
                       abilities.bullet_bounce_skill_tree,
                       abilities.projectile_negation_skill_tree,
                       abilities.bullet_size_skill_tree,
                       abilities.bullet_explosion_skill_tree]
    
    cached_skill_name_and_desc_surfs = {}
    for tree in list_of_skill_trees:
        for skill in tree.abilities_list:
            # Keys are tuple of string skill's name and description, values are the surfaces of skill's name and description
            cached_skill_name_and_desc_surfs[(skill.name, skill.description)] = [fs.render_outlined(skill.name, (255,255,255), (0,0,0), 2, fs.skill_name_font),
                                                                           fs.render_outlined(skill.description, (255,255,255), (0,0,0), 2, fs.skill_desc_font)]
    

    # Header text: "Choose an Upgrade"
    header_text = fs.render_outlined("Choose an Upgrade", (17, 255, 00), (0,0,0), 2, fs.header_font)

    choices = []

    level_up_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
    level_up_overlay.fill((0,0,0, 192))

    rect_containers = [pygame.Rect(((DISPLAY_WIDTH//2)-(600//2)),(150*i)-50,600,110) for i in range(1, 4)]

    rect_containers_max_ypos_dict = {i: [rect, rect.y] for i, rect in enumerate(rect_containers, start=1)}
    # The key is the index and the values are rect and original rect y

    skill_trees_choices = set([])
    skills_choices = []

    # Used to stop showing the roll and continue the game loop
    stop = False

    roll_layer = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
    roll_layer_pos_y = -DISPLAY_HEIGHT
    bounce_up = False

    # To check whether upgrades are now clickable
    is_clickable = False
    
    # Vanilla overlay before showing the upgrades
    flash_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
    flash_overlay_alpha = 2
    flash_overlay.fill((255, 249, 201, flash_overlay_alpha))


def roll(events, level_up_state, player, last_frame):
    """Responsible for the randomize abilities that show when player leveled up."""

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
            chosen_tree = random.choice(RollSystem.list_of_skill_trees)
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
    
    show_choices(RollSystem.skills_choices, events, level_up_state, player, last_frame)

def show_choices(skills_choices, events, level_up_state, player, last_frame):
    """The function responsible for showing the available abilities player can choose, including the animation"""

    # Checks if RollSystem.choices is empty, if it is empty then fill it in
    # with skill name and description (not actual object)
    if not RollSystem.choices:
        for skill in skills_choices: RollSystem.choices.append((skill.name, skill.description))
        SFX.level_up_sfx.play()
    
    # The alpha is used as timer and also used as the alpha for flash overlay
    if RollSystem.flash_overlay_alpha < 192:
        RollSystem.flash_overlay_alpha = min(192, RollSystem.flash_overlay_alpha+1)
        RollSystem.flash_overlay.fill((255, 249, 201, RollSystem.flash_overlay_alpha))

        # This only blits the flash overlay until alpha hits 92, if it is more than
        # 92 then nothing happens, no flash overlay is blitted. Until the alpha 
        # has not reached 192 then the roll will not be shown yet.
        if RollSystem.flash_overlay_alpha < 92: display.blit(RollSystem.flash_overlay, (0,0))
    else:
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
            # pygame.draw.rect(display, (rect_bg_color), (val.x, val.y, val.w, val.h), border_radius=8)
            pygame.draw.rect(RollSystem.roll_layer, (rect_bg_color), (val.x, val.y, val.w, val.h), border_radius=8)
            # pygame.draw.rect(display, (3, 71, 55), (val.x, val.y, val.w, val.h), 3, border_radius=8)
            pygame.draw.rect(RollSystem.roll_layer, (3, 71, 55), (val.x, val.y, val.w, val.h), 3, border_radius=8)

            # First is skill name and second is skill description, both are strings
            keys = RollSystem.choices[i-1][0], RollSystem.choices[i-1][1]

            # The text surfaces with outlines
            # The value is list, first element is surface of skill name
            skill_name_text_surf = RollSystem.cached_skill_name_and_desc_surfs[keys][0] 
            # The value is list, second element is surface of skill description
            skill_desc_text_surf = RollSystem.cached_skill_name_and_desc_surfs[keys][1]
            
            # Blitting of texts 
            # display.blit(skill_name_text_surf, (val.x+10, val.y+15))
            RollSystem.roll_layer.blit(skill_name_text_surf, (val.x+10, val.y+15))
            # display.blit(skill_desc_text_surf, (val.x+10, val.y+55))
            RollSystem.roll_layer.blit(skill_desc_text_surf, (val.x+10, val.y+55))
            # display.blit(RollSystem.header_text, ((DISPLAY_WIDTH//2)-(RollSystem.header_text.get_rect().w//2), 20))
            RollSystem.roll_layer.blit(RollSystem.header_text, ((DISPLAY_WIDTH//2)-(RollSystem.header_text.get_rect().w//2), 20))

            # Another layer which is where everything in the roll is blitted
            display.blit(RollSystem.roll_layer, (0,RollSystem.roll_layer_pos_y))
            # Refresh in order to clean up the last frame
            RollSystem.roll_layer.fill((0,0,0,0))

            # Move down the another layer/surface to make the effect of dropping down
            if not RollSystem.bounce_up:
                RollSystem.roll_layer_pos_y = min(100, RollSystem.roll_layer_pos_y+4)

                # If it's reached past the bottom, then it should bounce up
                if RollSystem.roll_layer_pos_y >= 100: RollSystem.bounce_up = True
            # If bounce_up is True, then it should slowly go up and stop exactly a y=0
            else:
                RollSystem.roll_layer_pos_y = max(0, RollSystem.roll_layer_pos_y-2)

                # If RollSystem.roll_layer_pos_y has reached 0 then and only then handle the clicking of rects.
                if RollSystem.roll_layer_pos_y <= 0: RollSystem.is_clickable = True

            # This is to check if the preparation is done, if the RollSystem.roll_layer y pos has reached
            # 0 then handle clicks.
            # This ensures that the player does not accidentally click the upgrade immediately after leveling
            # up.
            if RollSystem.is_clickable:
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
                            reset(last_frame)

                            # Applying the ability
                            apply_ability(skill, player)

            if RollSystem.stop:
                # Continue game loop
                level_up_state[0] = False
                break
    
def reset(last_frame=None):
    if last_frame is not None: last_frame.clear()

    RollSystem.skills_choices.clear()
    RollSystem.skill_trees_choices.clear()
    RollSystem.choices.clear()
    RollSystem.flash_overlay_alpha = 2
    RollSystem.bounce_up = False
    RollSystem.roll_layer_pos_y = -DISPLAY_HEIGHT
    RollSystem.is_clickable = False