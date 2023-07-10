from functools import lru_cache
from pathlib import Path
from typing import Callable, List, Tuple
from uuid import uuid4

import pygame


class MenuBar:
    """MenuBar class"""

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    item_margin: int = 4

    background_color: Tuple[int, int, int] = (31, 31, 31)

    def __init__(self, height: int):
        self.height = height
        self.menu_items: List[MenuItem] = [
            MenuItem(0, "File", height, lambda: None),
            MenuItem(1, "Edit", height, lambda: None),
            MenuItem(2, "Selection", height, lambda: None),
            MenuItem(3, "View", height, lambda: None),
            MenuItem(4, "Go", height, lambda: None),
            MenuItem(5, "Run", height, lambda: None),
            MenuItem(6, "Terminal", height, lambda: None),
            MenuItem(7, "Help", height, lambda: None),
        ]
        dist_from_left: int = 0
        for menu_item in sorted(self.menu_items, key=lambda x: x.order):
            menu_item.abs_coord_x = dist_from_left
            menu_item.abs_coord_y = 0
            dist_from_left += menu_item.get_width() + self.item_margin

    def draw(self, win: pygame.Surface) -> None:
        """Draws the menu bar"""
        menubar_surf = pygame.Surface((win.get_width(), self.height))
        menubar_surf.fill(self.background_color)

        for menu_item in self.menu_items:
            menubar_surf.blit(
                menu_item.draw(), (menu_item.abs_coord_x, menu_item.abs_coord_y)
            )

        win.blit(menubar_surf, (0, 0))


class MenuItem:
    """MenuItem class"""

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    background_color: Tuple[int, int, int] = (31, 31, 31)
    label_color: Tuple[int, int, int] = (174, 174, 174)

    background_highlighted_color: Tuple[int, int, int] = (51, 51, 51)
    label_highlighted_color: Tuple[int, int, int] = (121, 121, 121)

    label_padding: int = 8

    def __init__(self, order, label: str, menubar_height, action: Callable):
        self.uuid: str = str(uuid4())
        self.order: int = order
        self.abs_coord_x: int = 0
        self.abs_coord_y: int = 0
        self.label: str = label
        self.highlighted: bool = False
        self.menubar_height: int = menubar_height
        self.text_surf: pygame.Surface = pygame.font.SysFont(
            self.font_path.joinpath("ConsolaMono-Book.ttf").as_posix(),
            int(menubar_height * 0.64),
            False,
        ).render(
            self.label,
            True,
            self.label_color if not self.highlighted else self.label_highlighted_color,
        )
        self.width: int = self.text_surf.get_width() + self.label_padding * 2
        self.label_height: int = self.text_surf.get_height()
        self.action: Callable = action

    def draw(self) -> pygame.Surface:
        """Draws the menu item"""

        menubar_item_width: int = self.width
        menubar_item_label_heigth: int = self.label_height

        menubar_item_surf = pygame.Surface((menubar_item_width, self.menubar_height))
        menubar_item_surf.fill(
            self.background_color
            if not self.highlighted
            else self.background_highlighted_color
        )
        menubar_item_surf.blit(
            self.text_surf,
            (
                self.label_padding,
                (self.menubar_height - menubar_item_label_heigth) / 2,
            ),
        )
        return menubar_item_surf

    @lru_cache(maxsize=16)
    def get_width(self) -> int:
        """Returns the width of the menu item"""
        return self.width

    def set_highlight(self, status) -> None:
        """Sets the highlight status of the menu item"""
        self.highlighted = status

    def get_rect(self) -> pygame.Rect:
        """Returns the rect of the menu item"""
        return pygame.Rect(
            self.abs_coord_x, self.abs_coord_y, self.width, self.menubar_height
        )
