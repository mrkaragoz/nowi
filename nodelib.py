# pylint: disable=no-member

from typing import Tuple

import pygame
import pygame.gfxdraw


class MetaNode:
    """Boilerplate class for creating nodes"""

    def __init__(
        self,
        label: str,
        coord_x: int,
        coord_y: int,
        node_size: int,
        node_inner_color: Tuple[int, int, int],
        node_border_color: Tuple[int, int, int],
    ) -> None:
        self.label = label
        self.rel_coord_x = coord_x
        self.rel_coord_y = coord_y
        self.node_size = node_size
        self.node_inner_color = node_inner_color
        self.node_border_color = node_border_color
        self.surf = pygame.Surface(
            (self.node_size + 2, self.node_size + 2), pygame.SRCALPHA
        )
        # pygame.draw.circle(
        #     self.surf,
        #     self.node_inner_color,
        #     (self.node_size / 2, self.node_size / 2),
        #     self.node_size / 2,
        #     0,
        # )
        pygame.gfxdraw.filled_circle(
            self.surf,
            self.node_size // 2,
            self.node_size // 2,
            self.node_size // 2,
            self.node_inner_color,
        )
        # pygame.draw.circle(
        #     self.surf,
        #     (255, 255, 255),
        #     (self.node_size / 2, self.node_size / 2),
        #     self.node_size / 5,
        #     0,
        # )
        pygame.gfxdraw.filled_circle(
            self.surf,
            self.node_size // 2,
            self.node_size // 2,
            self.node_size // 5,
            (255, 255, 255),
        )
        # pygame.draw.circle(
        #     self.surf,
        #     self.node_border_color,
        #     (self.node_size // 2, self.node_size // 2),
        #     self.node_size // 2,
        #     2,
        # )
        pygame.gfxdraw.circle(
            self.surf,
            self.node_size // 2,
            self.node_size // 2,
            self.node_size // 2,
            self.node_border_color,
        )

    def draw(self) -> pygame.Surface:
        """Draws the node on the screen"""

        return self.surf


class Node(MetaNode):
    """Class for creating nodes"""

    node_size: int = 14
    node_inner_color: Tuple[int, int, int] = (255, 0, 0)
    node_border_color: Tuple[int, int, int] = (0, 0, 0)

    def __init__(self, label: str, coord_x: int, coord_y: int) -> None:
        self.label = label
        self.rel_coord_x = coord_x
        self.rel_coord_y = coord_y

        super().__init__(
            label,
            coord_x,
            coord_y,
            self.node_size,
            self.node_inner_color,
            self.node_border_color,
        )
