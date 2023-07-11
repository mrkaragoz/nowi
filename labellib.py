from pathlib import Path
from typing import Tuple
from uuid import uuid4

import pygame


class MetaLabel:
    """Meta class for labels"""

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    def __init__(
        self,
        uuid,
        label,
        rel_coord_x,
        rel_coord_y,
        font_name,
        font_color,
        font_size,
    ):
        self.uuid = uuid
        self.label = label
        self.rel_coord_x = rel_coord_x
        self.rel_coord_y = rel_coord_y
        self.font_name = font_name
        self.font_color = font_color
        self.font_size = font_size

        if not self.font_path.joinpath(font_name).exists:
            raise FileNotFoundError(f"Font {font_name} not found")
        self.font = pygame.font.SysFont(
            self.font_path.joinpath(font_name).as_posix(), font_size
        )

    def __str__(self):
        return f"{self.uuid}: {self.label}"

    def draw(self) -> pygame.Surface:
        """Draw label"""
        label_surf = self.font.render(self.label, True, self.font_color)
        return label_surf


class Label(MetaLabel):
    """Standart label class"""

    font_name: str = "ConsolaMono-Book.ttf"
    font_color: Tuple[int, int, int] = (0, 0, 0)
    font_size: int = 16

    hidden: bool = False

    def __init__(self, label, rel_coord_x, rel_coord_y):
        self.uuid: str = str(uuid4())
        self.label = label
        self.coord_x = rel_coord_x
        self.coord_y = rel_coord_y
        super().__init__(
            self.uuid,
            label,
            rel_coord_x,
            rel_coord_y,
            self.font_name,
            self.font_color,
            self.font_size,
        )
