import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, EDITOR_DATA, BUTTON_BG_COLOR, BUTTON_LINE_COLOR
from collections import defaultdict


class Button(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, rect, items, items_alt=None) -> None:
        super().__init__(groups)
        self.rect = rect
        self.image = pygame.Surface(self.rect.size)

        self.items = {'main': items, 'alt': items_alt}
        self.index = 0
        self.main_active = True

    def update(self) -> None:
        self.image.fill(BUTTON_BG_COLOR)
        if self.main_active:
            surface = self.items['main'][self.index][1]
        else:
            surface = self.items['alt'][self.index][1]
        x = self.rect.width / 2
        y = self.rect.height / 2
        rect = surface.get_rect(center=(x, y))
        self.image.blit(surface, rect)

    def get_id(self) -> int:
        if self.main_active:
            return self.items['main'][self.index][0]
        else:
            return self.items['alt'][self.index][0]

    def switch(self):
        self.index += 1
        if self.main_active:
            if self.index >= len(self.items['main']):
                self.index = 0
        else:
            if self.index >= len(self.items['alt']):
                self.index = 0


class Menu:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.rect = self.create_menu_rect()

        self.assets = self.import_assets()
        self.buttons = pygame.sprite.Group()
        self.tile_button_rect, self.coin_button_rect, self.enemy_button_rect, self.tree_button_rect = self.create_button_rects()
        Button(self.buttons, self.tile_button_rect, self.assets['terrain'])
        Button(self.buttons, self.coin_button_rect, self.assets['coin'])
        Button(self.buttons, self.enemy_button_rect, self.assets['enemy'])
        Button(self.buttons, self.tree_button_rect, self.assets['palm fg'], self.assets['palm bg'])

    @staticmethod
    def create_menu_rect() -> pygame.Rect:
        size = 180
        margin = 6
        topleft = WINDOW_WIDTH - size - margin, WINDOW_HEIGHT - size - margin
        return pygame.Rect(topleft, (size, size))

    @staticmethod
    def import_assets() -> dict[str: list[tuple[int, pygame.Surface]]]:
        surfaces = defaultdict(list)
        for key, value in EDITOR_DATA.items():
            if value['menu_surf']:
                surfaces[value['menu']].append((key, pygame.image.load(value['menu_surf'][1:])))
        return dict(surfaces)

    def click(self, mouse_pos: tuple[int, int], mouse_button):
        button: Button
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                left, middle, right = mouse_button
                if middle:
                    if button.items['alt']:
                        button.main_active = not button.main_active
                    else:
                        button.main_active = True
                if right:
                    button.switch()
                return button.get_id()

    def create_button_rects(self) -> list[pygame.Rect]:
        size = 90
        margin = 5
        generic_button_rect = pygame.Rect(self.rect.topleft, (size, size)).inflate(-margin, -margin)

        tile_button_rect = generic_button_rect.copy()
        coin_button_rect = generic_button_rect.copy().move(self.rect.width / 2, 0)
        enemy_button_rect = generic_button_rect.copy().move(self.rect.width / 2, self.rect.width / 2)
        tree_button_rect = generic_button_rect.copy().move(0, self.rect.width / 2)

        return [tile_button_rect, coin_button_rect, enemy_button_rect, tree_button_rect]

    def highlight_selected_button(self, index: int) -> None:
        selected_menu_item = EDITOR_DATA[index]['menu']
        if selected_menu_item == 'terrain':
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.tile_button_rect.inflate(4, 4), 5, 4)
        elif selected_menu_item == 'coin':
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.coin_button_rect.inflate(4, 4), 5, 4)
        elif selected_menu_item == 'enemy':
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.enemy_button_rect.inflate(4, 4), 5, 4)
        else:
            pygame.draw.rect(self.display_surface, BUTTON_LINE_COLOR, self.tree_button_rect.inflate(4, 4), 5, 4)

    def display(self, selected_index: int) -> None:
        self.buttons.update()
        self.buttons.draw(self.display_surface)
        self.highlight_selected_button(selected_index)
