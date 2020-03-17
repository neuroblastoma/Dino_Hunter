import thorpy
import pygame
import os
from util import Utilities


class MainMenu(thorpy.Application):
    def __init__(self, size, game_func):
        super().__init__(size, caption="Dino Hunter", flags=0)

        self.title_image = thorpy.Image(path=os.path.join("images", "dino_hunter.png"), colorkey=(0, 0, 0))
        self.start_button = thorpy.make_button("Start", func=game_func)
        self.high_score = thorpy.make_button("High Score", func=self.display_high_score)
        self.quit_button = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)
        self.bg = thorpy.Background(image=os.path.join("images", "retro_forest.jpg"), color=(200, 200, 200),
                                    elements=[self.title_image, self.start_button, self.high_score, self.quit_button])
        # Place holder
        self.menu = thorpy.Menu(self.bg)

        # React to custom Pygame events and allow us to communicate via a queue between the game and the menu
        self.high_score_reaction = thorpy.Reaction(reacts_to=pygame.USEREVENT + 4,
                                                   reac_func=Utilities.determine_highscore, params={"set_function": self.set_high_score})
        self.refresh_reaction = thorpy.Reaction(reacts_to=pygame.USEREVENT + 3, reac_func=self.refresh)

        self.set_score_reaction = thorpy.Reaction(reacts_to=pygame.USEREVENT + 2, reac_func=self.set_high_score)

    def start(self):
        """Creates and displays menu"""
        thorpy.theme.set_theme('human')
        self.bg.add_reaction(self.high_score_reaction)
        self.bg.add_reaction(self.refresh_reaction)

        thorpy.store(self.bg)
        self.menu = thorpy.Menu(self.bg)
        self.menu.play()

    def refresh(self, dummy):
        """Redraws the menu over the Pygame screen"""
        self.menu.blit_and_update()

    def return_main_menu(self):
        """Returns to the main menu"""
        thorpy.functions.quit_menu_func()
        self.menu.blit_and_update()

    def set_high_score(self, score_list, player_score, position):
        name = thorpy.Inserter.make("Congratulations! Enter initials for the Hall of Fame:", value="AAA")
        box = thorpy.make_ok_box([name])
        thorpy.auto_ok(box)
        box.center()
        thorpy.launch_blocking(box)
        pname = name.get_value()

        # Set high score
        Utilities.set_highscore(score_list, player_score, position, pname)

        # Restart main menu
        self.menu.blit_and_update()

    def display_high_score(self):
        # Title
        title_element = thorpy.make_text("Hall of Fame", 22, (255, 255, 0))
        title_element.set_font_size(50)
        title_element.set_font('helvetica')
        scores = Utilities.retrieve_highscore()

        # Scores
        display_txt = ""
        for item in scores.items():
            display_txt = display_txt + "{}  {}    {}\n".format(item[0], item[1]['name'], item[1]['score'])

        hs_element = thorpy.make_text(text=display_txt, font_size=30, font_color=(0, 0, 0))
        hs_element.set_font('helvetica')

        # Return
        return_button = thorpy.make_button(text="Return", func=self.return_main_menu)
        return_button.set_center((50, 30))

        background = thorpy.Background(image=os.path.join("images", "retro_forest.jpg"),
                                       elements=[title_element, hs_element])
        thorpy.store(background)
        hs_menu = thorpy.Menu([background, return_button])

        hs_menu.play()
