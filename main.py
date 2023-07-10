# pylint: disable=no-member

from enum import IntEnum
from pathlib import Path
from typing import List

# os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "HIDE"
import pygame  # pylint: disable=wrong-import-position

from cardlib import InputCard, MetaCard
from menubar import MenuBar
from app import App


class MouseButton(IntEnum):
    """Mouse Buttons"""

    LEFT = 1
    MIDDLE = 2
    RIGHT = 3


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

    menubar_height: int = 25
    menubar = MenuBar(menubar_height)

    clock = pygame.time.Clock()

    pygame.display.set_caption(f"Node Based Graph Wizard v{app.get_version}")

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
                # KEYBOARD BUTTON DOWN EVENT
                # ----------------------------------------------
                case pygame.KEYDOWN:
                    match event.key:
                        # --------------------------------------
                        # [D] DEBUG KEY:
                        # Print a debug info on terminal
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
                # MOUSE BUTTON DOWN EVENT
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
                                    for button in card.buttons:
                                        if button.get_rect().collidepoint(event.pos):
                                            button.click()
                # ----------------------------------------------
                # BUTTON UP EVENT
                # ----------------------------------------------
                case pygame.MOUSEBUTTONUP:
                    if (
                        event.button == MouseButton.MIDDLE
                        and app.get_middle_mouse_down_status()
                    ):
                        print("Middle Mouse Button Released")
                        app.set_middle_mouse_down_status(False, event.pos)
                # ----------------------------------------------
                # MOUSE MOTION EVENT
                # ----------------------------------------------
                case pygame.MOUSEMOTION:
                    # ------------------------------------------
                    # SCREEN DRAGGING WITH MIDDLE MOUSE BUTTON
                    # ------------------------------------------
                    if app.get_middle_mouse_down_status():
                        for card in cards:
                            card.update_card_pos(
                                app.get_middle_mouse_down_pos(),
                                event.pos,
                            )
                        app.set_screen_drag(
                            app.get_middle_mouse_down_pos(),
                            event.pos,
                        )
                        app.set_middle_mouse_down_pos(event.pos)
                    if event.pos[1] > menubar_height:
                        # ------------------------------------------
                        # HIGHLIGHTING CARD AND BUTTONS
                        # ------------------------------------------
                        # Find the cards that collide with the mouse position and
                        # highlight the card that has biggest z_order
                        card_to_be_highlighted: MetaCard | None = None
                        for card in cards:
                            # Set all card and button highlight to false
                            card.set_highlight(False)
                            for button in card.buttons:
                                button.set_highlight(False)
                            # Find the card that collides with the mouse position
                            if card.get_rect().collidepoint(event.pos):
                                if card_to_be_highlighted is None:
                                    card_to_be_highlighted = card
                                elif (
                                    card_to_be_highlighted is not None
                                    and card.z_order > card_to_be_highlighted.z_order
                                ):
                                    card_to_be_highlighted = card
                        # Highlight the card that has biggest z_order
                        if card_to_be_highlighted is not None:
                            card_to_be_highlighted.set_highlight(True)
                            for button in card_to_be_highlighted.buttons:  # type: ignore
                                if button.get_rect().collidepoint(event.pos):
                                    button.set_highlight(True)
                                else:
                                    button.set_highlight(False)
                    else:
                        # ------------------------------------------
                        # MENUBAR ON HOVER EFFECTS
                        # ------------------------------------------
                        for menu_item in menubar.menu_items:
                            if menu_item.get_rect().collidepoint(event.pos):
                                menu_item.set_highlight(True)
                            else:
                                menu_item.set_highlight(False)
                # ----------------------------------------------
                # QUIT EVENT
                # ----------------------------------------------
                case pygame.QUIT:
                    running = False
                # ----------------------------------------------
                # WINDOW RESIZED OR WINDOW SIZE CHANGED EVENT
                # ----------------------------------------------
                case pygame.WINDOWRESIZED | pygame.WINDOWSIZECHANGED:
                    window_width = screen.get_width()
                    window_height = screen.get_height()
                    pygame.display.update()

        clock.tick(60)

        fps_label = font_consolamono_16.render(
            f"FPS: {clock.get_fps():.0f}", True, (240, 240, 240)
        )
        coordinate_label = font_consolamono_16.render(
            f"X: {app.get_screen_drag()[0]}, Y: {app.get_screen_drag()[1]}",
            True,
            (240, 240, 240),
        )

        # screen.fill((248, 241, 215))
        screen.fill((33, 40, 48))

        for card in cards:
            card.draw(screen)

        screen.blit(fps_label, (window_width - 50, 30))
        screen.blit(coordinate_label, (window_width - 100, window_height - 20))

        menubar.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
