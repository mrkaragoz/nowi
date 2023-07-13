from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Self, Tuple
from uuid import uuid4

import pygame

from app import App
from cardlib import CardType


class MenuBar(App):
    """MenuBar class"""

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    item_margin: int = 4

    background_color: Tuple[int, int, int] = (31, 31, 31)

    def __init__(self, height: int):
        self.height = height
        add_input_card_menu: MenuItem = MenuItem(
            self, 0, "Input Card", self.add_card, args=[CardType.INPUTCARD], kwargs={}
        )

        self.menu_items: List[MenuItem] = [
            add_input_card_menu,
            MenuItem(self, 1, "Exit", print, args=["Exit Clicked"], kwargs={}),
        ]

        dist_from_left: int = 0
        for menu_item in sorted(self.menu_items, key=lambda x: x.order):
            menu_item.abs_coord_x = dist_from_left
            menu_item.abs_coord_y = 0
            dist_from_left += menu_item.get_width() + self.item_margin
            for child in menu_item.children:
                child.abs_coord_x = menu_item.abs_coord_x
                child.abs_coord_y = self.height + child.order * 25
                child.width = 200
                print(child.abs_coord_x, child.abs_coord_y)

    def draw(self, win: pygame.Surface) -> None:
        """Draws the menu bar"""
        menubar_surf = pygame.Surface((win.get_width(), self.height))
        menubar_surf.fill(self.background_color)

        for menu_item in self.menu_items:
            menubar_surf.blit(
                menu_item.draw(), (menu_item.abs_coord_x, menu_item.abs_coord_y)
            )

        for menu_item in self.menu_items:
            if menu_item.open:
                child_menu_surf = pygame.Surface((200, 25 * len(menu_item.children)))
                for i, child in enumerate(menu_item.children):
                    pygame.draw.rect(
                        child_menu_surf,
                        child.background_color,
                        (
                            0,
                            i * 25,
                            200,
                            25,
                        ),
                    )
                    child_menu_surf.blit(
                        child.text_surf,
                        (15, i * 25 + (25 - child.text_surf.get_height()) / 2),
                    )

                win.blit(
                    child_menu_surf,
                    (menu_item.abs_coord_x, menu_item.abs_coord_y + self.height),
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

    def __init__(
        self,
        menubar: MenuBar,
        order: int,
        label: str,
        action: Callable,
        args: List[Any],
        kwargs: Dict[str, Any],
    ):
        self.uuid: str = str(uuid4())
        self.order: int = order
        self.abs_coord_x: int = 0
        self.abs_coord_y: int = 0
        self.label: str = label
        self.highlighted: bool = False
        self.menubar_height: int = menubar.height
        self.text_surf: pygame.Surface = pygame.font.SysFont(
            self.font_path.joinpath("ConsolaMono-Book.ttf").as_posix(),
            int(self.menubar_height * 0.64),
            False,
        ).render(
            self.label,
            True,
            self.label_color if not self.highlighted else self.label_highlighted_color,
        )
        self.width: int = self.text_surf.get_width() + self.label_padding * 2
        self.label_height: int = self.text_surf.get_height()
        self.action: Callable = action
        self.args = args
        self.kwargs = kwargs
        self.children: List[Self] = []
        self.open: bool = False

    def add_child(self, child: Self):
        """Adds a chield to the menu item"""
        self.children.append(child)

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

    def click(self) -> None:
        """Executes the action of the menu item"""
        self.action(*self.args, **self.kwargs)

    def close(self) -> None:
        """Closes the menu at the given order"""
        self.open = False

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
