from pathlib import Path
from typing import List, Tuple
from uuid import uuid4
import itertools

import pygame

from buttonlib import MetaButton, StandartButton


class MetaCard:
    """Boilerplate class for creating cards"""

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    highlight: bool = False
    title_bar_height: int = 20

    z_order_iter = itertools.count()

    pygame.font.init()

    def __init__(
        self,
        title,
        width,
        height,
        coord_x,
        coord_y,
        card_border_color,
        card_border_thickness,
        title_bar_background_color,
        title_bar_highlight_color,
        title_bar_font_color,
        body_background_color,
        buttons,
    ):
        self.uuid: str = str(uuid4())
        self.z_order: int = next(self.z_order_iter)
        self.surf: pygame.Surface = pygame.Surface((width, height))
        self.title: str = title
        self.width: int = width
        self.height: int = height
        self.coord_x: int = coord_x
        self.coord_y: int = coord_y
        self.card_border_color: Tuple[int, int, int] = card_border_color
        self.card_border_thickness: int = card_border_thickness
        self.title_bar_background_color: Tuple[
            int, int, int
        ] = title_bar_background_color
        self.title_bar_highlight_color: Tuple[int, int, int] = title_bar_highlight_color
        self.title_bar_font_color: Tuple[int, int, int] = title_bar_font_color
        self.body_background_color: Tuple[int, int, int] = body_background_color
        self.buttons: List[MetaButton] = buttons

        self.title_bar_font = pygame.font.SysFont(
            self.font_path.joinpath("consolamono.ttf").as_posix(), 14
        )

    def __str__(self) -> str:
        return f"Type: Card [{self.__class__.__name__}], Title: {self.title}, UUID: {self.uuid}, z_order: {self.z_order}"

    def draw(
        self,
        win,
    ) -> None:
        """New draw function"""

        # Draw card border
        pygame.draw.rect(
            self.surf,
            self.card_border_color,
            (0, 0, self.width, self.height),
            0,
        )

        # Draw title bar rectangle
        pygame.draw.rect(
            self.surf,
            self.title_bar_background_color
            if not self.highlight
            else self.title_bar_highlight_color,
            (
                self.card_border_thickness,
                self.card_border_thickness,
                self.width - 2 * self.card_border_thickness,
                self.title_bar_height,
            ),
            0,
        )

        # Draw title bar text
        title_text = self.title_bar_font.render(
            self.title, True, self.title_bar_font_color
        )
        self.surf.blit(title_text, (5, 5))

        # Draw card body
        pygame.draw.rect(
            self.surf,
            self.body_background_color,
            (
                self.card_border_thickness,
                self.card_border_thickness + self.title_bar_height,
                self.width - 2 * self.card_border_thickness,
                self.height - 2 * self.card_border_thickness - self.title_bar_height,
            ),
            0,
        )

        # Draw buttons if any exist
        for button in self.buttons:
            button_render = button.draw()
            self.surf.blit(button_render, (button.rel_coord_x, button.rel_coord_y))

        win.blit(self.surf, (self.coord_x, self.coord_y))

    def update_card_pos(self, starting_pos, current_pos) -> None:
        """Update Card Position"""
        self.coord_x += current_pos[0] - starting_pos[0]
        self.coord_y += current_pos[1] - starting_pos[1]

    def get_rect(self) -> pygame.Rect:
        """Get InputCard Rect"""
        return pygame.Rect((self.coord_x, self.coord_y, self.width, self.height))

    def get_button_rect(self, button_id) -> pygame.Rect:
        """Get InputCard Rect"""
        # TODO: Use a dictionary to store buttons
        for button in self.buttons:
            if button.uuid == button_id:
                return pygame.Rect(
                    (
                        self.coord_x + button.rel_coord_x,
                        self.coord_y + button.rel_coord_y,
                        button.surf_width,
                        button.surf_height,
                    )
                )
        raise RuntimeError("Button not found")

    def set_highlight(self, status) -> None:
        """Set Highlight status of the card for various effects"""
        self.highlight = status


class InputCard(MetaCard):
    """Input Card"""

    width: int = 180
    height: int = 300

    card_border_color = (27, 38, 56)
    card_border_thickness = 2
    title_bar_background_color = (174, 18, 42)
    title_bar_highlight_color = (210, 18, 42)
    title_bar_font_color = (255, 255, 255)
    body_background_color = (195, 193, 170)

    def __init__(self, title, coord_x, coord_y):
        self.buttons: List[MetaButton] = [
            StandartButton(
                self,
                "Choose File...",
                10,
                40,
                callback=lambda: print("Choose File button clicked"),
            ),
            StandartButton(
                self,
                "Refresh",
                10,
                70,
                callback=lambda: print("Refresh button clicked"),
            ),
        ]

        super().__init__(
            title,
            self.width,
            self.height,
            coord_x,
            coord_y,
            self.card_border_color,
            self.card_border_thickness,
            self.title_bar_background_color,
            self.title_bar_highlight_color,
            self.title_bar_font_color,
            self.body_background_color,
            self.buttons,
        )
