from typing import List, Tuple

from cardlib import InputCard, MetaCard, CardType


class App:
    """A class that holds current status of the application"""

    left_mouse_button_down: bool = False
    left_mouse_button_down_pos: Tuple[int, int] = (0, 0)

    middle_mouse_button_down: bool = False
    middle_mouse_button_down_pos: Tuple[int, int] = (0, 0)

    version_major: int = 0
    version_minor: int = 1
    version_revision: int = 0

    screen_drag_x: int = 0
    screen_drag_y: int = 0

    cards: List[MetaCard] = []

    def __init__(self):
        pass

    def add_card(self, card: CardType) -> None:
        """Add a card to the application"""
        print("Add card function called")

        if not card in CardType:
            raise TypeError("Card must be of type CardType")

        match card:
            case CardType.INPUTCARD:
                print("Card added as an input card")
                self.cards.append(InputCard("Input Card", 300, 300))

    def set_left_mouse_button_down_status(self, status, pos) -> None:
        """Set the status of the left mouse button"""
        self.left_mouse_button_down = status
        self.left_mouse_button_down_pos = pos

    def set_middle_mouse_down_status(self, status, pos) -> None:
        """Set the status of the middle mouse button"""
        self.middle_mouse_button_down = status
        self.middle_mouse_button_down_pos = pos

    def set_middle_mouse_down_pos(self, pos) -> None:
        """Set the position of the middle mouse button"""
        self.middle_mouse_button_down_pos = pos

    def get_middle_mouse_down_status(self) -> bool:
        """Get the status of the middle mouse button"""
        return self.middle_mouse_button_down

    def get_middle_mouse_down_pos(self) -> Tuple[int, int]:
        """Get the position of the middle mouse button"""
        return self.middle_mouse_button_down_pos

    def set_screen_drag(self, starting_pos, current_pos) -> None:
        """Set the screen drag value"""
        self.screen_drag_x += current_pos[0] - starting_pos[0]
        self.screen_drag_y += current_pos[1] - starting_pos[1]

    def get_screen_drag(self) -> Tuple[int, int]:
        """Get the screen drag value"""
        return self.screen_drag_x, self.screen_drag_y

    @property
    def get_version(self) -> str:
        """Get the major version number"""
        return f"{self.version_major}.{self.version_minor}.{self.version_revision}"
