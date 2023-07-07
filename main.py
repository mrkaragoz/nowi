# pylint: disable=no-member

from enum import IntEnum
from pathlib import Path
from typing import List, Tuple

# os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "HIDE"
import pygame  # pylint: disable=wrong-import-position

from cardlib import InputCard, MetaCard


class MouseButton(IntEnum):
    """Mouse Buttons"""

    LEFT = 1
    MIDDLE = 2
    RIGHT = 3


class App:
    """A class that holds current status of the application"""

    middle_mouse_down: bool = False
    middle_mouse_down_pos: Tuple[int, int] = (0, 0)

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


def main() -> None:
    """Main function of the Node Baed Graph Wizard"""

    # Initialize App
    app = App()

    data_path: Path = Path("data")
    font_path: Path = data_path.joinpath("fonts")

    window_width: int = 800
    window_height: int = 600

    pygame.init()
    font_consolamono_16 = pygame.font.SysFont(
        font_path.joinpath("consolamono.ttf").as_posix(), 16
    )
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Node Based Graph Wizard v0.1")

    cards: List[MetaCard] = []

    running: bool = True

    # TODO: Remove counter
    counter: int = 0

    while running:

        ########################################################################
        #                              E v e n t s                             #
        ########################################################################
        for event in pygame.event.get():
            match event.type:
                # ----------------------------------------------
                # KEYBOARD BUTTON DOWN
                # ----------------------------------------------
                case pygame.KEYDOWN:
                    match event.key:
                        # --------------------------------------
                        # DEBUG KEY
                        # --------------------------------------
                        case pygame.K_d:
                            print("----------------------")
                            print("Event: Debug Key Pressed")
                            print("Cards:")
                            for card in cards:
                                print(card)
                                print("Buttons:")
                                for button in card.buttons:
                                    print(button)
                                print("- - - - - - - - - - - -")
                            print("----------------------")
                # ----------------------------------------------
                # MOUSE BUTTON DOWN
                # ----------------------------------------------
                case pygame.MOUSEBUTTONDOWN:
                    match event.button:
                        # --------------------------------------
                        # LEFT MOUSE BUTTON
                        # --------------------------------------
                        case MouseButton.LEFT:
                            cards.append(
                                InputCard(
                                    f"File Input {counter}",
                                    event.pos[0],
                                    event.pos[1],
                                )
                            )
                            counter += 1
                        # --------------------------------------
                        # MIDDLE MOUSE BUTTON
                        # --------------------------------------
                        case MouseButton.MIDDLE:
                            # print("Middle Mouse Button Down")
                            app.set_middle_mouse_down_status(True, event.pos)
                        # --------------------------------------
                        # RIGHT MOUSE BUTTON
                        # --------------------------------------
                        case MouseButton.RIGHT:
                            for card in cards:
                                if card.get_rect().collidepoint(event.pos):
                                    # print("----------------------")
                                    # print("Event: Mouse Button Right Clicked")
                                    # print(f"Card: {card}")
                                    # print(f"Buttons: {card.buttons}")
                                    # print("----------------------")
                                    for button in card.buttons:
                                        if button.get_rect().collidepoint(event.pos):
                                            button.click()
                # ----------------------------------------------
                # BUTTON UP
                # ----------------------------------------------
                case pygame.MOUSEBUTTONUP:
                    if (
                        event.button == MouseButton.MIDDLE
                        and app.get_middle_mouse_down_status()
                    ):
                        print("Middle Mouse Button Released")
                        app.set_middle_mouse_down_status(False, event.pos)
                # ----------------------------------------------
                # MOUSE MOTION
                # ----------------------------------------------
                case pygame.MOUSEMOTION:
                    if app.get_middle_mouse_down_status():
                        for card in cards:
                            card.update_card_pos(
                                app.get_middle_mouse_down_pos(),
                                event.pos,
                            )
                        app.set_middle_mouse_down_pos(event.pos)
                    for card in cards:
                        if card.get_rect().collidepoint(event.pos):
                            # print("----------------------")
                            # print("Event: Mouse Moved")
                            # print(f"Card: {card}")
                            # print(f"Buttons: {card.buttons}")
                            # print("----------------------")
                            card.set_highlight(True)
                            for button in card.buttons:
                                # print(button)
                                if button.get_rect().collidepoint(event.pos):
                                    button.set_highlight(True)
                                else:
                                    button.set_highlight(False)
                        else:
                            card.set_highlight(False)
                # ----------------------------------------------
                # QUIT
                # ----------------------------------------------
                case pygame.QUIT:
                    running = False
                # ----------------------------------------------
                # WINDOW RESIZED OR WINDOW SIZE CHANGED
                # ----------------------------------------------
                case pygame.WINDOWRESIZED | pygame.WINDOWSIZECHANGED:
                    window_width = screen.get_width()
                    window_height = screen.get_height()
                    pygame.display.update()

        clock.tick(60)
        screen.fill((248, 241, 215))

        fps_label = font_consolamono_16.render(
            f"FPS: {clock.get_fps():.0f}", True, (0, 0, 0)
        )
        screen.blit(fps_label, (window_width - 50, 10))

        for card in cards:
            card.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
