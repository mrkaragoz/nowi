import itertools
from enum import Enum
from pathlib import Path
from tkinter import filedialog
from typing import Dict, List, Tuple
from uuid import uuid4

import pygame

from buttonlib import MetaButton, StandartButton
from labellib import Label, MetaLabel
from nodelib import MetaNode, Node


class CardType(Enum):
    """Enum for card types"""

    INPUTCARD = 1


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
        labels,
        nodes,
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
        self.labels: List[MetaLabel] = labels
        self.nodes: List[MetaNode] = nodes

        self.title_bar_font = pygame.font.Font(
            self.font_path.joinpath("ConsolaMono-Bold.ttf").as_posix(), 10
        )

        self.file: str = ""

    def __str__(self) -> str:
        return f"Type: Card [{self.__class__.__name__}], Title: {self.title}, UUID: {self.uuid}, z_order: {self.z_order}"

    def draw(self, win) -> None:
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

        # Draw non-hidden buttons if any exist
        for button in self.buttons:
            if not button.hidden:
                button_render = button.draw()
                self.surf.blit(button_render, (button.rel_coord_x, button.rel_coord_y))

        # Draw non-hidden labels if any exist
        for label in self.labels:
            if not label.hidden:
                label_render = label.draw()
                self.surf.blit(label_render, (label.rel_coord_x, label.rel_coord_y))

        for node in self.nodes:
            node_render = node.draw()
            self.surf.blit(node_render, (node.rel_coord_x, node.rel_coord_y))

        win.blit(self.surf, (self.coord_x, self.coord_y))

    def update_z_order_to_bring_front(self) -> None:
        """Update z_order to bring card to front"""
        # TODO: Only update z_order if card is not already at front
        self.z_order = next(self.z_order_iter)

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
    height: int = 600

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
                "Input File...",
                10,
                40,
                False,
                False,
                callback=self.read_file,
                callback_args=[],
                callback_kwargs={},
            ),
            StandartButton(
                self,
                "Refresh",
                10,
                70,
                False,
                False,
                callback=print,
                callback_args=["Refresh button clicked"],
                callback_kwargs={},
            ),
        ]

        self.labels: List[MetaLabel] = [
            Label(
                "Test",
                10,
                100,
            )
        ]

        self.nodes: List[MetaNode] = []

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
            self.labels,
            self.nodes,
        )

    def read_file(self):
        """Read file"""

        file_path: Path = Path(filedialog.askopenfilename(defaultextension=".txt"))

        if not file_path.exists:
            raise FileNotFoundError(f"File {file_path} not found")

        row_number: int = 0
        titles: List[str] = []
        data: Dict[int, List[float]] = {}
        with open(file_path, "r", encoding="ISO-8859-9") as file_handle:
            for row in file_handle:
                if row_number == 0:
                    titles = row.split("\t")
                    titles = [title.strip() for title in titles if title != "\n"]
                else:
                    data[row_number] = [
                        float(value) for value in row.split("\t") if value != "\n"
                    ]
                row_number += 1

        # Hide all buttons
        for button in self.buttons:
            button.hide()

        # Hide all labels
        for label in self.labels:
            label.hide()

        for i, title in enumerate(titles):
            self.nodes.append(Node(title, 150, 30 + i * 20))

        for i, title in enumerate(titles):
            self.labels.append(Label(title, 10, 30 + i * 20))
