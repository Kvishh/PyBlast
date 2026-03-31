import pygame

class FontSystem:
    font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 28)
    font_fps = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 26)
    font_timer = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 60)
    font_level = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 20)

    header_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 64)
    skill_name_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 42)
    skill_desc_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 22)

    died_header_font = pygame.font.Font("assets/font/Micro_5/Micro5-Regular.ttf", 128)

    def render_outlined(text: str, text_color: pygame.typing.ColorLike, outline_color: pygame.typing.ColorLike, outline_width: int, font) -> pygame.Surface:
        old_outline = font.outline
        if old_outline != 0:
            font.outline = 0
        base_text_surf = font.render(text, False, text_color).convert_alpha()
        font.outline = outline_width
        outlined_text_surf = font.render(text, True, outline_color).convert_alpha()

        outlined_text_surf.blit(base_text_surf, (outline_width, outline_width))
        font.outline = old_outline
        return outlined_text_surf