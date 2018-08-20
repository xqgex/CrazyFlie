import time
import pygame
from CrazyGame import logger
from CrazyGame.pygameUtils import colors
from CrazyGame.pygameUtils import displayBoard

cf_logger = logger.get_logger(__name__)

PICTURE_DIRECTORY = 'pictures'
WINDOW_RECT = (1000, 800)

TEXT_LINE_HEIGHT = 50
TEXT_LINE_RECT = pygame.Rect(0, WINDOW_RECT[1]-TEXT_LINE_HEIGHT,WINDOW_RECT[0],TEXT_LINE_HEIGHT)

MAIN_RECT = pygame.Rect(0, 0, WINDOW_RECT[0], WINDOW_RECT[1] - TEXT_LINE_HEIGHT)


class Drawer:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.display_surf = pygame.display.set_mode(WINDOW_RECT, pygame.HWSURFACE)
        self.text_line_font = pygame.font.SysFont("arial", 30)
        self.buttons = []
        self.board = None
        pygame.display.set_caption('Crazy Game')
        self.reset_main_rect(update_display=False)
        self.set_text_line('Welcome To Crazy Game', update_display=False)
        pygame.display.update()

    def reset_main_rect(self, update_display=True):
        pygame.draw.rect(self.display_surf, colors.RED, MAIN_RECT)
        self.buttons = []
        if update_display:
            pygame.display.update()

    def set_text_line(self, text='', update_display=True):
        pygame.draw.rect(self.display_surf, colors.WHITE, TEXT_LINE_RECT)

        textsurface = self.text_line_font.render(text, False, colors.BLACK)
        text_pos = (TEXT_LINE_RECT.centerx-textsurface.get_size()[0]/2, TEXT_LINE_RECT.y + 10)
        self.display_surf.blit(textsurface, text_pos)
        if update_display:
            pygame.display.update()

    def add_button(self, button):
        button.display_surf = self.display_surf
        button.render()
        self.buttons.append(button)

    def render_buttons(self, update_display=True):
        for button in self.buttons:
            button.render()

        if update_display:
            pygame.display.update()

    def check_buttons_mouse_event(self, event_type):
        pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.handle_mouse_event(event_type, pos):
                return button

        return None

    def set_board(self, orch):
        self.board = displayBoard.DisplayBoard(self.display_surf, orch)

    def render_board(self, update_display=False):
        if self.board:
            self.board.render()
            if update_display:
                pygame.display.update()

    def render(self):
        self.render_buttons()
        self.render_board()
        pygame.display.update()

class Button:
    BUTTON_COLORS = {'idle': colors.GREEN, 'down':colors.BLUE}
    BUTTON_TEXT_COLOR = colors.WHITE

    def __init__(self, position, size, text, image_name=None):
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.font = pygame.font.SysFont("arial", min(30, self.rect.height - 5))
        self.text = text
        self.text_surface = self.font.render(self.text, False, Button.BUTTON_TEXT_COLOR)
        self.text_position = (self.rect.centerx - self.text_surface.get_width() / 2,
                              self.rect.centery - self.text_surface.get_height() / 2)
        self.image_name = image_name
        self.color = colors.GREEN
        self.state = 'idle'

    def render(self):
        pygame.draw.rect(self.display_surf, Button.BUTTON_COLORS[self.state], self.rect)
        self.display_surf.blit(self.text_surface, self.text_position)

    def handle_mouse_event(self, event_type, mouse_location):
        if self.rect.collidepoint(*mouse_location):
            cf_logger.info('mouse event %s occurred on button %s'%(event_type, self.text))
            if event_type == pygame.MOUSEBUTTONDOWN:
                self.state = 'down'
            elif event_type == pygame.MOUSEBUTTONUP:
                if self.state == 'idle':
                    return False
                self.state = 'idle'
            self.render()
            time.sleep(0.1)
            pygame.display.update()
            return True

        if self.state == 'down':
            self.state = 'idle'
            self.render()
            pygame.display.update()

        return False
