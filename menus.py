from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'
import pygame
from utils import Button

pygame.init()


class MenuMaker:
    sounds = (pygame.mixer.Sound("./sounds/click_forward.wav"),
            pygame.mixer.Sound("./sounds/click_backward.wav"),
            pygame.mixer.Sound("./sounds/button_hover.wav"))

    def __init__(self, screen, clock, ttt_dim, screen_height, screen_width, btn_args, rtn_values):
        self.screen = screen
        self.clock = clock
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.rtn_values = rtn_values

        self.button_res_resize_height = self.screen_height/480 # 640x480 standard resolution
        self.button_res_resize_width = self.screen_width/640

        self.buttons = [Button(self.screen, self.screen_width//2, (i+1)*self.screen_height//(len(btn_args)+1), "./images/dormant.png", btn_args[i][0], (int(btn_args[i][1][0]*self.button_res_resize_width), int(btn_args[i][1][1]*self.button_res_resize_height)), btn_args[i][2]) for i in (range(len(btn_args)))]
        self.return_stuff = [(rtn_values[i], self.screen, self.clock, ttt_dim, self.screen_height, self.screen_width) for i in (range(len(rtn_values)))]

        self.hover_sound_list = [[0,0] for i in range(len(self.buttons))] # used to detect the moment mouse hovers on any button to play hover sound
        # if we play when mouse is on button, then it will play the sound indefinately till the mouse is on the button.

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (0,)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.buttons)):
                        if self.buttons[i].check_for_click(event.pos):
                            if (i == len(self.buttons)-1) and (type(self)==MenuMaker):
                                MenuMaker.sounds[1].play()
                            else:
                                MenuMaker.sounds[0].play()
                            return self.return_stuff[i]

            self.screen.fill("black")
            for i in range(len(self.buttons)):
                self.buttons[i].render_button()
                self.hover_sound_list[i][0] = self.hover_sound_list[i][1]
                self.hover_sound_list[i][1] = self.buttons[i].hover_detection(pygame.mouse.get_pos())
                if self.hover_sound_list[i] == [0,1]:
                    MenuMaker.sounds[2].play()

            pygame.display.flip()
            self.clock.tick(60)


class MainMenu(MenuMaker):
    def __init__(self, ttt_dim, screen_height, screen_width, btn_args, rtn_values, window_icon="./images/main_icon.png"):
        self.ttt_dim = 3 if ttt_dim is None else ttt_dim
        self.screen_height = 480 if screen_height is None else screen_height
        self.screen_width = 640 if screen_width is None else screen_width

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        pygame.display.set_icon(pygame.image.load(window_icon))

        super().__init__(self.screen, self.clock, self.ttt_dim, self.screen_height, self.screen_width, btn_args, rtn_values)