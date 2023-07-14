from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple
from uuid import uuid4

import pygame


class MetaButton:
    """Boilerplate class for creating buttons"""

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    pygame.font.init()

    def __init__(
        self,
        parent: Any,
        text: str,
        rel_corrd_x: int,
        rel_coord_y: int,
        bg_color: Tuple[int, int, int],
        bg_disabled_color: Tuple[int, int, int],
        highlight_color: Tuple[int, int, int],
        border_color: Tuple[int, int, int],
        font_name: str,
        font_color: Tuple[int, int, int],
        font_size: int,
        border_thickness: int,
        disabled: bool,
        hidden: bool,
        callback: Callable,
        callback_args: List[Any],
        callback_kwargs: Dict[str, Any],
    ):
        """Initialize Button"""
        self.uuid = uuid4()
        # print(f"Button initialize with uuid: {self.uuid}")
        self.parent_card = parent
        self.highlight: bool = False
        self.text: str = text
        self.rel_coord_x: int = rel_corrd_x
        self.rel_coord_y: int = rel_coord_y
        self.bg_color: Tuple[int, int, int] = bg_color
        self.bg_disabled_color: Tuple[int, int, int] = bg_disabled_color
        self.highlight_color: Tuple[int, int, int] = highlight_color
        self.border_color: Tuple[int, int, int] = border_color
        if not self.font_path.joinpath(font_name).exists:
            raise FileNotFoundError(f"Font {font_name} not found")
        # print(f"Font {self.font_path.joinpath(font_name).as_posix()} loaded")
        self.font = pygame.font.SysFont(
            self.font_path.joinpath(font_name).as_posix(), font_size
        )
        self.font_color: Tuple[int, int, int] = font_color
        self.width = (
            self.get_text_width_height(text, self.font)[0] + (font_size / 3) * 2
        )

        self.height = font_size + (font_size / 3) * 2
        self.border_thickness = border_thickness
        self.surf_width = self.width + border_thickness * 2
        self.surf_height = self.height + border_thickness * 2
        self.surf = pygame.Surface((self.surf_width, self.surf_height))
        self.disabled = disabled
        self.hidden = hidden
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs

    def __str__(self) -> str:
        """String representation of the button"""
        return f"Type: Button [{self.__class__.__name__}], Text: {self.text}, UUID: {self.uuid}, Parent: {self.parent_card}"

    @lru_cache(maxsize=1024)
    def get_text_width_height(
        self, text: str, font: pygame.font.Font
    ) -> Tuple[int, int]:
        """Get text width in specific font and size"""
        text_render: pygame.Surface = font.render(text, True, (0, 0, 0))
        return (text_render.get_width(), text_render.get_height())

    def get_rect(self) -> pygame.Rect:
        """Get rect of the button"""
        if self.parent_card is not None:
            return self.parent_card.get_button_rect(self.uuid)
        else:
            raise RuntimeError("Parent card is not set")

    def click(self) -> None:
        """Call callback function"""
        if self.disabled:
            return
        print(f"Button [{self.uuid}] {self.text} clicked")
        print(f"Parent card: {self.parent_card}")
        ret = self.callback(*self.callback_args, **self.callback_kwargs)

    def set_highlight(self, status: bool) -> None:
        """Set highlight state"""
        self.highlight = status

    def set_disabled(self, status: bool) -> None:
        """Set disabled state"""
        self.disabled = status

    def draw(self) -> pygame.Surface:
        """Draw button on surface"""
        self.surf.fill(self.border_color)
        if self.disabled:
            bg_color: Tuple[int, int, int] = self.bg_disabled_color
        elif self.highlight:
            bg_color = self.highlight_color
        else:
            bg_color = self.bg_color
        pygame.draw.rect(
            self.surf,
            bg_color,
            (
                self.border_thickness,
                self.border_thickness,
                self.width - self.border_thickness * 2,
                self.height - self.border_thickness * 2,
            ),
        )

        button_text = self.font.render(self.text, True, self.font_color)
        text_width, text_height = self.get_text_width_height(self.text, self.font)

        self.surf.blit(
            button_text,
            ((self.surf_width - text_width) / 2, (self.surf_height - text_height) / 2),
        )

        return self.surf

    def hide(self) -> None:
        """Hide button"""
        self.hidden = True


class StandartButton(MetaButton):
    """Standart Button"""

    bg_color: Tuple[int, int, int] = (27, 38, 56)
    bg_disabled_color: Tuple[int, int, int] = (2, 3, 4)
    highlight_color: Tuple[int, int, int] = (99, 140, 208)
    border_color: Tuple[int, int, int] = (0, 0, 0)
    border_thickness: int = 1
    font_color: Tuple[int, int, int] = (255, 255, 255)
    font_name: str = "ConsolaMono-Bold.ttf"
    font_size: int = 16

    def __init__(
        self,
        parent: Any,
        text: str,
        rel_coord_x: int,
        rel_coord_y: int,
        disabled: bool,
        hidden: bool,
        callback: Callable,
        callback_args: List[Any],
        callback_kwargs: Dict[str, Any],
    ):
        super().__init__(
            parent,
            text,
            rel_coord_x,
            rel_coord_y,
            self.bg_color,
            self.bg_disabled_color,
            self.highlight_color,
            self.border_color,
            self.font_name,
            self.font_color,
            self.font_size,
            self.border_thickness,
            disabled,
            hidden,
            callback,
            callback_args,
            callback_kwargs,
        )
