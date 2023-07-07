from typing import Tuple


class App:
    """A class that holds current status of the application"""

    middle_mouse_down: bool = False
    middle_mouse_down_pos: Tuple[int, int] = (0, 0)

    version_major: int = 0
    version_minor: int = 1
    version_revision: int = 0

    screen_drag_x: int = 0
    screen_drag_y: int = 0

    def __init__(self):
        pass

    def set_middle_mouse_down_status(self, status, pos) -> None:
        """Set the status of the middle mouse button"""
        self.middle_mouse_down = status
        self.middle_mouse_down_pos = pos

    def set_middle_mouse_down_pos(self, pos) -> None:
        """Set the position of the middle mouse button"""
        self.middle_mouse_down_pos = pos

    def get_middle_mouse_down_status(self) -> bool:
        """Get the status of the middle mouse button"""
        return self.middle_mouse_down

    def get_middle_mouse_down_pos(self) -> Tuple[int, int]:
        """Get the position of the middle mouse button"""
        return self.middle_mouse_down_pos

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
